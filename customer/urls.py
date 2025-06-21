from django.urls import path
from .views import create_customer, show_customers, delete_customer, update_customer

urlpatterns = [
    path("create/", create_customer, name="create_customer"),
    path("show/", show_customers, name="show_customers"),
    path("delete/<int:id>", delete_customer, name="delete_customer"),
    path("update/<int:id>", update_customer, name="update_customer"),
]
