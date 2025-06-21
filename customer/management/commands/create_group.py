from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from reservation_app.models import Reserve
from customer.models import Customer

class Command(BaseCommand):
    help = 'Crea el grupo "Customers" y asigna los permisos necesarios'

    def handle(self, *args, **kwargs):
        # Crear el grupo 'customers'
        group, created = Group.objects.get_or_create(name="Customers")

        # Obtener los ContentTypes para los modelos Reserva y Cliente
        reservation_content_type = ContentType.objects.get_for_model(Reserve)
        customers_content_type = ContentType.objects.get_for_model(Customer)

        # Obtener los permisos necesarios
        reserve_permissions = Permission.objects.filter(
            content_type=reservation_content_type,
            codename__in=["add_reserve", "change_reserve", "delete_reserve", "view_reserve"],
        )
        customer_permissions = Permission.objects.filter(
            content_type=customers_content_type, codename__in=["change_customer"]
        )

        # Asignar los permisos al grupo
        group.permissions.set(list(reserve_permissions) + list(customer_permissions))

        self.stdout.write(self.style.SUCCESS(f'Grupo "{group.name}" creado y permisos asignados.'))
