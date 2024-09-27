from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("symbol", "amount")

    def validate(self, data):
        if data["amount"] <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return data
