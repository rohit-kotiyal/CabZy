from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification


def send_notification(user, type, title, message):
    
    # save to DB
    Notification.objects.create(
        user = user,
        type = type,
        title = title,
        message = message
    )


    # push via websocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{user.id}",
        {
            "type": 'send_notification',
            'title': title,
            'message': message,
        }
    )