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
        fields = '__all__'
    
class TableSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Table
        fields = '__all__'
    
class EmployeeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Employee
        fields = '__all__'
        
class OrderItemSerializer(serializers.Serializer):
    food_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class OrderRequestSerializer(serializers.Serializer):
    table_number = serializers.IntegerField()
    items = OrderItemSerializer(many=True)
    
class OrderResponseSerializer(serializers.Serializer):
    msg = serializers.CharField()
        
class FoodOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    cost = serializers.IntegerField()
    quantity = serializers.IntegerField()
        
class OrderOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    table_number = serializers.IntegerField()
    total_cost = serializers.IntegerField()
    ordered_time = serializers.DateTimeField()
    foods = FoodOutputSerializer(many=True)