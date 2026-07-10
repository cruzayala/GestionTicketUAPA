from django.db import models
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


class TicketEvent(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=120)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
