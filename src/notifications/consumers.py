from channels.generic.websocket import WebsocketConsumer

from .models import Client

class NotificationsConsumer(WebsocketConsumer):
    def connect(self):
        Client.objects.create(channel_name=self.channel_name, user=self.scope['user'])

    def disconnect(self, close_code):
        Client.objects.get(channel_name=self.channel_name).delete()

    def receive(self, event):
        self.send(text_data=event["text"])
