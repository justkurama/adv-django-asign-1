from django.db import models
from django.conf import settings

class Order(models.Model):
    ORDER_TYPES = [('buy', 'Buy'), ('sell', 'Sell')]
    STATUS_CHOICES = [('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    order_type = models.CharField(max_length=10, choices=ORDER_TYPES)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_type} {self.quantity} at {self.price}"

class Transaction(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    executed_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Transaction for Order {self.order.id} at {self.executed_at}"
