from celery import shared_task
import requests
from django.db.models import Sum
from django.apps import apps
from django.db import transaction


@shared_task
def buy_from_exchange_task(order_id):
    Order = apps.get_model("orders", "Order")
    order = Order.objects.get(id=order_id)
    order_value = Order.get_order_price(order.symbol, order.amount)

    if order_value >= 10 and order.status == Order.PENDING:
        orders_to_update = Order.objects.filter(id__in=[order.id])
        total_value = order_value
    else:
        with transaction.atomic():
            small_orders = Order.objects.select_for_update().filter(
                symbol=order.symbol, status=Order.PENDING, amount__lt=10
            )
            orders_amount = small_orders.aggregate(total=Sum("amount"))["total"] or 0
            total_value = Order.get_order_price(order.symbol, orders_amount)

            if total_value > 10:
                orders_to_update = list(small_orders)
                small_orders.update(status=Order.INPROGRESS)
            else:
                return
    try:
        response = requests.post(
            "https://exchange.com/api/buy",
            json={"crypto_name": order.symbol, "total_value": str(total_value)},
        )

        new_status = Order.SUCCESS if response.status_code == 200 else Order.FAILED
    except requests.exceptions.RequestException as e:
        new_status = Order.FAILED

    for order in orders_to_update:
        order.status = new_status
    Order.objects.bulk_update(orders_to_update, ["status"])
