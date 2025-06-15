from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path("ws/orders/", consumers.OrderConsumer.as_asgi()),
    path("ws/ready/orders/", consumers.ReadyOrdersConsumer.as_asgi()),
]
