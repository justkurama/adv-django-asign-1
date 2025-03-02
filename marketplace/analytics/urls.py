from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalyticsReportViewSet, ExportReportView

router = DefaultRouter()
router.register(r'analytics_reports', AnalyticsReportViewSet, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
    path('export/csv/', ExportReportView.as_view({'get': 'export_csv'}), name='export_csv'),
]
