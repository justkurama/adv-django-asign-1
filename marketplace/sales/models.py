from django.db import models
from django.conf import settings
from products.models import Product

class SalesOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('processed', 'Processed'),
        ('canceled', 'Canceled'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sales_orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer.username}"

class Invoice(models.Model):
    order = models.OneToOneField(SalesOrder, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='invoices/', blank=True, null=True)

    def __str__(self):
        return f"Invoice for Order {self.order.id}"

class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True)
    percentage = models.FloatField(help_text="Discount percentage (e.g., 10 for 10%)")
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return f"Discount {self.code} - {self.percentage}%"
