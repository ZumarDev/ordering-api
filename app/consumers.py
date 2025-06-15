import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class OrderConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.groupname = "orders"
        await self.channel_layer.group_add(self.groupname, self.channel_name)
        await self.accept()
        data = await self.get_orders()

        await self.send(text_data=json.dumps({"orders": data}))

    # getting data from the request.
    async def receive(self, text_data):
        from .models import Ordering

        data = json.loads(text_data)

        id = data.get("id")
        status = data.get("status")

        order = await sync_to_async(Ordering.objects.get)(id=id)
        order.status = status
        await sync_to_async(order.save)()

    @sync_to_async
    def get_orders(self):
        from .models import OrderedFood, Ordering

        orders = Ordering.objects.all().exclude(status="delivered")

        data = []
        for order in orders:
            ordered_foods = OrderedFood.objects.filter(order=order)
            foods = []
            for ordered_food in ordered_foods:
                foods.append(
                    {
                        "id": ordered_food.food.id,
                        "name": ordered_food.food.name,
                        "cost": ordered_food.food.cost,
                        "quantity": ordered_food.quantity,
                    }
                )

            data.append(
                {
                    "id": order.id,
                    "table_number": order.table_number.table_number,
                    "total_cost": order.cost,
                    "status": order.status,
                    "ordered_time": order.ordered_time.strftime("%d-%m-%Y, %H:%M:%S"),
                    "foods": foods,
                }
            )
        return data

    # function for getting orders with new ones
    async def send_new_order(self, event):
        data = await self.get_orders()
        await self.send(text_data=json.dumps({"orders": data}))

    # function for getting orders with updates
    async def send_order_updates(self, event):
        data = await self.get_orders()
        await self.send(text_data=json.dumps({"orders": data}))

    async def get_order_after_deleting(self, event):
        data = await self.get_orders()
        await self.send(text_data=json.dumps({"orders": data}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name,
        )


class ReadyOrdersConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.groupname = "ready_orders"
        await self.channel_layer.group_add(self.groupname, self.channel_name)
        await self.accept()

        data = await self.get_ready_orders()
        await self.send(text_data=json.dumps({"orders": data}))

    async def receive(self, text_data):
        from .models import Ordering

        data = json.loads(text_data)

        id = data.get("id")
        status = data.get("status")

        order = await sync_to_async(Ordering.objects.get)(id=id)
        order.status = status
        await sync_to_async(order.save)()

    @sync_to_async
    def get_ready_orders(self):
        from .models import Ordering, OrderedFood

        ready_orders = Ordering.objects.filter(status="done")
        data = []
        for order in ready_orders:
            ordered_foods = []
            
            foods = OrderedFood.objects.filter(order=order)
            for food in foods:
                ordered_foods.append(
                    {
                        "id": food.food.id,
                        "name": food.food.name,
                        "cost": food.food.cost,
                        "quantity": food.quantity,
                    }
                )
            data.append(
                {
                    "id": order.id,
                    "table_number": order.table_number.table_number,
                    "total_cost": order.cost,
                    "status": order.status,
                }
            )

        return data

    async def send_order_updates(self, event):
        data = await self.get_ready_orders()
        await self.send(text_data=json.dumps({"orders": data}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name,
        )
