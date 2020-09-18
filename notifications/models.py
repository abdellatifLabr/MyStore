import json

from django.db import models
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.humanize.templatetags import humanize
from django.utils.translation import gettext
from django.core import serializers
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from shopping.models import Product, Store, Subscription

class Client(models.Model):
    channel_name = models.CharField(max_length=128)
    user = models.ForeignKey(get_user_model(), related_name='clients', on_delete=models.CASCADE)

    def send(self, type, data):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(self.channel_name, { 'type': type, 'data': data })
    
    def __str__(self):
        return f'Client - {self.user}'

class NotificationType(models.Model):
    name = models.CharField(max_length=64)
    action = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class NotificationSource(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Notification(models.Model):
    seen = models.BooleanField(default=False)
    type = models.ForeignKey(NotificationType, related_name='notifications', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name='notifications', on_delete=models.CASCADE)
    source = models.ForeignKey(NotificationSource, related_name='notifications', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def time_ago(self):
        return humanize.naturaltime(self.created)

    def send(self):
        for client in self.user.clients.iterator():
            source = json.loads(serializers.serialize('json', [self.source.content_object]))[0]
            client.send('notification', {
                'type': self.type.name,
                'action': gettext(self.type.action),
                'created': str(self.time_ago),
                'source': source['fields']
            })


def send_product_release_notifications(sender, instance, created, **kwargs):
    if created:
        product = instance
        for subscription in product.store.subscriptions.iterator():
            notification_source, created = NotificationSource.objects.get_or_create(
                content_type=ContentType.objects.get_for_model(Store),
                object_id=product.store.id
            )
            notification = Notification.objects.create(
                user=subscription.user,
                type=NotificationType.objects.get(name='PRODUCT_RELEASE'),
                source=notification_source
            )
            notification.send()

def send_subscription_notifications(sender, instance, created, **kwargs):
    if created:
        subscription = instance
        notification_source = NotificationSource.objects.create(
            content_object=subscription.user
        )
        notification = Notification.objects.create(
            user=subscription.store.user,
            type=NotificationType.objects.get(name='SUBSCRIPTION'),
            source=notification_source
        )
        notification.send()

post_save.connect(send_subscription_notifications, sender=Subscription)
post_save.connect(send_product_release_notifications, sender=Product)
