import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser


class RideConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ride_id   = self.scope['url_route']['kwargs']['ride_id']
        self.room_name = f"ride_{self.ride_id}"
        user           = self.scope['user']

        # reject unauthenticated connections
        if isinstance(user, AnonymousUser):
            await self.close()
            return

        # join ride group
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        """Driver sends GPS location updates through here."""
        data = json.loads(text_data)
        user = self.scope['user']

        if data.get('type') == 'location_update':
            # save to DB
            await self.update_driver_location(
                user, data.get('lat'), data.get('lng')
            )
            # broadcast to everyone in ride group
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'driver_location',
                    'lat':  data.get('lat'),
                    'lng':  data.get('lng'),
                }
            )

    async def driver_location(self, event):
        """Broadcast driver location to all connected clients."""
        await self.send(text_data=json.dumps({
            'type': 'driver_location',
            'lat':  event['lat'],
            'lng':  event['lng'],
        }))

    async def ride_status_update(self, event):
        """Broadcast ride status changes."""
        await self.send(text_data=json.dumps({
            'type':   'ride_status_update',
            'status': event['status'],
        }))

    @database_sync_to_async
    def update_driver_location(self, user, lat, lng):
        try:
            profile             = user.driver_profile
            profile.current_lat = lat
            profile.current_lng = lng
            profile.save()
        except Exception:
            pass