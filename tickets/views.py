from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ContactForm, LoginForm, SearchTicketForm, TicketCommentForm, TicketDetailForm, TicketUpdateForm
from .models import Ticket, TicketEvent


def support_required(user):
    return user.is_authenticated and user.is_staff


def home(request):
    form = SearchTicketForm(request.POST or None)
    error = ""
    if request.method == "POST" and form.is_valid():
        number = form.cleaned_data["number"].upper()
        if Ticket.objects.filter(number=number).exists():
            return redirect("ticket_status", number=number)
        error = "No encontramos un ticket con ese numero."
    return render(request, "tickets/index.html", {"form": form, "error": error})


def login_view(request):
    if support_required(request.user):
        return redirect("panel")
    form = LoginForm(request.POST or None)
    error = ""
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"].strip()
        password = form.cleaned_data["password"].strip()
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            auth_login(request, user)
            return redirect("panel")
        error = "Usuario o contrasena incorrectos, o la cuenta no tiene acceso administrativo."
    return render(request, "tickets/login.html", {"form": form, "error": error})


@require_POST
def logout_view(request):
    auth_logout(request)
    return redirect("home")


@user_passes_test(support_required, login_url="login")
def panel(request):
    tickets = Ticket.objects.all()
    context = {
        "open_count": tickets.filter(status="Abierto").count(),
        "process_count": tickets.filter(status="En proceso").count(),
        "closed_count": tickets.filter(status="Cerrado").count(),
        "priority_tickets": tickets.filter(priority="Alta")[:3],
        "recent_tickets": tickets[:3],
    }
    return render(request, "tickets/panel.html", context)


@user_passes_test(support_required, login_url="login")
def ticket_list(request):
    tickets = Ticket.objects.all()
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "Todos")
    priority = request.GET.get("priority", "Cualquier prioridad")
    if query:
        tickets = tickets.filter(Q(number__icontains=query) | Q(subject__icontains=query) | Q(full_name__icontains=query))
    if status != "Todos":
        tickets = tickets.filter(status=status)
    if priority != "Cualquier prioridad":
        tickets = tickets.filter(priority=priority)
    context = {
        "tickets": tickets,
        "query": query,
        "status": status,
        "priority": priority,
        "total": tickets.count(),
    }
    return render(request, "tickets/tickets.html", context)


def ticket_contact(request):
    form = ContactForm(request.POST or None, initial=request.session.get("ticket_contact", {}))
    if request.method == "POST" and form.is_valid():
        request.session["ticket_contact"] = form.cleaned_data
        return redirect("ticket_detail_form")
    return render(request, "tickets/crear_ticket.html", {"form": form})


def ticket_detail_form(request):
    contact = request.session.get("ticket_contact")
    if not contact:
        return redirect("ticket_contact")
    form = TicketDetailForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        ticket = Ticket.objects.create(
            full_name=contact["full_name"],
            email=contact["email"],
            enrollment=contact.get("enrollment", ""),
            category=form.cleaned_data["category"],
            priority=form.cleaned_data["priority"],
            subject=form.cleaned_data["subject"],
            description=form.cleaned_data["description"],
        )
        TicketEvent.objects.create(
            ticket=ticket,
            title="Ticket recibido",
            note="La solicitud fue registrada correctamente.",
            author_name="Sistema",
            author_role="Sistema",
        )
        request.session["last_ticket"] = ticket.number
        request.session.pop("ticket_contact", None)
        return redirect("ticket_confirm")
    return render(request, "tickets/ticket_detalle.html", {"form": form})


def ticket_confirm(request):
    number = request.session.get("last_ticket")
    if not number:
        return redirect("home")
    ticket = get_object_or_404(Ticket, number=number)
    return render(request, "tickets/ticket_confirmacion.html", {"ticket": ticket})


def ticket_status(request, number):
    ticket = get_object_or_404(Ticket, number=number.upper())
    form = TicketCommentForm(request.POST or None)
    error = ""
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"].strip().lower()
        if email == ticket.email.lower():
            TicketEvent.objects.create(
                ticket=ticket,
                title="Mensaje del solicitante",
                note=form.cleaned_data["message"].strip(),
                author_name=ticket.full_name,
                author_role="Solicitante",
            )
            messages.success(request, "Su mensaje fue agregado al seguimiento del ticket.")
            return redirect("ticket_status", number=ticket.number)
        error = "El correo no coincide con el usado al crear este ticket."
    return render(request, "tickets/estado_ticket.html", {"ticket": ticket, "form": form, "error": error})


@user_passes_test(support_required, login_url="login")
def ticket_manage(request, number):
    ticket = get_object_or_404(Ticket, number=number.upper())
    form = TicketUpdateForm(request.POST or None, initial={
        "category": ticket.category,
        "priority": ticket.priority,
        "subject": ticket.subject,
        "description": ticket.description,
        "status": ticket.status,
    })
    if request.method == "POST" and form.is_valid():
        ticket.category = form.cleaned_data["category"]
        ticket.priority = form.cleaned_data["priority"]
        ticket.subject = form.cleaned_data["subject"]
        ticket.description = form.cleaned_data["description"]
        ticket.status = form.cleaned_data["status"]
        ticket.save()
        note = form.cleaned_data["note"].strip()
        TicketEvent.objects.create(
            ticket=ticket,
            title="Respuesta del equipo de soporte" if note else "Ticket actualizado",
            note=note,
            author_name=request.user.get_full_name() or request.user.username,
            author_role="Soporte",
        )
        messages.success(request, "Los cambios del ticket fueron guardados correctamente.")
        return redirect("ticket_manage", number=ticket.number)
    return render(request, "tickets/ticket_manage.html", {"ticket": ticket, "form": form})


@user_passes_test(support_required, login_url="login")
@require_POST
def ticket_delete(request, number):
    ticket = get_object_or_404(Ticket, number=number.upper())
    ticket.delete()
    messages.success(request, "El ticket fue eliminado correctamente.")
    return redirect("ticket_list")


@user_passes_test(support_required, login_url="login")
def settings_view(request):
    return render(request, "tickets/configuracion.html")
