from django.db import models

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
    name = models.CharField(max_length=100, blank=True, null=True)
    cost = models.PositiveIntegerField(default=0)
    ordered_time = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=255)
    status = models.CharField(
        choices=STATUS_CHOICES, default="in_progress", max_length=50
    )

    class Meta:
        verbose_name = "Orders"

    def __str__(self):
        return f"{self.name if self.name else ''}"


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

    def __str__(self):
        return self.order.name
