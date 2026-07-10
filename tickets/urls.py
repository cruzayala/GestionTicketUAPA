from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("panel/", views.panel, name="panel"),
    path("tickets/", views.ticket_list, name="ticket_list"),
    path("tickets/nuevo/", views.ticket_create_admin, name="ticket_create_admin"),
    path("tickets/<str:number>/eliminar/", views.ticket_delete, name="ticket_delete"),
    path("tickets/<str:number>/", views.ticket_manage, name="ticket_manage"),
    path("crear-ticket/", views.ticket_contact, name="ticket_contact"),
    path("ticket-detalle/", views.ticket_detail_form, name="ticket_detail_form"),
    path("ticket-confirmacion/", views.ticket_confirm, name="ticket_confirm"),
    path("estado-ticket/<str:number>/", views.ticket_status, name="ticket_status"),
    path("configuracion/", views.settings_view, name="settings"),
]
