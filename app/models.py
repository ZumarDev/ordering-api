from django.db import models
from user.models import User

IN_PROGERESS, DONE, DELIVERED = "IN_PROGERESS", "DONE", "DELIVERED"


class Food(models.Model):
    name = models.CharField(max_length=100)
    cost = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to="food_images/")
    time_to_prepare = models.CharField(default="10-15", help_text="in minutes")

    def __str__(self):
        return self.name


class Orders(models.Model):
    STATUS_CHOICES = (
        (IN_PROGERESS, IN_PROGERESS),
        (DONE, DONE),
        (DELIVERED, DELIVERED),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    cost = models.PositiveIntegerField(default=0)
    ordered_time = models.DateTimeField(blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(
        choices=STATUS_CHOICES, default=IN_PROGERESS, max_length=50
    )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"{self.id}"


class OrderedFood(models.Model):
    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE,
        related_name="ordered_foods",
        blank=True,
        null=True,
    )
    order = models.ForeignKey(
        Orders, on_delete=models.CASCADE, related_name="ordered_foods"
    )
    quantity = models.PositiveSmallIntegerField()
