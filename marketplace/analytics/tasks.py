from celery import shared_task
from .models import AnalyticsReport
from .views import AnalyticsReportViewSet

@shared_task
def generate_daily_reports():
    view = AnalyticsReportViewSet()
    
    trading_data = view.generate_trading_volume()
    sales_data = view.generate_sales_revenue()
    profit_loss_data = view.generate_profit_loss()

    AnalyticsReport.objects.create(report_type="trading", data=trading_data)
    AnalyticsReport.objects.create(report_type="sales", data=sales_data)
    AnalyticsReport.objects.create(report_type="profit_loss", data=profit_loss_data)

    return "Daily Analytics Reports Generated!"
