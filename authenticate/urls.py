from django.urls import path
from .views import login_view, close_session, Register

urlpatterns = [
    path("", login_view, name="login"),
    path("close/", close_session, name="close_session"),
    path("register/", Register.as_view(), name="register"),
]
