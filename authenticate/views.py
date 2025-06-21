from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.models import Group
from customer.models import Customer


# Create your views here.


def login_view(request):
    """
    Vista para manejar el inicio de sesión de los usuarios.

    Si el usuario no está autenticado, muestra un formulario de autenticación.
    Si el formulario es enviado y válido, autentica al usuario y lo redirige a la página de reservas.
    Si la autenticación falla, muestra un mensaje de error.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP con el formulario de inicio de sesión o una redirección.
    """
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                nombre_usuario = form.cleaned_data.get("username")
                contra = form.cleaned_data.get("password")
                usuario = authenticate(username=nombre_usuario, password=contra)
                if usuario is not None:
                    login(request, usuario)
                    return redirect("welcome")
                else:
                    messages.error(request, "Usuario o contraseña incorrectos")
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            form = AuthenticationForm()
        return render(request, "login/login.html", {"form": form})
    else:
        return redirect("welcome")


@login_required
def close_session(request):
    """
    Vista para manejar el cierre de sesión de los usuarios.

    Cierra la sesión del usuario autenticado y lo redirige a la página de inicio de sesión.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP con la redirección a la página de inicio de sesión.
    """
    logout(request)
    return redirect("login")


class Register(View):
    """
    Vista basada en clases para manejar el registro de nuevos usuarios.

    Métodos:
        get(request): Muestra el formulario de registro.
        post(request): Procesa el formulario de registro y crea un nuevo usuario y cliente.
    """

    def get(self, request):
        """
        Muestra el formulario de registro.

        Args:
            request (HttpRequest): La solicitud HTTP.

        Returns:
            HttpResponse: La respuesta HTTP con el formulario de registro.
        """
        form = UserCreationForm()
        return render(request, "register/register.html", {"form": form})

    def post(self, request):
        """
        Procesa el formulario de registro y crea un nuevo usuario y cliente.

        Si el formulario es válido, guarda el nuevo usuario, crea un cliente asociado,
        añade al usuario al grupo "Customers" y lo autentica.

        Args:
            request (HttpRequest): La solicitud HTTP.

        Returns:
            HttpResponse: La respuesta HTTP con la redirección a la página de actualización del cliente
            o la respuesta HTTP con el formulario de registro y los mensajes de error.
        """
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            customer = create_customer(user)
            group = Group.objects.get(name="Customers")
            user.groups.add(group)
            login(request, user)
            return redirect("update_customer", id=customer.id)
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
            return render(request, "register/register.html", {"form": form})


def create_customer(user):
    """
    Crea un nuevo cliente asociado a un usuario.

    Args:
        user (User): El usuario para el cual se crea el cliente.

    Returns:
        Customer: El objeto cliente creado.
    """
    customer = Customer.objects.create(
        user=user,
    )
    return customer
