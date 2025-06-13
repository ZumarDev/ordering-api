from rest_framework import serializers
from .models import (
    Food,
    Employee,
    OrderedFood,
    Ordering,
    Table,
)


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = "__all__"


class TableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = "__all__"


class OrderItemSerializer(serializers.Serializer):
    food_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


class OrderRequestSerializer(serializers.Serializer):
    table_number = serializers.IntegerField()
    items = OrderItemSerializer(many=True)


class OrderResponseSerializer(serializers.Serializer):
    msg = serializers.CharField()


class FoodSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    cost = serializers.IntegerField()


class OrderSerializer(serializers.ModelSerializer):
    foods = serializers.SerializerMethodField("get_ordered_foods")

    class Meta:
        model = Ordering
        fields = ["id", "table_number", "cost", "ordered_time", "status", "foods"]

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
