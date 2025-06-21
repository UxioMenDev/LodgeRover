from django.contrib.auth.models import Permission, User
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse

from .models import Customer


class CustomerModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1')
        self.user2 = User.objects.create_user(username='user2')
        self.staff_user = User.objects.create_user(username='staff', is_staff=True)
        
        self.customer = Customer.objects.create(
            user=self.user1,
            name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            address='123 Street',
            card_number='1234567890123456'
        )

    def test_non_staff_cannot_change_user_field(self):
        """Verifica que un usuario no staff no pueda cambiar el campo 'user'."""
        self.customer.user = self.user2  # Intento cambiar a user2 (no staff)
        with self.assertRaises(PermissionDenied):
            self.customer.save()

    def test_staff_can_change_user_field(self):
        """Verifica que un staff pueda cambiar el campo 'user'."""
        self.customer.user = self.staff_user  # Cambiar a staff_user (staff)
        try:
            self.customer.save()
        except PermissionDenied:
            self.fail("Staff no debería recibir PermissionDenied al cambiar 'user'.")

    def test_non_staff_can_change_non_user_fields(self):
        """Verifica que un usuario no staff pueda cambiar otros campos."""
        self.customer.name = 'Jane'
        try:
            self.customer.save()
        except PermissionDenied:
            self.fail("Cambiar campos no relacionados a 'user' no debe lanzar error.")


class CustomerViewsTest(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username='staff', 
            password='staffpass', 
            is_staff=True
        )
        permissions = [
            'add_customer', 'view_customer', 'change_customer', 'delete_customer'
        ]
        for codename in permissions:
            self.staff_user.user_permissions.add(
                Permission.objects.get(codename=codename)
            )

        self.regular_user = User.objects.create_user(
            username='regular', 
            password='regularpass',
        )
        permission = Permission.objects.get(codename='change_customer')
        self.regular_user.user_permissions.add(permission)
        self.regular_customer = Customer.objects.create(
            user=self.regular_user,
            name='Regular',
            last_name='User',
            email='regular@test.com',
            phone='0987654321',
            address='Regular Address',
            card_number='0000111122223333'
        )

    def test_create_customer_by_staff_creates_user(self):
        """Verifica que staff pueda crear cliente y usuario asociado."""
        self.client.login(username='staff', password='staffpass')
        data = {
            'name': 'New',
            'last_name': 'Customer',
            'email': 'new@customer.com',
            'phone': '5555555555',
            'address': 'New Address',
            'card_number': '1234123412341234'
        }
        response = self.client.post(reverse('create_customer'), data)
        self.assertEqual(response.status_code, 200)
        
        new_customer = Customer.objects.get(name='New')
        new_user = User.objects.get(username='new_customer')
        self.assertEqual(new_customer.user, new_user)
        self.assertEqual(new_user.first_name, 'New')
        self.assertEqual(new_user.last_name, 'Customer')

    def test_non_staff_cannot_create_customer(self):
        """Verifica que usuario sin permisos no pueda acceder a crear cliente."""
        self.client.login(username='regular', password='regularpass')
        response = self.client.get(reverse('create_customer'))
        self.assertEqual(response.status_code, 403)

    def test_show_customers_requires_permission(self):
        """Verifica que se requiera permiso para ver clientes."""
        self.client.login(username='regular', password='regularpass')
        response = self.client.get(reverse('show_customers'))
        self.assertEqual(response.status_code, 403)

    def test_staff_can_delete_customer(self):
        """Verifica que staff pueda eliminar un cliente."""
        self.client.login(username='staff', password='staffpass')
        url = reverse('delete_customer', args=[self.regular_customer.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)  
        self.assertFalse(Customer.objects.filter(id=self.regular_customer.id).exists())

    def test_update_own_customer_by_user(self):
        """Verifica que usuario pueda actualizar su propio cliente."""
        self.client.login(username='regular', password='regularpass')
        url = reverse('update_customer', args=[self.regular_customer.id])
        data = {
            'name': 'UpdatedName',
            'last_name': 'User',
            'email': 'updated@test.com',
            'phone': '0987654321',
            'address': 'Updated Address',
            'card_number': '0000111122223333'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)
        self.regular_customer.refresh_from_db()
        self.assertEqual(self.regular_customer.name, 'UpdatedName')

    def test_user_cannot_update_other_customer(self):
        """Verifica que usuario no pueda actualizar cliente de otro."""
        another_user = User.objects.create_user(username='another', password='anotherpass')
        another_customer = Customer.objects.create(
            user=another_user,
            name='Another',
            last_name='User',
            email='another@test.com',
            phone='0000000000',
            address='Another Address',
            card_number='4444333322221111'
        )
        
        self.client.login(username='regular', password='regularpass')
        url = reverse('update_customer', args=[another_customer.id])
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 403)

    def test_staff_can_update_any_customer(self):
        """Verifica que staff pueda actualizar cualquier cliente."""
        self.client.login(username='staff', password='staffpass')
        url = reverse('update_customer', args=[self.regular_customer.id])
        data = {
            'name': 'StaffUpdated',
            'last_name': 'User',
            'email': 'staffupdated@test.com',
            'phone': '0987654321',
            'address': 'Regular Address',
            'card_number': '0000111122223333'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.regular_customer.refresh_from_db()
        self.assertEqual(self.regular_customer.name, 'StaffUpdated')