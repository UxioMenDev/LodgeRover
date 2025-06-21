import random
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
            users = [
                User.objects.create_user(
                    username=f"user{i}",
                    password="password"
                )
                for i in range(1, 9)
            ]
            customers = [
                Customer(
                    user=user,
                    name=f"Customer {i}",
                    last_name=f"LastName {i}",
                    email=f"customer{i}@example.com",
                    phone=f"123456789{i}",
                    address=f"Address {i}",
                    card_number=f"123456781234567{i}"
                )
                for i, user in enumerate(users, start=1)
            ]
            Customer.objects.bulk_create(customers)
            self.stdout.write(self.style.SUCCESS("Clientes creados con éxito"))