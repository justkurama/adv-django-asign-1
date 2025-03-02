import pdfkit
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import SalesOrder, Invoice, Discount, Payment
from .serializers import SalesOrderSerializer, InvoiceSerializer, DiscountSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
import paypalrestsdk
from rest_framework.response import Response

class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        order = serializer.save(customer=self.request.user)
        order.total_price = order.apply_discount()
        order.save()

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def generate_invoice(self, order):
        html = render_to_string("invoice_template.html", {"order": order})
        pdf_path = f"media/invoices/invoice_{order.id}.pdf"
        pdfkit.from_string(html, pdf_path)
        return pdf_path

    def create(self, request, *args, **kwargs):
        order = SalesOrder.objects.get(id=request.data["order"])
        pdf_path = self.generate_invoice(order)
        invoice = Invoice.objects.create(order=order, pdf_file=pdf_path)
        return HttpResponse(f"Invoice generated at {invoice.pdf_file}")
    
class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        order_id = request.data.get("order_id")
        order = SalesOrder.objects.get(id=order_id)

        payment = Payment.objects.create(order=order, status="pending")
        approval_url = payment.create_paypal_payment()

        if approval_url:
            return Response({"approval_url": approval_url, "payment_id": payment.id})
        return Response({"error": "Payment creation failed"}, status=400)

    def execute(self, request):
        payment_id = request.query_params.get("paymentId")
        payer_id = request.query_params.get("PayerID")

        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            payment_obj = Payment.objects.get(paypal_payment_id=payment_id)
            payment_obj.status = "paid"
            payment_obj.save()
            return Response({"message": "Payment successful!"})
        return Response({"error": "Payment execution failed"}, status=400)
