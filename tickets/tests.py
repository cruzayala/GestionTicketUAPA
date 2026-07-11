from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.staticfiles import finders
from django.test import Client, TestCase
from django.urls import reverse

from .forms import UserCreateForm
from .models import Ticket, TicketEvent
from .views import support_agents


class StaticFilesTests(TestCase):
    def test_only_asset_directories_are_public(self):
        self.assertIsNotNone(finders.find("css/styles.css"))
        self.assertIsNone(finders.find("db.sqlite3"))
        self.assertIsNone(finders.find("gestion_ticket/settings.py"))


class PublicTicketTests(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(
            full_name="Persona Prueba",
            email="persona@example.com",
            enrollment="100000000",
            category="Soporte tecnico",
            priority="Media",
            subject="Caso de prueba",
            description="Descripcion de prueba",
        )
        TicketEvent.objects.create(
            ticket=self.ticket,
            title="Respuesta del equipo de soporte",
            note="Mensaje privado del seguimiento",
            author_name="Agente Prueba",
            author_role="Soporte",
        )
        self.url = reverse("ticket_status", args=[self.ticket.number])

    def test_history_requires_email_verification(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Verifique su correo")
        self.assertNotContains(response, "Mensaje privado del seguimiento")
        response = self.client.post(self.url, {"action": "verify", "email": "persona@example.com"})
        self.assertRedirects(response, self.url)
        response = self.client.get(self.url)
        self.assertContains(response, "Mensaje privado del seguimiento")

    def test_wrong_email_does_not_reveal_history(self):
        response = self.client.post(self.url, {"action": "verify", "email": "otro@example.com"})
        self.assertContains(response, "El correo no coincide")
        self.assertNotContains(response, "Mensaje privado del seguimiento")

    def test_comment_requires_verified_session(self):
        response = self.client.post(self.url, {"action": "comment", "message": "Mensaje de prueba"})
        self.assertRedirects(response, self.url)
        self.assertEqual(self.ticket.events.count(), 1)
        self.client.post(self.url, {"action": "verify", "email": "persona@example.com"})
        response = self.client.post(self.url, {"action": "comment", "message": "Mensaje de prueba"})
        self.assertRedirects(response, self.url)
        self.assertEqual(self.ticket.events.count(), 2)


class TicketManagementTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="agente", password="ClavePrueba2026", is_staff=True)
        self.ticket = Ticket.objects.create(
            full_name="Persona Prueba",
            email="persona@example.com",
            category="Soporte tecnico",
            priority="Media",
            subject="Caso de prueba",
            description="Descripcion de prueba",
        )
        self.client.login(username="agente", password="ClavePrueba2026")

    def test_ticket_cannot_close_without_assignee(self):
        response = self.client.post(reverse("ticket_manage", args=[self.ticket.number]), {
            "assigned_to": "",
            "category": self.ticket.category,
            "priority": self.ticket.priority,
            "subject": self.ticket.subject,
            "description": self.ticket.description,
            "status": "Cerrado",
            "note": "",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Asigne un responsable antes de cerrar el ticket")
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, "Abierto")


class RolePermissionTests(TestCase):
    def setUp(self):
        self.content_type = ContentType.objects.get_for_model(Ticket)
        self.view_ticket = Permission.objects.get(content_type=self.content_type, codename="view_ticket")
        self.change_ticket = Permission.objects.get(content_type=self.content_type, codename="change_ticket")

    def create_user_with_permissions(self, username, permissions):
        group = Group.objects.create(name=f"Rol {username}")
        group.permissions.add(*permissions)
        user = get_user_model().objects.create_user(username=username, password="ClavePrueba2026")
        user.groups.add(group)
        return user

    def test_read_only_role_cannot_modify_or_open_configuration(self):
        self.create_user_with_permissions("lector", [self.view_ticket])
        client = Client()
        response = client.post(reverse("login"), {"username": "lector", "password": "ClavePrueba2026"})
        self.assertRedirects(response, reverse("panel"))
        self.assertEqual(client.get(reverse("ticket_list")).status_code, 200)
        self.assertEqual(client.get(reverse("ticket_create_admin")).status_code, 302)
        self.assertEqual(client.get(reverse("settings")).status_code, 302)

    def test_change_role_user_can_be_assigned(self):
        user = self.create_user_with_permissions("tecnico", [self.view_ticket, self.change_ticket])
        self.assertIn(user, support_agents())

    def test_functional_permissions_open_their_modules(self):
        manage_access = Permission.objects.get(content_type=self.content_type, codename="manage_access")
        view_reports = Permission.objects.get(content_type=self.content_type, codename="view_reports")
        self.create_user_with_permissions("coordinador", [manage_access, view_reports])
        client = Client()
        response = client.post(reverse("login"), {"username": "coordinador", "password": "ClavePrueba2026"})
        self.assertRedirects(response, reverse("settings"))
        self.assertEqual(client.get(reverse("settings")).status_code, 200)
        self.assertEqual(client.get(reverse("reports")).status_code, 200)

    def test_new_users_are_not_administrators_by_default(self):
        self.assertFalse(UserCreateForm().fields["is_staff"].initial)
