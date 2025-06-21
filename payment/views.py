import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from reservation_app.models import Reserve


@csrf_exempt
@require_POST
def payment(request):
    """
    Maneja las solicitudes de pago para una reserva.

    Este endpoint acepta solicitudes POST con un cuerpo JSON que contiene
    los campos `orderID`, `reservationID` y `price`. Verifica que el precio
    de la reserva coincida con el precio proporcionado y marca la reserva
    como pagada si la verificación es exitosa.

    Parámetros:
    request (HttpRequest): La solicitud HTTP recibida.

    Retorna:
    JsonResponse: Una respuesta JSON con el estado de la operación.
        - {"status": "success"} si el pago se procesa correctamente.
        - {"status": "failed"} si hay algún error en el procesamiento.

    Ejemplo de solicitud:
    POST /payment/
    {
        "orderID": "12345",
        "reservationID": "67890",
        "price": 100.0
    }

    Ejemplo de respuesta:
    {
        "status": "success"
    }
    """
    if request.method == "POST":
        data = json.loads(request.body)
        reservation_id = data.get("reservationID")
        try:
            reservation = Reserve.objects.get(id=reservation_id)
        except Reserve.DoesNotExist:
            return JsonResponse({"status": "failed"}, status=404)
        if reservation.price != data.get("price"):
            return JsonResponse({"status": "failed"}, status=400)
        reservation.paid = True
        reservation.save()

        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=400)
