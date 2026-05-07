import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']

        if isinstance(user, AnonymousUser):
            await self.close()
            return

        self.group_name = f"notifications_{user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        """Receive notification from group and send to WebSocket client."""
        await self.send(text_data=json.dumps({
            'type':    'notification',
            'title':   event['title'],
            'message': event['message'],
        }))