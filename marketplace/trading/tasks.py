from celery import shared_task
from .models import Order, Transaction, SalesOrder
from django.utils.timezone import now

@shared_task
def process_orders():
    buy_orders = Order.objects.filter(order_type='buy', status='pending').order_by('-price')
    sell_orders = Order.objects.filter(order_type='sell', status='pending').order_by('price')

    for buy in buy_orders:
        for sell in sell_orders:
            if buy.price >= sell.price and buy.quantity == sell.quantity:
                buy.status = 'completed'
                sell.status = 'completed'

                Transaction.objects.create(
                    order=buy,
                    total_amount=buy.quantity * buy.price,
                    executed_at=now()
                )

                Transaction.objects.create(
                    order=sell,
                    total_amount=sell.quantity * sell.price,
                    executed_at=now()
                )

                buy.save()
                sell.save()
                break  # Move to next buy order

@shared_task
def process_pending_orders():
    orders = SalesOrder.objects.filter(status='pending')
    for order in orders:
        order.status = 'processed'
        order.save()
    return f"{orders.count()} orders processed"

@shared_task
def generate_sales_report():
    total_orders = SalesOrder.objects.filter(status='processed').count()
    return f"Total Processed Orders: {total_orders}"