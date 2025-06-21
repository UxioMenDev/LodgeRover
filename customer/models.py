'''
Customer
'''

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

# Create your models here.


class Customer(models.Model):
    """
    Modelo que representa a un cliente.

    Atributos:
        user (User): Relación uno a uno con el modelo User de Django.
        name (str): Nombre del cliente, con un máximo de 50 caracteres.
        last_name (str): Apellido del cliente, con un máximo de 50 caracteres.
        email (str): Correo electrónico del cliente.
        phone (str): Número de teléfono del cliente, con un máximo de 10 caracteres.
        address (str): Dirección del cliente, con un máximo de 100 caracteres.
        card_number (str): Número de tarjeta del cliente, con un máximo de 16 caracteres.
    """  

    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para agregar una verificación de permisos.

        Si el cliente ya existe y el usuario que intenta modificarlo no es el mismo
        que el usuario original y no es un usuario con permisos de staff, se lanza
        una excepción PermissionDenied.

        Args:
            *args: Argumentos posicionales.
            **kwargs: Argumentos de palabra clave.
        """
        if self.pk is not None:
            original = Customer.objects.get(pk=self.pk)
            if self.user != original.user and not self.user.is_staff:
                raise PermissionDenied("No tienes permiso para modificar este cliente.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.last_name}"
