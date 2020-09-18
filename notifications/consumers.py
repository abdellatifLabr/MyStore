from channels.generic.websocket import JsonWebsocketConsumer
from graphql_jwt.shortcuts import get_user_by_token

from .models import Client

class NotificationsConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        try:
            Client.objects.get(channel_name=self.channel_name).delete()
        except Client.DoesNotExist:
            pass

    def receive_json(self, content):
        if content['type'] == 'auth':
            token = content['text']
            user = get_user_by_token(token)
            Client.objects.create(channel_name=self.channel_name, user=user)
    
    def notification(self, event):
        self.send_json({
            'type': 'websocket.send',
            'text': event
        })
