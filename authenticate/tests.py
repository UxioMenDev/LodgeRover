from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from customer.models import Customer
from reservation_app.models import Reserve  

class LoginViewTest(TestCase):
    def setUp(self):
        reserve_content_type = ContentType.objects.get_for_model(Reserve)
        customer_content_type = ContentType.objects.get_for_model(Customer)
        Permission.objects.get_or_create(codename='view_reserve', defaults={'name': 'Can view reserve', 'content_type': reserve_content_type})
        Permission.objects.get_or_create(codename='update_customer', defaults={'name': 'Can update customer', 'content_type': customer_content_type})

        self.user = User.objects.create_user(username='testuser', password='testpass123')
        permissions = [
            'view_reserve', 'update_customer'
        ]
        for codename in permissions:
            self.user.user_permissions.add(
                Permission.objects.get(codename=codename)
            )

        self.login_url = reverse('login')
        self.reservations_url = reverse('show_reservations')
        

    def test_get_unauthenticated_user(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/login.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    def test_post_valid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, self.reservations_url)
        user = authenticate(username='testuser', password='testpass123')
        self.assertTrue(user.is_authenticated)

    def test_post_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        storage = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'Usuario o contraseña incorrectos' for message in storage))

    def test_authenticated_user_redirect(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.login_url)
        self.assertRedirects(response, self.reservations_url)


class CloseSessionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.logout_url = reverse('close_session')
        self.login_url = reverse('login')

    def test_logout_authenticated_user(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.login_url)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_unauthenticated_user(self):
        response = self.client.get(self.logout_url)
        expected_redirect = f"{reverse('login')}?next={self.logout_url}"
        self.assertRedirects(response, expected_redirect)


class RegisterViewTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        Group.objects.create(name='Customers')  # Asegurar que el grupo existe

    def test_get_request(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/register.html')
        self.assertIsInstance(response.context['form'], UserCreationForm)

    def test_post_valid_data(self):
        data = {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        response = self.client.post(self.register_url, data)
        
        self.assertTrue(User.objects.filter(username='newuser').exists())
        user = User.objects.get(username='newuser')
        
        self.assertTrue(Customer.objects.filter(user=user).exists())
        customer = Customer.objects.get(user=user)
        
        self.assertTrue(user.groups.filter(name='Customers').exists())
        
        permission = Permission.objects.get(codename='change_customer')
        user.user_permissions.add(permission)
        

        self.client.login(username='newuser', password='complexpassword123')
        self.assertEqual(response.wsgi_request.user, user)
        self.assertRedirects(response, reverse('update_customer', args=[customer.id]))

    def test_post_invalid_data(self):
        data = {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'differentpassword'
        }
        response = self.client.post(self.register_url, data)        
        self.assertFalse(User.objects.filter(username='newuser').exists())    
        storage = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Los dos campos de contraseña no coinciden.' in str(message) for message in storage))


class CustomerCreationTest(TestCase):
    def test_create_customer(self):
        user = User.objects.create_user(username='testuser')
        customer = Customer.objects.create(user=user)
        self.assertEqual(customer.user, user)
        self.assertIsNotNone(customer.id)