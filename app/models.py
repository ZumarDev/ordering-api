from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=100)
    cost = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='media/food_images')
    
    def __str__(self):
        return self.name

class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    salary = models.PositiveIntegerField()
    
    def __str__(self):
        return self.full_name

class Table(models.Model):
    capacity = models.PositiveSmallIntegerField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='tables',blank=True, null=True)
    
    def __str__(self):
        return f"{self.id}"
    

class Ordering(models.Model):
    STATUS_CHOICES = (
        ('in_progress','in_progress'),
        ('done','done'),
        ('delivered','delivered')
    )
    table_number = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='table')
    name = models.CharField(max_length=100, blank=True, null=True)
    cost = models.PositiveIntegerField(default=0)
    ordered_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES,default='in_progress',max_length=50)    


    def __str__(self):
        return self.name 
    
class OrderedFood(models.Model):
    food = models.ForeignKey(Food,on_delete=models.CASCADE, related_name='ordered_foods',blank=True, null=True)
    order = models.ForeignKey(Ordering, on_delete=models.CASCADE, related_name='ordered_foods')
    quantity = models.PositiveSmallIntegerField()
    

    
    
    def __str__(self):
        return self.order.name
