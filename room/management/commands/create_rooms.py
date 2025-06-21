import random
from django.core.management.base import BaseCommand
from reservation_app.models import Room


class Command(BaseCommand):
    help = "Crea 10 alojamientos"

    def handle(self, *args, **kwargs):
        if Room.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Los alojamientos ya existen. No se añadieron nuevos alojamientos."
                )
            )
            return
        else:
            rooms = [
                Room(
                    number=i,
                    description=f"Alojamiento {i}",
                    price=random.randint(20, 100),
                    capacity=random.randint(2, 4),
                )
                for i in range(1, 11)
            ]
            Room.objects.bulk_create(rooms)
            self.stdout.write(self.style.SUCCESS("Alojamientos creados con éxito"))
