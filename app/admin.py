from django.contrib import admin
from .models import Food, OrderedFood, Orders


class FoodAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "cost", "time_to_prepare")
    search_fields = ("name",)


class OrderedFoodAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "quantity")
    list_filter = ("quantity",)


class OrderingAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "cost")
    search_fields = ("name",)






admin.site.register(Food, FoodAdmin)

admin.site.register(Orders, OrderingAdmin)
admin.site.register(OrderedFood, OrderedFoodAdmin)
