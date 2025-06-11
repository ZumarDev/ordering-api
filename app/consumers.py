import json
from datetime import datetime, timedelta
from django.utils import timezone
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.groupname = 'orders'
        from .models import OrderedFood, Ordering
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name
)        
        await self.accept()
        
        data = await self.get_orders()
        await self.send(text_data=json.dumps({'orders':data}))
        
        
    @sync_to_async
    def get_orders(self):
        from .models import OrderedFood, Ordering

        orders = Ordering.objects.all()
        
        data = []
        for order in orders:
            
            deletion_time = order.ordered_time + timedelta(days=2)
            if timezone.now() > deletion_time:
                order.delete()
                continue
            
            ordered_foods = OrderedFood.objects.filter(order=order)
            foods = []
            for ordered_food in ordered_foods:
                foods.append({
                    'id': ordered_food.food.id,
                    'name': ordered_food.food.name,
                    'cost': ordered_food.food.cost,
                    'quantity': ordered_food.quantity,
                })
                
            data.append({
                "id": order.id,
                "table_number": order.table_number.id,
                "total_cost": order.cost,
                "ordered_time": order.ordered_time.strftime("%d-%m-%Y, %H:%M:%S"),
                "foods": foods,
            })
        return data
    
    async def send_new_order(self, event):
        data = await self.get_orders()
        await self.send(text_data=json.dumps({'orders': data}))
        
    async def send_order_updates(self, event):
        data = await self.get_orders()
        await self.send(text_data=json.dumps({'orders':data}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name,
        )
        
        
