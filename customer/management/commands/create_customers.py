import requests
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from customer.models import Customer

class Command(BaseCommand):
    help = "Crea 10 clientes"

    def handle(self, *args, **kwargs):
        if Customer.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Los clientes ya existen. No se añadieron nuevos clientes."
                )
            )
            return
        else:
            # Obtener datos de la API
            response = requests.get('https://api.generadordni.es/profiles/person')
            api_data = response.json()            
            users = [
                User.objects.create_user(
                    username=f"{api_data[i-1].get('nombre_usuario')}",
                    password="abc123."
                )
                for i in range(0, 10)
            ]
            customers = [
                Customer(
                    user=user,
                    name=api_data[i-1].get('nombre'),
                    last_name=f"{api_data[i-1].get('apellido1')} {api_data[i-1].get('apellido2')}",
                    email=api_data[i-1].get('email'),
                    phone=api_data[i-1].get('telefono'),
                    address=f"{api_data[i-1].get('direccion')} {api_data[i-1].get('numero_via')} {api_data[i-1].get('codigo_postal')} {api_data[i-1].get('municipio')} {api_data[i-1].get('provincia')}",
                    card_number=api_data[i-1].get('tarjeta')
                )
                for i, user in enumerate(users, start=1)
            ]
            Customer.objects.bulk_create(customers)
            self.stdout.write(self.style.SUCCESS("Clientes creados con éxito"))