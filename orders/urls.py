from django.urls import path
from .views import SubmitOrderView

urlpatterns = [
    path("submit/<int:user_id>/", SubmitOrderView.as_view(), name="submit-order"),
]
