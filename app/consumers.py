import json
from datetime import datetime, timedelta
from django.utils import timezone
from .models import OrderedFood, Ordering
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        await self.send(text_data=json.dumps({
            'msg':'connected to websocket'
        }))