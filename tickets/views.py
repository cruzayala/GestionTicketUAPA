from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q

from .forms import ContactForm, LoginForm, SearchTicketForm, StatusForm, TicketDetailForm
from .models import Ticket, TicketEvent


def support_required(request):
    return bool(request.session.get("support_user"))


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
    form = LoginForm(request.POST or None)
    error = ""
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"].strip()
        password = form.cleaned_data["password"].strip()
        if username == "admin" and password == "1234":
            request.session["support_user"] = "Admin"
            return redirect("panel")
        error = "Usuario o contrasena incorrectos."
    return render(request, "tickets/login.html", {"form": form, "error": error})


def logout_view(request):
    request.session.flush()
    return redirect("home")


def panel(request):
    if not support_required(request):
        return redirect("login")
    tickets = Ticket.objects.all()
    context = {
        "open_count": tickets.filter(status="Abierto").count(),
        "process_count": tickets.filter(status="En proceso").count(),
        "closed_count": tickets.filter(status="Cerrado").count(),
        "priority_tickets": tickets.filter(priority="Alta")[:3],
        "recent_tickets": tickets[:3],
    }
    return render(request, "tickets/panel.html", context)


def ticket_list(request):
    if not support_required(request):
        return redirect("login")
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
        TicketEvent.objects.create(ticket=ticket, title="Ticket recibido", note="La solicitud fue registrada correctamente.")
        request.session["last_ticket"] = ticket.number
        request.session.pop("ticket_contact", None)
        return redirect("ticket_confirm")
    return render(request, "tickets/ticket_detalle.html", {"form": form})


def ticket_confirm(request):
    number = request.session.get("last_ticket")
    ticket = get_object_or_404(Ticket, number=number)
    return render(request, "tickets/ticket_confirmacion.html", {"ticket": ticket})


def ticket_status(request, number):
    ticket = get_object_or_404(Ticket, number=number.upper())
    return render(request, "tickets/estado_ticket.html", {"ticket": ticket})


def ticket_manage(request, number):
    if not support_required(request):
        return redirect("login")
    ticket = get_object_or_404(Ticket, number=number.upper())
    form = StatusForm(request.POST or None, initial={"status": ticket.status})
    if request.method == "POST" and form.is_valid():
        ticket.status = form.cleaned_data["status"]
        ticket.save()
        note = form.cleaned_data["note"].strip()
        TicketEvent.objects.create(ticket=ticket, title=f"Estado actualizado a {ticket.status}", note=note)
        return redirect("ticket_manage", number=ticket.number)
    return render(request, "tickets/ticket_manage.html", {"ticket": ticket, "form": form})


def ticket_delete(request, number):
    if not support_required(request):
        return redirect("login")
    ticket = get_object_or_404(Ticket, number=number.upper())
    if request.method == "POST":
        ticket.delete()
        return redirect("ticket_list")
    return redirect("ticket_manage", number=ticket.number)


def settings_view(request):
    if not support_required(request):
        return redirect("login")
    return render(request, "tickets/configuracion.html")
