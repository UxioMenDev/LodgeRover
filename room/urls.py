from django.urls import path
from .views import show_rooms

urlpatterns = [
    path("show/", show_rooms, name="show_rooms"),
]
