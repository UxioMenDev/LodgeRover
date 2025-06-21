from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render

from room.models import Room

from .forms import ImageForm, ReservationForm
from .models import Reserve
from django.db.models import Q

# Create your views here.


@login_required
@permission_required("reservation_app.add_reserve", raise_exception=True)
def create_reservation(request, room=None, date=None):
    """
    Vista para crear una nueva reserva.
    Si el método de la solicitud es POST, maneja la solicitud POST.
    Si el método de la solicitud es GET, maneja la solicitud GET.

    Args:
        request: La solicitud HTTP.
        room: El número de la habitación (opcional).
        date: La fecha de inicio de la reserva (opcional).

    Returns:
        Una redirección o un renderizado de la plantilla de formulario de reserva.
    """
    if request.method == "POST":
        return handle_post_request(request, room)
    else:
        return handle_get_request(request, room, date)


def handle_post_request(request, room):
    """
    Maneja la solicitud POST para crear una reserva.

    Args:
        request: La solicitud HTTP.
        room: El número de la habitación (opcional).

    Returns:
        Una redirección o un renderizado de la plantilla de formulario de reserva con errores.
    """
    form = ReservationForm(request.POST, user=request.user)
    if form.is_valid():
        reservation = form.save(commit=False)
        reservation.user = request.user
        reservation.nights = (reservation.end_date - reservation.starting_date).days
        if not request.user.is_staff:
            reservation.customer = request.user.customer
        reservation.occupied_dates = Reserve.compute_occupied_dates(reservation)
        # Save first to get an ID
        reservation.save()
        
        if not handle_room_assignment(request, reservation, room):
            return redirect("create_reservation")
            
        Reserve.calculate_price(reservation)
        reservation.save()
        return redirect("show_reservations")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
    return render_form(request, form)


def handle_get_request(request, room, date):
    """
    Maneja la solicitud GET para crear una reserva.

    Args:
        request: La solicitud HTTP.
        room: El número de la habitación (opcional).
        date: La fecha de inicio de la reserva (opcional).

    Returns:
        Un renderizado de la plantilla de formulario de reserva.
    """
    if room:
        room = Room.objects.get(number=room)
        form = ReservationForm(
            user=request.user,
            initial={"people": room.capacity, "starting_date": date.isoformat()},
        )
    else:
        form = ReservationForm(user=request.user)
    context = {"form": form}
    return render(request, "reservation_app/reservation_form.html", context)


def handle_room_assignment(request, reservation, room):
    """
    Maneja la asignación de habitaciones para una reserva.

    Args:
        request: La solicitud HTTP.
        reservation: La instancia de la reserva.
        room: El número de la habitación (opcional).

    Returns:
        True si la asignación fue exitosa, False en caso contrario.
    """
    free_rooms = Reserve.find_free_rooms(reservation)
    if not free_rooms:
        messages.error(
            request, "No hay habitaciones disponibles para la fecha seleccionada"
        )
        reservation.delete()
        return False
    if room:
        assign_specific_room(reservation, room)
    else:
        Reserve.assign_room(reservation)
    reservation.save()
    return True


def assign_specific_room(reservation, room_number):
    """
    Asigna una habitación específica a una reserva.

    Args:
        reservation: La instancia de la reserva.
        room_number: El número de la habitación.

    Returns:
        None
    """
    room = Room.objects.get(number=room_number)
    reservation.rooms.set([room])
    room.reserve_dates(reservation)
    room.save()


def render_form(request, form):
    """
    Renderiza el formulario de reserva.

    Args:
        request: La solicitud HTTP.
        form: El formulario de reserva.

    Returns:
        Un renderizado de la plantilla de formulario de reserva.
    """
    context = {"form": form}
    return render(request, "reservation_app/reservation_form.html", context)


@login_required
@permission_required("reservation_app.view_reserve", raise_exception=True)
def show_reservations(request):
    """
    Vista para mostrar las reservas.

    Args:
        request: La solicitud HTTP.

    Returns:
        Un renderizado de la plantilla de lista de reservas.
    """
    if request.user.is_staff:
        reservations = Reserve.objects.all()
    else:
        reservations = Reserve.objects.filter(user=request.user)

    search_query = request.GET.get('search', '')
    if search_query:
        reservations = reservations.filter(
            Q(customer__name__icontains=search_query) |
            Q(customer__last_name__icontains=search_query)
        )

    start_date = request.GET.get('start_date')
    if start_date:
        reservations = reservations.filter(starting_date=start_date)
    
    payment_status = request.GET.get('payment_status')
    if payment_status:
        paid = payment_status == 'paid'
        reservations = reservations.filter(paid=paid)
    
    reservations = reservations.order_by('-starting_date')

    context = {
        "reservations": reservations,
        "search_query": search_query,
        "selected_date": start_date,
        "payment_status": payment_status
    }
    return render(request, "reservation_app/show_reservations.html", context)


@login_required
@permission_required("reservation_app.change_reserve", raise_exception=True)
def update_reservation(request, id):
    """
    Vista para actualizar una reserva existente.

    Args:
        request: La solicitud HTTP.
        id: El ID de la reserva a actualizar.

    Returns:
        Una redirección o un renderizado de la plantilla de formulario de reserva.
    """
    reservation = Reserve.objects.get(id=id)
    old_dates = reservation.occupied_dates
    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation, user=request.user)
        if form.is_valid():
            for room in reservation.rooms.all():
                for date in old_dates:
                    if date in room.occupied_dates:
                        room.occupied_dates.remove(date)
                room.save()
            reservation = form.save(commit=False)
            reservation.nights = (reservation.end_date - reservation.starting_date).days
            reservation.occupied_dates = Reserve.compute_occupied_dates(reservation)
            Reserve.calculate_price(reservation)
            reservation.save()
            form.save_m2m()
            for room in reservation.rooms.all():
                room.reserve_dates(reservation)
            return redirect("show_reservations")
    else:
        initial_data = {
            'starting_date': reservation.starting_date.strftime('%Y-%m-%d'),
            'end_date': reservation.end_date.strftime('%Y-%m-%d'),
            'people': reservation.people,
            'rooms': reservation.rooms.all()
        }
        form = ReservationForm(initial=initial_data, instance=reservation, user=request.user)
    
    context = {"form": form}
    return render(request, "reservation_app/reservation_form.html", context)


@login_required
@permission_required("reservation_app.delete_reserve", raise_exception=True)
def delete_reservation(request, id):
    """
    Vista para eliminar una reserva existente.

    Args:
        request: La solicitud HTTP.
        id: El ID de la reserva a eliminar.

    Returns:
        Una redirección a la lista de reservas.
    """
    reservation = Reserve.objects.get(id=id)
    for room in reservation.rooms.all():
        for date in room.occupied_dates:
            if date in reservation.occupied_dates:
                room.occupied_dates.remove(date)
    reservation.delete()
    return redirect("show_reservations")


@login_required
@permission_required("reservation_app.add_images", raise_exception=True)
def upload_images(request, id):
    """
    Vista para subir documentos identificativos relacionados con una reserva.

    Args:
        request: La solicitud HTTP.
        id: El ID de la reserva.

    Returns:
        Una redirección o un renderizado de la plantilla de subida de imágenes.
    """
    reserve = Reserve.objects.get(id=id)
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save(commit=False)
            image_instance.reserve = reserve
            image_instance.save()
            reserve.images.add(image_instance)
            if reserve.images.count() == reserve.people:
                return redirect("show_reservations")
            else:
                return redirect("upload_images", id=id)
    else:
        form = ImageForm()
    images = reserve.images.all()
    context = {"form": form, "images": images}
    return render(request, "reservation_app/upload_images.html", context)


@login_required
@permission_required("reservation_app.change_reserve", raise_exception=True)
def select_room(request, reservation_id, room_id):
    """
    Vista para seleccionar una habitación para una reserva.

    Args:
        request: La solicitud HTTP.
        reservation_id: El ID de la reserva.
        room_id: El ID de la habitación actual.

    Returns:
        Un renderizado de la plantilla de selección de habitación.
    """
    reservation = Reserve.objects.get(id=reservation_id)
    old_room = reservation.rooms.get(id=room_id)
    other_rooms_capacity = reservation.people - old_room.capacity
    rooms = Reserve.find_free_rooms(reservation)
    rooms = [
        r for r in rooms if r.capacity + other_rooms_capacity >= reservation.people
    ]

    if not rooms:
        messages.error(request, "No hay habitaciones disponibles que cumplan con la capacidad requerida.")
        return redirect("show_reservations")

    return render(
        request,
        "room/select_room.html",
        {"rooms": rooms, "reservation": reservation, "old_room": old_room},
    )


@login_required
@permission_required("reservation_app.change_reserve", raise_exception=True)
def change_room(request, reservation_id, old_room_id, room_id):
    """
    Vista para cambiar una habitación en una reserva.

    Args:
        request: La solicitud HTTP.
        reservation_id: El ID de la reserva.
        old_room_id: El ID de la habitación actual.
        room_id: El ID de la nueva habitación.

    Returns:
        Una redirección a la lista de reservas.
    """
    reservation = Reserve.objects.get(id=reservation_id)
    old_room = reservation.rooms.get(id=old_room_id)
    new_room = Room.objects.get(id=room_id)
    reservation.rooms.remove(old_room)
    reservation.rooms.add(new_room)
    old_room.save()
    new_room.save()
    Reserve.calculate_price(reservation)
    reservation.save()
    return show_reservations(request)

@login_required
def welcome(request):
    return render(request, "reservation_app/welcome.html")