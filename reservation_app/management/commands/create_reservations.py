import random
from django.core.management.base import BaseCommand
from reservation_app.models import Reserve, Room
from customer.models import Customer
from datetime import datetime, timedelta
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Crea 10 reservas"

    def handle(self, *args, **kwargs):
        if Reserve.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Las reservas ya existen. No se añadieron nuevas reservas."
                )
            )
            return
        else:
            rooms = list(Room.objects.all())
            customers = list(Customer.objects.all())
            users = list(User.objects.all())  # Obtener todos los usuarios
            if not rooms or not customers or not users:
                self.stdout.write(
                    self.style.ERROR(
                        "No hay suficientes habitaciones, clientes o usuarios para crear reservas."
                    )
                )
                return

            reservations = []
            for i in range(10):
                customer = random.choice(customers)
                user = customer.user
                starting_date = datetime.now().date() + timedelta(days=random.randint(1, 30))
                nights = random.randint(1, 14)
                people = random.randint(1, 10)
                
                reserve = Reserve(
                    user=user, 
                    customer=customer,
                    starting_date=starting_date,
                    nights=nights,
                    end_date=starting_date + timedelta(days=nights),
                    people=people
                )
                reserve.save()
                
                reserve.assign_room()
                reserve.occupied_dates = reserve.compute_occupied_dates()
                reserve.calculate_price()
                reserve.save()
                
                reservations.append(reserve)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"Se han creado {len(reservations)} reservas exitosamente."
                )
            )