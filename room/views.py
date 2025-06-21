from datetime import datetime, timedelta
from django.shortcuts import render
from .models import Room
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def show_rooms(request):
    """
    Vista para mostrar todas las habitaciones disponibles y las fechas próximas.

    Esta vista requiere que el usuario esté autenticado.

    Args:
        request: El objeto HttpRequest.

    Returns:
        HttpResponse: La respuesta renderizada con la plantilla 'room/show_rooms.html' y el contexto.
    """
    rooms = Room.objects.all()
    dates = [datetime.now().date() + timedelta(days=i) for i in range(15)]
    context = {"rooms": rooms, "dates": dates}
    return render(request, "room/show_rooms.html", context)
