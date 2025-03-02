from rest_framework import viewsets
from rest_framework.response import Response
from .models import AnalyticsReport
from .serializers import AnalyticsReportSerializer
from trading.models import Transaction
from sales.models import SalesOrder
from django.utils.timezone import now
from django.http import HttpResponse
from django.db.models import Sum
import csv

class AnalyticsReportViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsReport.objects.all().order_by('-generated_at')
    serializer_class = AnalyticsReportSerializer

    def generate_trading_volume(self):
        total_trades = Transaction.objects.count()
        total_amount = Transaction.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        return {"total_trades": total_trades, "total_amount": float(total_amount)}

    def generate_sales_revenue(self):
        total_sales = SalesOrder.objects.count()
        total_revenue = SalesOrder.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
        return {"total_sales": total_sales, "total_revenue": float(total_revenue)}

    def generate_profit_loss(self):
        revenue = self.generate_sales_revenue()["total_revenue"]
        expenses = Transaction.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        profit_loss = revenue - expenses
        return {"revenue": float(revenue), "expenses": float(expenses), "profit_loss": float(profit_loss)}

    def create(self, request, *args, **kwargs):
        report_type = request.data.get("report_type")

        if report_type == "trading":
            data = self.generate_trading_volume()
        elif report_type == "sales":
            data = self.generate_sales_revenue()
        elif report_type == "profit_loss":
            data = self.generate_profit_loss()
        else:
            return Response({"error": "Invalid report type"}, status=400)

        report = AnalyticsReport.objects.create(report_type=report_type, data=data)
        return Response(AnalyticsReportSerializer(report).data)
    
class ExportReportView(viewsets.ViewSet):
    def export_csv(self, request, *args, **kwargs):
        reports = AnalyticsReport.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="analytics_reports.csv"'
        writer = csv.writer(response)
        writer.writerow(['Report Type', 'Generated At', 'Data'])

        for report in reports:
            writer.writerow([report.report_type, report.generated_at, report.data])

        return response