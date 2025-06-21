from django.shortcuts import render

import reservation_app
import reservation_app.views
from .forms import CustomerForm
from .models import Customer
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

# Create your views here.


@login_required
@permission_required("customer.add_customer", raise_exception=True)
def create_customer(request):
    """
    Crea un nuevo cliente.

    Si el usuario es staff, también crea un usuario asociado al cliente.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: Redirige a la vista de mostrar clientes si el formulario es válido.
    """
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            if request.user.is_staff:
                customer_data = form.cleaned_data
                username = (
                    f"{customer_data['name']}_{customer_data['last_name']}".lower()
                )
                user = User.objects.create_user(
                    username=username,
                    first_name=customer_data["name"],
                    last_name=customer_data["last_name"],
                    email=customer_data["email"],
                )
                form.instance.user = user
                form.save()
            return show_customers(request)
    else:
        form = CustomerForm()
    context = {"form": form}
    return render(request, "customer/customer_form.html", context)


@login_required
@permission_required("customer.view_customer", raise_exception=True)
def show_customers(request):
    """
    Muestra la lista de clientes.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la plantilla con la lista de clientes.
    """
    customers = Customer.objects.all()
    context = {"customers": customers}
    return render(request, "customer/show_customer.html", context)


@login_required
@permission_required("customer.delete_customer", raise_exception=True)
def delete_customer(request, id):
    """
    Elimina un cliente existente.

    Args:
        request (HttpRequest): La solicitud HTTP.
        id (int): El ID del cliente a eliminar.

    Returns:
        HttpResponse: Redirige a la vista de mostrar clientes.
    """
    customer = Customer.objects.get(id=id)
    customer.delete()
    return show_customers(request)


@login_required
@permission_required("customer.change_customer", raise_exception=True)
def update_customer(request, id):
    """
    Actualiza la información de un cliente existente.

    Args:
        request (HttpRequest): La solicitud HTTP.
        id (int): El ID del cliente a actualizar.

    Raises:
        PermissionDenied: Si el usuario no tiene permiso para editar el cliente.

    Returns:
        HttpResponse: Redirige a la vista de mostrar clientes o reservas según el rol del usuario.
    """
    customer = get_object_or_404(Customer, pk=id)
    if request.user != customer.user and not request.user.is_staff:
        raise PermissionDenied("No tienes permiso para editar este cliente.")
    elif request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            if request.user.is_staff:
                return show_customers(request)
            else:
                return reservation_app.views.show_reservations(request)
    else:
        form = CustomerForm(instance=customer)
    context = {"form": form}
    return render(request, "customer/customer_form.html", context)
