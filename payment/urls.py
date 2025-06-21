from django.urls import path
from .views import payment

urlpatterns = [
    path("payment/", payment, name="payment"),
]
