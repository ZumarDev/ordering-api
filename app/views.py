from drf_spectacular.utils import extend_schema
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import (
    FoodSerializer,
    OrderRequestSerializer,
    OrderResponseSerializer,
    OrderSerializer,
    OrderUpdateSerializer,
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
        user = request.user
        order = Orders.objects.create(
            user=user,
            latitude=latitude,
            longitude=longitude,
            ordered_time=timezone.now(),
        )

        logger.info("creating new order")

        cost = 0

        for food_data in foods:
            food = get_object_or_404(Food, id=food_data["food_id"])
            quantity = food_data["quantity"]
            cost += food.cost * quantity

            OrderedFood.objects.create(order=order, food=food, quantity=quantity)

            logger.info("Order created with total cost %s", cost)

        order.cost = cost
        order.save()
        return Response(
            {"msg": "Order created successfully"}, status=status.HTTP_201_CREATED
        )


class OrderUpdateView(APIView):

    @extend_schema(
        request=OrderRequestSerializer,
        responses={201: OrderResponseSerializer},
    )
    def put(self, request, pk):
        try:
            order = Orders.objects.get(id=pk)
        except Orders.DoesNotExist:
            return Response({"msg": "Order does not found"})
        serializer = OrderUpdateSerializer(
            instance=order, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "Order is changed"})


class GetAllOrders(APIView):

    def get(self, request):
        orders = Orders.objects.all()
        serializer = OrderSerializer(orders, many=True).data
        return Response({"data": serializer})


class OrderDeleteView(APIView):

    def delete(self, request, pk):
        try:
            order = Orders.objects.get(id=pk)
            order.delete()
        except Orders.DoesNotExist:
            return Response({"msg": "No order in this id"})

        return Response({"msg": "Order deleted."})
