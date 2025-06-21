"""
Reserve e Image 
"""

from datetime import timedelta

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

from room.models import Room

# Create your models here.


class Reserve(models.Model):
    """
    Modelo que representa una reserva.

    Atributos:
        user (ForeignKey): Usuario que realiza la reserva.
        customer (ForeignKey): Cliente que será hospedado.
        starting_date (DateField): Fecha de inicio de la reserva.
        nights (IntegerField): Número de noches de la reserva.
        end_date (DateField): Fecha de finalización de la reserva.
        people (IntegerField): Número de personas en la reserva.
        rooms (ManyToManyField): Habitaciones reservadas.
        price (FloatField): Precio total de la reserva.
        images (ManyToManyField): Imágenes asociadas a la reserva.
        paid (BooleanField): Indica si la reserva ha sido pagada.
        occupied_dates (ArrayField): Fechas ocupadas por la reserva.

    Métodos:
        assign_room(): Asigna habitaciones a la reserva según la capacidad requerida.
        compute_occupied_dates(): Calcula las fechas ocupadas por la reserva.
        find_free_rooms(): Encuentra habitaciones libres para las fechas de la reserva.
        calculate_price(): Calcula el precio total de la reserva.
        __str__(): Representación en cadena de la reserva.
    """
        

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey("customer.Customer", on_delete=models.CASCADE)
    starting_date = models.DateField()
    nights = models.IntegerField()
    end_date = models.DateField()
    people = models.IntegerField()
    rooms = models.ManyToManyField(Room)
    price = models.FloatField(default=0)
    images = models.ManyToManyField(
        "Image", related_name="image_set", max_length=people
    )
    paid = models.BooleanField(default=False)
    occupied_dates = ArrayField(models.DateField(), blank=True, default=list)

    def assign_room(self):
        """
        Asigna habitaciones a la reserva según la capacidad requerida.

        Este método busca habitaciones libres y las asigna a la reserva
        según la cantidad de personas. Si hay una habitación con la capacidad
        exacta, se asigna directamente. De lo contrario, se asignan varias
        habitaciones hasta cubrir la capacidad requerida.
        """
        people = self.people
        while people > 0:
            free_rooms = Reserve.find_free_rooms(self)
            if Room.objects.filter(capacity=people).exists():
                room = Room.objects.filter(capacity=people).first()
                room.reserve_dates(self)
                room.save()
                self.rooms.add(room)
                people -= room.capacity
            else:
                capacities = {room.id: room.capacity for room in free_rooms}
                for room_id, capacity in capacities.items():
                    room = Room.objects.get(id=room_id)
                    room.reserve_dates(self)
                    room.save()
                    self.rooms.add(room)
                    people -= capacity
                    if people <= 0:
                        break
            self.save()

    def compute_occupied_dates(self):
        """
        Calcula las fechas ocupadas por la reserva.

        Este método genera una lista de fechas ocupadas desde la fecha de inicio
        hasta el final de la reserva, basándose en el número de noches.
        
        Returns:
            list: Lista de fechas ocupadas.
        """
        occupied_dates = []
        for i in range(self.nights):
            occupied_dates.append(self.starting_date + timedelta(days=i))
        return occupied_dates

    def find_free_rooms(self):
        """
        Encuentra habitaciones libres para las fechas de la reserva.

        Este método busca todas las habitaciones y filtra aquellas que no
        tienen intersección con las fechas ocupadas de la reserva.
        
        Returns:
            list: Lista de habitaciones libres.
        """
        rooms = Room.objects.all()
        free_rooms = []
        for room in rooms:
            if not set(self.occupied_dates).intersection(set(room.occupied_dates)):
                free_rooms.append(room)
        return free_rooms

    def calculate_price(self):
        """
        Calcula el precio total de la reserva.

        Este método suma el precio de todas las habitaciones reservadas
        multiplicado por el número de noches.
        """
        price = 0
        rooms = self.rooms.all()
        for room in rooms:
            price += room.price * self.nights
        self.price = price

    def __str__(self):
        return f"{self.customer} - {self.starting_date}"


class Image(models.Model):
    """
    Modelo que representa el documento de identidad de un huésped.

    Atributos:
        image (ImageField): Archivo de imagen.
        reserve (ForeignKey): Reserva a la que pertenece la imagen.
    """
    image = models.ImageField(upload_to="images")
    reserve = models.ForeignKey(Reserve, on_delete=models.CASCADE)
