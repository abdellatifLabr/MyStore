import json

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext
from django.core import serializers
from channels.layers import get_channel_layer

class Client(models.Model):
    channel_name = models.CharField(max_length=64)
    user = models.ForeignKey(get_user_model(), related_name='clients', on_delete=models.CASCADE)

    async def send(self, type, data):
        channel_layer = get_channel_layer()
        await channel_layer.send(self.channel_name, { 'type': type, 'data': data })

class NotificationType(models.Model):
    name = models.CharField(max_length=64)
    action = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Notification(models.Model):
    seen = models.BooleanField(default=False)
    type = models.ForeignKey(NotificationType, related_name='notifications', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name='notifications', on_delete=models.CASCADE)

    # source is a dynamic foreign key
    source = models.ForeignKey(ContentType, related_name='notifications', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('source', 'object_id')

    def send(self):
        for client in self.user.clients.iterator():
            source = json.loads(serializers.serialize('json', [self.source]))
            client.send('notification', {
                'type': self.type.name,
                'action': gettext(self.type.action),
                'source': source.fields
            })
