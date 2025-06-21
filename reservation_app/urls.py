from django.urls import path, register_converter
from . import converters
from .views import (
    create_reservation,
    show_reservations,
    update_reservation,
    delete_reservation,
    upload_images,
    select_room,
    change_room,
    welcome
)

register_converter(converters.DateConverter, "date")


urlpatterns = [
    path("create/", create_reservation, name="create_reservation"),
    path("show/", show_reservations, name="show_reservations"),
    path("update/<int:id>/", update_reservation, name="update_reservation"),
    path("delete/<int:id>/", delete_reservation, name="delete_reservation"),
    path("upload/<int:id>/", upload_images, name="upload_images"),
    path(
        "create/<int:room>/<date:date>",
        create_reservation,
        name="create_reservation_with_room",
    ),
    path("select/<int:reservation_id>/<int:room_id>", select_room, name="select_room"),
    path(
        "change/<int:reservation_id>/<int:old_room_id>/<int:room_id>/",
        change_room,
        name="change_room",
    ),
    path('', welcome, name='welcome'),

]
