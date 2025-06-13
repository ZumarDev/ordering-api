from django.urls import path
from rest_framework.routers import DefaultRouter
from django.urls import include
from .views import (
    EmployeeView,
    FoodView,
    TableView,
    OrderingView,
    ChangeOrderView,
    GetAllOrders,
)

router = DefaultRouter()
router.register(r"foods", FoodView)
router.register(r"tables", TableView)
router.register(r"employees", EmployeeView),

urlpatterns = [
    path('order/', OrderingView.as_view()),
    path('change/order/<str:pk>/',ChangeOrderView.as_view()), 
    path('all/orders/',GetAllOrders.as_view()), 
    path("", include(router.urls)),
]
