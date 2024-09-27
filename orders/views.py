from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order
from .serializers import OrderSerializer
from users.models import User


class SubmitOrderView(APIView):

    def post(self, request, user_id):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order_value = Order.get_order_price(
                serializer.validated_data["symbol"], serializer.validated_data["amount"]
            )
            try:
                User.decrease_balance(user_id, order_value)
                order = serializer.save()
                return Response(
                    {
                        "message": "Order submitted successfully.",
                        "order_id": order.id,
                        "status": order.status,
                        "created_at": order.created_at,
                    },
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
