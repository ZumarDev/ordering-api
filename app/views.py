from drf_spectacular.utils import extend_schema
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    FoodSerializer,
    OrderRequestSerializer,
    OrderResponseSerializer,
    OrderSerializer,
)
from .models import (
    Food,
    OrderedFood,
    Orders,
)

# Logging
import logging

logger = logging.getLogger("django")


class MenuView(APIView):
    def get(self, request):
        foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True).data
        return Response(serializer)


class OrderingView(APIView):

    @extend_schema(
        request=OrderRequestSerializer,
        responses={201: OrderResponseSerializer},
        description="Create a new order with list of items",
    )
    def post(self, request):
        data = request.data
        logger.info("getting data from the request")
        foods = data.get("items", [])
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        order = Orders.objects.create(
            latitude=latitude,
            longitude=longitude,
            ordered_time=timezone.now(),
        )
        
        logger.info("creating new order")
        
        cost = 0

        for food_data in foods:
            food = Food.objects.get(id=food_data["food_id"])
            quantity = food_data["quantity"]
            cost += food.cost * quantity

            OrderedFood.objects.create(order=order, food=food, quantity=quantity)

            logger.info("Order created with total cost %s", cost)

        order.cost = cost
        order.save()
        return Response(
            {"msg": "Order created successfully"}, status=status.HTTP_201_CREATED
        )


class ChangeOrderView(APIView):

    @extend_schema(
        request=OrderRequestSerializer,
        responses={201: OrderResponseSerializer},
    )
    def patch(self, request, pk):
        try:
            order = Orders.objects.get(id=pk)
        except Orders.DoesNotExist:
            return Response({"msg": "Order does not found"})
        ordered_foods = OrderedFood.objects.filter(order=order)

        data = request.data

        items = data.get("items", [])

        order.ordered_time = timezone.now()
        order.name = order.name
        # Deleting old order
        for ordered_food in ordered_foods:
            ordered_food.delete()

        cost = 0
        # Changing order
        for food_data in items:
            food = Food.objects.get(id=food_data["food_id"])
            print(food_data["food_id"])
            quantity = food_data["quantity"]
            cost += food.cost * quantity
            OrderedFood.objects.create(order=order, food=food, quantity=quantity)
        order.cost = cost
        order.save()
        return Response({"msg": "Order is changed"})


class GetAllOrders(APIView):

    def get(self, request):
        orders = Orders.objects.all()
        serializer = OrderSerializer(orders, many=True).data
        return Response({"data": serializer})


class DeleteOrderView(APIView):

    def delete(self, request, pk):
        try:
            order = Orders.objects.get(id=pk)
            order.delete()
        except Orders.DoesNotExist:
            return Response({"msg": "No order in this id"})

        return Response({"msg": "Order deleted."})
