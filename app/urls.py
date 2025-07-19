from django.urls import path
from django.conf.urls.static import static
from config import settings
from .views import (
    OrderingView,
    ChangeOrderView,
    GetAllOrders,
    DeleteOrderView,
    MenuView,
)

urlpatterns = [
    path("order/food/", OrderingView.as_view()),
    path("update/order/<str:pk>/", ChangeOrderView.as_view()),
    path("orders/", GetAllOrders.as_view()),
    path("delete/order/<str:pk>/", DeleteOrderView.as_view()),
    path("foods/", MenuView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
