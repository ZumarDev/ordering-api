import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from user.models import Admin, Courier
from .models import IN_PROGERESS


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # user = self.scope["user"] TO DO

        # if not user.is_authenticated and not user.role in (Courier, Admin):
        #     await self.close()
        #     return

        self.groupname = "orders"
        await self.channel_layer.group_add(self.groupname, self.channel_name)
        await self.accept()
        data = await self.get_orders()

        await self.send(text_data=json.dumps({"orders": data}))

    # getting data from the request.
    async def receive(self, text_data):
        from .models import Orders

        data = json.loads(text_data)

        id = data.get("id")
        status = data.get("status")

        order = await sync_to_async(Orders.objects.get)(id=id)
        order.status = status
        await sync_to_async(order.save)()

    @sync_to_async
    def get_orders(self):
        from .models import OrderedFood, Orders

        orders = Orders.objects.filter(status=IN_PROGERESS)

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
                   # "user": order.user,
                    "total_cost": order.cost,
                    "status": order.status,
                    "latitude": order.latitude,
                    "longitude": order.longitude,
                    "ordered_time": order.ordered_time.strftime("%d-%m-%Y, %H:%M:%S"),
                    "foods": foods,
                }
            )
        return data

    # function for getting new orders
    async def send_new_order(self, event):
        data = await self.get_orders()
        await self.send(text_data=json.dumps({"orders": data}))

    # function for getting orders after changing
    async def send_order_updates(self, event):
        data = await self.get_orders()
        await self.send(text_data=json.dumps({"orders": data}))

    # function for getting orders after deleting
    async def get_order_after_deleting(self, event):
        data = await self.get_orders()
        await self.send(text_data=json.dumps({"orders": data}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name,
        )


class ReadyOrders(AsyncWebsocketConsumer):
    async def connect(self):
        # user = self.scope["user"] TO DO 

        # if not user.is_authenticated and not user.role == Courier:
        #     await self.close()
        #     return

        self.groupname = "ready_orders"
        await self.channel_layer.group_add(self.groupname, self.channel_name)
        await self.accept()

        data = await self.get_ready_orders()
        await self.send(text_data=json.dumps({"orders": data}))

    async def receive(self, text_data):
        from .models import Orders

        data = json.loads(text_data)

        id = data.get("id")
        status = data.get("status")

        order = await sync_to_async(Orders.objects.get)(id=id)
        order.status = status
        await sync_to_async(order.save)()

    @sync_to_async
    def get_ready_orders(self):
        from .models import Orders, OrderedFood

        ready_orders = Orders.objects.filter(status="done")
        data = []
        for order in ready_orders:
            foods = []

            foods = OrderedFood.objects.filter(order=order)
            for food in foods:
                foods.append(
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
                 #   "user": order.user,
                    "total_cost": order.cost,
                    "status": order.status,
                    "latitude": order.latitude,
                    "longitude": order.longitude,
                    "food": foods,
                }
            )

        return data

    # function for getting orders after changing
    async def send_order_updates(self, event):
        data = await self.get_ready_orders()
        await self.send(text_data=json.dumps({"orders": data}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name,
        )
