from django.urls import path
from .views import (
    OrderingView,
    ChangeOrderView,
    GetAllOrders,
    DeleteOrderView,
    MenuView,
)

urlpatterns = [
    path('order/', OrderingView.as_view()),
    path('update/order/<str:pk>/', ChangeOrderView.as_view()), 
    path('all/orders/', GetAllOrders.as_view()), 
    path('delete/order/<str:pk>/', DeleteOrderView.as_view()),
    path('foods/', MenuView.as_view()),
]


