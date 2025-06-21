from django.test import TestCase
from django.contrib.auth.models import User
from room.models import Room
from .models import Reserve, Image
from customer.models import Customer
from datetime import date, timedelta
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class ReserveModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.customer = Customer.objects.create(user=cls.user, name="Test Customer")
        cls.room = Room.objects.create(number=101, capacity=2, price=100.00)
        cls.reserve = Reserve.objects.create(
            user=cls.user,
            customer=cls.customer,
            starting_date=date.today(),
            nights=3,
            end_date=date.today() + timedelta(days=3),
            people=2,
            price=300.00
        )
        cls.reserve.rooms.add(cls.room)

    def test_reserve_creation(self):
        self.assertEqual(self.reserve.user.username, 'testuser')
        self.assertEqual(self.reserve.customer.name, 'Test Customer')
        self.assertEqual(self.reserve.nights, 3)
        self.assertEqual(self.reserve.people, 2)
        self.assertEqual(self.reserve.price, 300.00)
        self.assertTrue(self.reserve.rooms.filter(number=101).exists())

    def test_compute_occupied_dates(self):
        occupied_dates = self.reserve.compute_occupied_dates()
        expected_dates = [date.today() + timedelta(days=i) for i in range(3)]
        self.assertEqual(occupied_dates, expected_dates)

    def test_calculate_price(self):
        self.reserve.calculate_price()
        self.assertEqual(self.reserve.price, 300.00)

    def test_assign_room(self):
        self.reserve.assign_room()
        self.assertTrue(self.reserve.rooms.filter(number=101).exists())

class ImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.customer = Customer.objects.create(user=cls.user, name="Test Customer")
        cls.room = Room.objects.create(number=101, capacity=2, price=100.00)
        cls.reserve = Reserve.objects.create(
            user=cls.user,
            customer=cls.customer,
            starting_date=date.today(),
            nights=3,
            end_date=date.today() + timedelta(days=3),
            people=2,
            price=300.00
        )
        cls.image = Image.objects.create(reserve=cls.reserve, image='path/to/image.jpg')

    def test_image_creation(self):
        self.assertEqual(self.image.reserve, self.reserve)
        self.assertEqual(self.image.image, 'path/to/image.jpg')

from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class ReserveViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        content_type = ContentType.objects.get_for_model(Reserve)
        permission = Permission.objects.get(
            codename='add_reserve',
            content_type=content_type,
        )
        cls.user.user_permissions.add(permission)
        cls.customer = Customer.objects.create(user=cls.user, name="Test Customer")
        cls.room = Room.objects.create(number=101, capacity=2, price=100.00)

    def test_create_reservation_get(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('create_reservation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservation_app/reservation_form.html')

    def test_create_reservation_post(self):
        self.client.login(username='testuser', password='12345')
        data = {
            'customer': self.customer.id,
            'starting_date': date.today(),
            'nights': 3,
            'people': 2,
            'rooms': [self.room.id],
        }
        response = self.client.post(reverse('create_reservation'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Reserve.objects.filter(customer=self.customer).exists())

class ShowReservationsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        content_type = ContentType.objects.get_for_model(Reserve)
        permission = Permission.objects.get(
            codename='view_reserve',
            content_type=content_type,
        )
        cls.user.user_permissions.add(permission)
        cls.customer = Customer.objects.create(user=cls.user, name="Test Customer")
        cls.room = Room.objects.create(number=101, capacity=2, price=100.00)
        cls.reserve = Reserve.objects.create(
            user=cls.user,
            customer=cls.customer,
            starting_date=date.today(),
            nights=3,
            end_date=date.today() + timedelta(days=3),
            people=2,
            price=300.00
        )
        cls.reserve.rooms.add(cls.room)

    def test_show_reservations(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('show_reservations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservation_app/show_reservations.html')
        self.assertContains(response, 'Test Customer')        


class UploadImagesViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        
        content_type = ContentType.objects.get_for_model(Reserve)
        permission, created = Permission.objects.get_or_create(
            codename='add_images',
            content_type=content_type,
            defaults={'name': 'Can add images'},
        )
        
        cls.user.user_permissions.add(permission)
        cls.customer = Customer.objects.create(user=cls.user, name="Test Customer")
        cls.room = Room.objects.create(number=101, capacity=2, price=100.00)
        cls.reserve = Reserve.objects.create(
            user=cls.user,
            customer=cls.customer,
            starting_date=date.today(),
            nights=3,
            end_date=date.today() + timedelta(days=3),
            people=2,
            price=300.00
        )
        cls.reserve.rooms.add(cls.room)
    def test_upload_images_get(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('upload_images', args=[self.reserve.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservation_app/upload_images.html')

    def test_upload_images_post(self):
        self.client.login(username='testuser', password='12345')
        with open('media/rooms/default.jpg', 'rb') as img:
            response = self.client.post(reverse('upload_images', args=[self.reserve.id]), {'image': img})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Image.objects.filter(reserve=self.reserve).exists())