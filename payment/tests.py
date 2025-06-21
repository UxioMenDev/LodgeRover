import json
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from customer.models import Customer
from reservation_app.models import Reserve


class PaymentViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.customer = Customer.objects.create(user=self.user)
        self.reserve = Reserve.objects.create(
            user=self.user,
            customer=self.customer,
            starting_date=date.today(),
            nights=3,
            end_date=date.today() + timedelta(days=3),
            people=2,
            price=100.00
        )
        self.payment_url = reverse('payment')

    def test_successful_payment(self):
        """Test cuando el pago es exitoso."""
        data = {
            "orderID": "12345",
            "reservationID": self.reserve.id,
            "price": 100.0
        }
        response = self.client.post(
            self.payment_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "success"})
        # Verificar que la reserva se marcó como pagada
        updated_reserve = Reserve.objects.get(id=self.reserve.id)
        self.assertTrue(updated_reserve.paid)

    def test_price_mismatch_failure(self):
        """Test falla cuando el precio no coincide con la reserva."""
        data = {
            "orderID": "12345",
            "reservationID": self.reserve.id,
            "price": 99.99  # Precio incorrecto
        }
        response = self.client.post(
            self.payment_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"status": "failed"})
        # Verificar que la reserva NO está pagada
        updated_reserve = Reserve.objects.get(id=self.reserve.id)
        self.assertFalse(updated_reserve.paid)

    def test_invalid_reservation_id(self):
        """Test falla cuando la reserva no existe."""
        data = {
            "orderID": "12345",
            "reservationID": 9999,  # ID inexistente
            "price": 100.0
        }
        response = self.client.post(
            self.payment_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    def test_non_post_method_failure(self):
        """Test rechaza métodos HTTP que no sean POST."""
        # Probar con GET
        response = self.client.get(self.payment_url)
        self.assertEqual(response.status_code, 405)

        # Probar con PUT
        response = self.client.put(self.payment_url)
        self.assertEqual(response.status_code, 405)