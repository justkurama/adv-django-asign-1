from rest_framework import viewsets
from .models import SalesOrder, Invoice, Discount
from .serializers import SalesOrderSerializer, InvoiceSerializer, DiscountSerializer
from rest_framework.permissions import IsAuthenticated

class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated]

class InvoiceViewSet(viewsets.ModelViewSet): 
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
