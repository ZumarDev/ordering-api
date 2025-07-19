from rest_framework import serializers
from .models import (
    Food,
    OrderedFood,
    Orders
)


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = "__all__"



class OrderItemSerializer(serializers.Serializer):
    food_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


class OrderRequestSerializer(serializers.Serializer):
    items = OrderItemSerializer(many=True)


class OrderResponseSerializer(serializers.Serializer):
    msg = serializers.CharField()


class FoodSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    cost = serializers.IntegerField()
    image = serializers.ImageField()
    time_to_prepare = serializers.CharField()


class OrderSerializer(serializers.ModelSerializer):
    foods = serializers.SerializerMethodField("get_ordered_foods")

    class Meta:
        model = Orders
        fields = ["id", "cost", "ordered_time", "status", "foods"]

    def get_ordered_foods(self, obj):
        ordered_foods = OrderedFood.objects.filter(order=obj)
        foods = []
        for ordered_food in ordered_foods:
            foods.append(
                {
                    "id": ordered_food.food.id,
                    "name": ordered_food.food.name,
                    "cost": ordered_food.food.cost,
                }
            )
        return foods
