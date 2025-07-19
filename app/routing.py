from django.urls import path
from .consumers import OrderConsumer, ReadyOrders


websocket_urlpatterns = [
    path("ws/orders/", OrderConsumer.as_asgi()),
    path("ws/ready/orders/", ReadyOrders.as_asgi()),
]
