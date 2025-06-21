from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, timedelta
from .models import Room
from reservation_app.models import Reserve
from customer.models import Customer  

from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from datetime import date, timedelta
from .models import Room
from .views import show_rooms

class RoomModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='johndoe', password='12345')
        self.customer = Customer.objects.create(name="John Doe", email="john.doe@example.com", user=self.user)

        self.room = Room.objects.create(
            number=101,
            description="Una habitación cómoda y espaciosa.",
            price=100.0,
            capacity=2,
            photo=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )
        self.reservation = Reserve.objects.create(
            customer_id=self.customer.id,
            starting_date=date.today(),
            nights=3,
            people=2,
            end_date=date.today() + timedelta(days=3),  # Aquí faltaba una coma
            user_id=self.user.id
        )

    def test_room_creation(self):
        """Test para verificar la creación de una habitación."""
        self.assertEqual(self.room.number, 101)
        self.assertEqual(self.room.description, "Una habitación cómoda y espaciosa.")
        self.assertEqual(self.room.price, 100.0)
        self.assertEqual(self.room.capacity, 2)
        self.assertTrue(self.room.photo)

    def test_reserve_dates(self):
        """Test para verificar que las fechas de reserva se añaden correctamente."""
        self.room.reserve_dates(self.reservation)
        expected_dates = [self.reservation.starting_date + timedelta(days=i) for i in range(self.reservation.nights)]
        self.assertEqual(self.room.occupied_dates, expected_dates)

    def test_room_str_representation(self):
        """Test para verificar la representación en cadena del modelo Room."""
        self.assertEqual(str(self.room), "101")



class ShowRoomsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.room = Room.objects.create(
            number=102,
            description="Otra habitación cómoda.",
            price=150.0,
            capacity=3
        )

    def test_show_rooms_view(self):
        """Test para verificar que la vista show_rooms renderiza correctamente."""
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/room/show/')

        # Verifica que el usuario esté autenticado
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        # Verifica que la respuesta sea 200 OK
        self.assertEqual(response.status_code, 200)

        # Verifica que 'rooms' y 'dates' estén en el contexto de la respuesta
        self.assertIn('rooms', response.context)
        self.assertIn('dates', response.context)
        self.assertEqual(response.context['rooms'].first().number, 102)

        # Verifica que la plantilla renderiza correctamente las habitaciones y las fechas
        self.assertContains(response, 'Habitación 102')
        self.assertContains(response, 'Otra habitación cómoda.')
        self.assertContains(response, 'Capacidad: 3')
        self.assertContains(response, 'Precio por noche: 150,0')

        # Verifica que las fechas se renderizan correctamente
        for date in response.context['dates']:
            self.assertContains(response, str(date))