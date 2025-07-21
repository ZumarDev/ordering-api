from rest_framework import serializers
from .models import Food, OrderedFood, Orders
from django.utils import timezone


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


class OrderItemSerializer(serializers.Serializer):
    food_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


class OrderUpdateSerializer(serializers.Serializer):
    items = OrderItemSerializer(many=True)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    def update(self, instance, validated_data):
        items = validated_data.get("items")
        latitude = validated_data.get("latitude")
        longitude = validated_data.get("longitude")
        request = self.context.get("request")
        OrderedFood.objects.filter(order=instance).delete()
        cost = 0
        for item in items:
            food = Food.objects.get(id=item["food_id"])
            quantity = item["quantity"]
            cost += food.cost * quantity
            OrderedFood.objects.create(food=food, quantity=quantity, order=instance)

        instance.cost = cost
        instance.user = request.user
        instance.ordered_time = timezone.now()
        instance.latitude = latitude
        instance.longitude = longitude

        instance.save()

        return instance
