from django.db import models
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer

class ClientManager(models.Manager):

    def notify(self, *args, **kwargs):
        for client in self.iterator():
            client.notify(*args, **kwargs)


class Client(models.Model):
    channel_name = models.CharField(max_length=64)
    user = models.ForeignKey(get_user_model(), related_name='clients', on_delete=models.CASCADE)

    objects = ClientManager()

    def notify(self, *args, **kwargs):
        channel_layer = get_channel_layer(self.channel_name)
        channel_layer.send(*args)
