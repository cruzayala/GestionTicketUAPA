from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Ticket",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("number", models.CharField(blank=True, max_length=20, unique=True)),
                ("full_name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("enrollment", models.CharField(blank=True, max_length=30)),
                ("category", models.CharField(choices=[("Soporte tecnico", "Soporte tecnico"), ("Plataforma virtual", "Plataforma virtual"), ("Administrativa", "Administrativa"), ("Otro", "Otro")], max_length=40)),
                ("priority", models.CharField(choices=[("Baja", "Baja"), ("Media", "Media"), ("Alta", "Alta")], default="Media", max_length=20)),
                ("subject", models.CharField(max_length=160)),
                ("description", models.TextField()),
                ("status", models.CharField(choices=[("Abierto", "Abierto"), ("En proceso", "En proceso"), ("Cerrado", "Cerrado")], default="Abierto", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="TicketEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("note", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("ticket", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="events", to="tickets.ticket")),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
