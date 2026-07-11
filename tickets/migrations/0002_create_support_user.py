import os

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_support_user(apps, schema_editor):
    password = os.getenv("DJANGO_INITIAL_ADMIN_PASSWORD")
    if not password:
        return
    User = apps.get_model("auth", "User")
    username = "admin"
    if User.objects.filter(username=username).exists():
        return
    User.objects.create(
        username=username,
        email="soporte@uapa.edu",
        first_name="Equipo",
        last_name="Soporte",
        password=make_password(password),
        is_staff=True,
        is_superuser=False,
        is_active=True,
    )


def remove_support_user(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.filter(username="admin", email="soporte@uapa.edu").delete()


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tickets", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_support_user, remove_support_user),
    ]
