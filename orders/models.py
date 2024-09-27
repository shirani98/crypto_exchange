from django.db import models
from .tasks import buy_from_exchange_task
from django.db import transaction


class Order(models.Model):
    PENDING = "P"
    INPROGRESS = "I"
    SUCCESS = "S"
    FAILED = "F"
    CANCELED = "C"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (INPROGRESS, "In Progress"),
        (SUCCESS, "Success"),
        (FAILED, "Failed"),
        (CANCELED, "Canceled"),
    ]

    symbol = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.symbol} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        if self._state.adding:
            super().save(*args, **kwargs)
            return transaction.on_commit(lambda: buy_from_exchange_task.delay(self.id))

        return super().save(*args, **kwargs)

    @staticmethod
    def get_order_price(symbol, amount):
        # Hardcode order price calculator
        if symbol == "ABAN":
            return amount * 4
