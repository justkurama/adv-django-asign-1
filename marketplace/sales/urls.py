from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesOrderViewSet, InvoiceViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'sales_orders', SalesOrderViewSet, basename='sales_order')
router.register(r'invoices', InvoiceViewSet, basename='invoice')

urlpatterns = [
    path('', include(router.urls)),
    path('payments/execute/', PaymentViewSet.as_view({'get': 'execute'}), name='execute_payment'),
]
