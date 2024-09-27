from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from users.models import User
from .serializers import BalanceUpdateSerializer
from django.core.exceptions import ValidationError


class IncreaseBalanceView(APIView):

    def post(self, request, user_id):
        serializer = BalanceUpdateSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data["amount"]
            user = get_object_or_404(User, id=user_id)

            try:
                User.increase_balance(user_id, amount)
                return Response(
                    {"message": "Balance increased successfully."},
                    status=status.HTTP_200_OK,
                )
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
