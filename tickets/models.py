from django.db import models
from django.conf import settings
from django.utils import timezone


CATEGORY_CHOICES = [
    ("Soporte tecnico", "Soporte tecnico"),
    ("Plataforma virtual", "Plataforma virtual"),
    ("Administrativa", "Administrativa"),
    ("Otro", "Otro"),
]

PRIORITY_CHOICES = [
    ("Baja", "Baja"),
    ("Media", "Media"),
    ("Alta", "Alta"),
]

STATUS_CHOICES = [
    ("Abierto", "Abierto"),
    ("En proceso", "En proceso"),
    ("Cerrado", "Cerrado"),
]


class Ticket(models.Model):
    number = models.CharField(max_length=20, unique=True, blank=True)
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    enrollment = models.CharField(max_length=30, blank=True)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="Media")
    subject = models.CharField(max_length=160)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Abierto")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_tickets")
    assigned_at = models.DateTimeField(null=True, blank=True)
    first_response_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.number:
            year = timezone.now().year
            prefix = f"GT-{year}-"
            last = Ticket.objects.filter(number__startswith=prefix).order_by("-id").first()
            next_value = 1
            if last:
                next_value = int(last.number.split("-")[-1]) + 1
            self.number = f"{prefix}{next_value:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.number

    @property
    def priority_class(self):
        return f"prioridad-{self.priority.lower()}"

    @property
    def status_class(self):
        if self.status == "En proceso":
            return "estado-proceso"
        if self.status == "Cerrado":
            return "estado-cerrado"
        return "estado-abierto"

    @property
    def category_badge(self):
        if self.category == "Administrativa":
            return "Admin"
        if self.category == "Plataforma virtual":
            return "Virtual"
        if self.category == "Otro":
            return "Otro"
        return "Tecnico"

    @property
    def phase_label(self):
        if self.status == "Cerrado":
            return "Cerrado"
        if not self.assigned_to:
            return "Sin asignar"
        if self.first_response_at:
            return "Seguimiento"
        return "Asignado"

    @property
    def assignee_name(self):
        if not self.assigned_to:
            return "Sin asignar"
        return self.assigned_to.get_full_name() or self.assigned_to.username

    @property
    def elapsed_label(self):
        end_time = self.closed_at or timezone.now()
        total_minutes = max(int((end_time - self.created_at).total_seconds() // 60), 0)
        days, remaining = divmod(total_minutes, 1440)
        hours, minutes = divmod(remaining, 60)
        if days:
            return f"{days}d {hours}h"
        if hours:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"

    @property
    def response_label(self):
        if not self.first_response_at:
            return "Pendiente"
        total_minutes = max(int((self.first_response_at - self.created_at).total_seconds() // 60), 0)
        hours, minutes = divmod(total_minutes, 60)
        if hours:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"


class TicketEvent(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=120)
    note = models.TextField(blank=True)
    author_name = models.CharField(max_length=120, default="Sistema")
    author_role = models.CharField(max_length=30, default="Sistema")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
