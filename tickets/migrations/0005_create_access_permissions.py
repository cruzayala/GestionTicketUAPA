from django.db import migrations


def create_access_permissions(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Permission = apps.get_model("auth", "Permission")
    content_type, _ = ContentType.objects.get_or_create(app_label="tickets", model="ticket")
    for codename, name in [
        ("view_reports", "Ver reportes"),
        ("manage_access", "Administrar usuarios, roles y permisos"),
    ]:
        Permission.objects.get_or_create(content_type=content_type, codename=codename, defaults={"name": name})


def remove_access_permissions(apps, schema_editor):
    Permission = apps.get_model("auth", "Permission")
    Permission.objects.filter(
        content_type__app_label="tickets",
        content_type__model="ticket",
        codename__in=["view_reports", "manage_access"],
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0004_ticket_assigned_at_ticket_assigned_to_and_more"),
    ]

    operations = [
        migrations.RunPython(create_access_permissions, remove_access_permissions),
    ]
