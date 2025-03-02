from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesOrderViewSet, InvoiceViewSet

router = DefaultRouter()
router.register(r'sales_orders', SalesOrderViewSet, basename='sales_order')
router.register(r'invoices', InvoiceViewSet, basename='invoice')

urlpatterns = [
    path('', include(router.urls)),
]
