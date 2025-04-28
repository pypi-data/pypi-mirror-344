import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        room = self.scope['url_route']['kwargs']['room']
        self.room_group_name = f'notification_{room}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def notification(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))
