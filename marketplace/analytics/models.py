from django.db import models
from trading.models import Transaction
from sales.models import SalesOrder
from django.utils.timezone import now

class AnalyticsReport(models.Model):
    REPORT_TYPES = [
        ('trading', 'Trading Volume'),
        ('sales', 'Sales Revenue'),
        ('profit_loss', 'Profit/Loss'),
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    generated_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()  # Store reports in JSON format

    def __str__(self):
        return f"{self.report_type} Report - {self.generated_at.strftime('%Y-%m-%d %H:%M')}"
