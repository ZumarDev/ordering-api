from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Ordering
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# signal for new order


@receiver(post_save, sender=Ordering)
def get_new_orders(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "orders",
            {"type": "send_new_order", "message": "new order"},
        )


# signal for order updates


@receiver(post_save, sender=Ordering)
def get_updates_orders(sender, instance, created, **kwargs):
    if created == False:
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "orders",
            {
                "type": "send_order_updates",
                "message": "updated order",
            },
        )

        async_to_sync(channel_layer.group_send)(
            "ready_orders",
            {
                "type": "send_order_updates",
                "message": "updated order",
            },
        )


@receiver(post_delete, sender=Ordering)
def get_order_after_deleting(sender, instance, **kwargs):

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "orders",
        {
            "type": "get_order_after_deleting",
            "message": "order deleted",
        },
    )
