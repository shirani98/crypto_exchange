from django.urls import path
from .views import IncreaseBalanceView

urlpatterns = [
    path(
        "<int:user_id>/increase-balance/",
        IncreaseBalanceView.as_view(),
        name="increase-balance",
    ),
]
