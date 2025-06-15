from django.contrib import admin
from .models import Food, Table, Employee, Ordering, OrderedFood


class FoodAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'cost', 'time_to_prepare')
    search_fields = ('name',)
    
class OrderedFoodAdmin(admin.ModelAdmin):
    list_display = ('id','order','quantity')
    list_filter = ('quantity',)
    
class OrderingAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'name', 'cost')
    search_fields = ('name',)
    list_filter = ('table_number',)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('full_name',)
    list_filter = ('tables',)

class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'capacity')
    search_fields = ('id',)
    list_filter = ('capacity',)

admin.site.register(Food, FoodAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Ordering, OrderingAdmin)
admin.site.register(OrderedFood, OrderedFoodAdmin)