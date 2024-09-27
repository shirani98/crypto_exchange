from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.db.models import F
from django.core.exceptions import ValidationError


class User(AbstractUser):
    balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        default=0.0,
    )

    def __str__(self):
        return self.username

    @classmethod
    def decrease_balance(cls, user_id, amount):
        with transaction.atomic():
            updated = User.objects.filter(id=user_id, balance__gte=amount).update(
                balance=F("balance") - amount
            )
            if updated == 0:
                raise ValidationError(f"Insufficient balance.")

    @classmethod
    def increase_balance(cls, user_id, amount):
        with transaction.atomic():
            User.objects.filter(id=user_id).update(balance=F("balance") + amount)
