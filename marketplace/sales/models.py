from django.db import models
from django.conf import settings
from products.models import Product

class SalesOrder(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('processed', 'Processed'), ('canceled', 'Canceled')]
    
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sales_orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def apply_discount(self):
        if self.discount:
            discount_amount = (self.discount.percentage / 100) * self.total_price
            return round(self.total_price - discount_amount, 2)
        return self.total_price

class Invoice(models.Model):
    order = models.OneToOneField(SalesOrder, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='invoices/', blank=True, null=True)

class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True)
    percentage = models.FloatField(help_text="Discount percentage (e.g., 10 for 10%)")
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return f"{self.code} - {self.percentage}%"


import paypalrestsdk
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE, 
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})

class Payment(models.Model):
    order = models.OneToOneField(SalesOrder, on_delete=models.CASCADE)
    paypal_payment_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed')])
    created_at = models.DateTimeField(auto_now_add=True)

    def create_paypal_payment(self):
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://127.0.0.1:8000/api/sales/payments/execute/",
                "cancel_url": "http://127.0.0.1:8000/api/sales/payments/cancel/",
            },
            "transactions": [{
                "amount": {"total": str(self.order.total_price), "currency": "USD"},
                "description": f"Payment for Order {self.order.id}",
            }],
        })

        if payment.create():
            self.paypal_payment_id = payment.id
            self.status = "pending"
            self.save()
            return payment["links"][1]["href"]  # Approval URL
        else:
            return None