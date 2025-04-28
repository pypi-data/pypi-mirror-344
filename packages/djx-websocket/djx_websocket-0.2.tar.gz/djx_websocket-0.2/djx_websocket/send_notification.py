from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class NotificationObj:

    def __init__(self, message):
        self.message_type = 'notification'
        self.message = message


class CRUDMessage:

    def __init__(self, object_id, object_type, action):
        self.data = {
            "data": {
                "id": object_id,
                "type": object_type,
                "action": action
            },
            "category": "crud"
        }


def send_notification(notification):
    """

    :param notification:
    :return:
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("notification_public",
                                            {
                                                'type': 'notification',  # notification.message_type,
                                                'message': CRUDMessage(object_id=1, object_type="obj",
                                                                       action="action").data
                                            })
