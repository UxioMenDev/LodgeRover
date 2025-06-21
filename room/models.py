"""
Room
"""

from datetime import timedelta

from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.


class Room(models.Model):
    """
    Modelo que representa una habitación en el sistema de reservas.

    Atributos:
        number (int): Número único de la habitación.
        description (str): Descripción de la habitación (opcional).
        price (float): Precio por noche de la habitación.
        capacity (int): Capacidad máxima de personas en la habitación (por defecto 2).
        photo (ImageField): Foto de la habitación (opcional, por defecto "rooms/default.jpg").
        reservations (ManyToManyField): Relación con el modelo Reserve, representa las reservas asociadas a la habitación.
        occupied_dates (ArrayField): Lista de fechas ocupadas para la habitación.

    Métodos:
        reserve_dates(reservation): Añade las fechas de una reserva a la lista de fechas ocupadas.
    """
    number = models.IntegerField(unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    capacity = models.IntegerField(default=2)
    photo = models.ImageField(
        upload_to="rooms", null=True, blank=True, default="rooms/default.jpg"
    )
    reservations = models.ManyToManyField("reservation_app.Reserve", blank=True)
    occupied_dates = ArrayField(models.DateField(), blank=True, default=list)

    def reserve_dates(self, reservation):
        """
        Añade las fechas de una reserva a la lista de fechas ocupadas.

        Args:
            reservation (Reserve): Objeto de reserva que contiene la fecha de inicio y el número de noches.
        """
        for i in range(reservation.nights):
            self.occupied_dates.append(reservation.starting_date + timedelta(days=i))
        self.save()
        
    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def __str__(self):
        return str(self.number)
