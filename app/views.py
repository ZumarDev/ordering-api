from datetime import datetime, timedelta
from drf_spectacular.utils import extend_schema
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    EmployeeSerializer,
    FoodSerializer,
    OrderOutputSerializer,
    OrderRequestSerializer,
    OrderResponseSerializer,
    TableSerializer,
    OrderItemSerializer
)
from .models import (
    Employee,
    Food,
    OrderedFood,
    Ordering,
    Table,
)

# Logging
import logging
logger = logging.getLogger('django')


class FoodView(viewsets.ModelViewSet):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()


class TableView(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class EmployeeView(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class OrderingView(APIView):
    
    @extend_schema(
        request=OrderRequestSerializer,
        responses={201: OrderResponseSerializer},
        description="Create a new order with table number and list of items"
    )
    
    def post(self, request):
        data = request.data
        logger.info('getting data from the request')
        foods = data.get("items", [])
        
        table_number = data.get("table_number")
        table = Table.objects.get(id=table_number)
        

        order = Ordering.objects.create(
            table_number=table,
            name=f"orderin_{table_number}",
            ordered_time=timezone.now(),
        )
        logger.info('creating new order')
        cost = 0

        for food_data in foods:
            food = Food.objects.get(id=food_data["food_id"])
            quantity = food_data["quantity"]
            cost += food.cost * quantity

            OrderedFood.objects.create(order=order, food=food, quantity=quantity)
            
            logger.info('Order created with total cost %s', cost )


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
            order = Ordering.objects.get(id=pk)
        except Ordering.DoesNotExist:
            return Response({'msg':'Order does not found'})
        ordered_foods = OrderedFood.objects.filter(order=order)
        
        data = request.data
        table_number = data.get('table_number')
        items = data.get('items', [])
        
        table = Table.objects.get(id=table_number)
        logger.info('getting table number')
        try:
            table = Table.objects.get(id=table_number)
        except Table.DoesNotExist:
            return Response({'msg':'Table does not found'})
        
        order.table_number = table
        order.ordered_time = timezone.now()
        order.name = order.name
        # Deleting old order
        for ordered_food in ordered_foods:
            ordered_food.delete()
        
        cost = 0 
        #Changing order
        for food_data in items:
            food = Food.objects.get(id=food_data['food_id'])
            print(food_data['food_id'])
            quantity = food_data['quantity']
            cost += food.cost * quantity
            OrderedFood.objects.create(order=order,food=food,quantity=quantity)
        order.cost = cost
        order.save()
        return Response({'msg':'Order is changed'})
            
        
        '''
class AllOrdersView(APIView):
    
    @extend_schema(
        responses={200: OrderOutputSerializer(many=True)},
    )
    def get(self, request):

        orders = Ordering.objects.all()
        
        data = []
        for order in orders:
            ordered_foods = OrderedFood.objects.filter(order=order)
            foods = []
            # Deletion
            deletion_time = order.ordered_time + timedelta(days=1)
            if deletion_time < timezone.now():
                order.delete()                
            else:
                for food in ordered_foods:
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
                        "table_number": order.table_number.id,
                        "total_cost": order.cost,
                        "ordered_time": order.ordered_time.strftime("%d-%m-%Y, %H:%M:%S"),
                        "foods": foods,
                    }
                )
        return Response(data, status=status.HTTP_200_OK)
'''