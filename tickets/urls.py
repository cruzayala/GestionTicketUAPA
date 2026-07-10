from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("panel/", views.panel, name="panel"),
    path("tickets/", views.ticket_list, name="ticket_list"),
    path("tickets/nuevo/", views.ticket_create_admin, name="ticket_create_admin"),
    path("reportes/", views.reports, name="reports"),
    path("tickets/<str:number>/eliminar/", views.ticket_delete, name="ticket_delete"),
    path("tickets/<str:number>/", views.ticket_manage, name="ticket_manage"),
    path("crear-ticket/", views.ticket_contact, name="ticket_contact"),
    path("ticket-detalle/", views.ticket_detail_form, name="ticket_detail_form"),
    path("ticket-confirmacion/", views.ticket_confirm, name="ticket_confirm"),
    path("estado-ticket/<str:number>/", views.ticket_status, name="ticket_status"),
    path("configuracion/", views.settings_view, name="settings"),
    path("configuracion/usuarios/", views.access_users, name="access_users"),
    path("configuracion/usuarios/nuevo/", views.access_user_create, name="access_user_create"),
    path("configuracion/usuarios/<int:user_id>/editar/", views.access_user_update, name="access_user_update"),
    path("configuracion/usuarios/<int:user_id>/eliminar/", views.access_user_delete, name="access_user_delete"),
    path("configuracion/roles/", views.access_roles, name="access_roles"),
    path("configuracion/roles/nuevo/", views.access_role_create, name="access_role_create"),
    path("configuracion/roles/<int:role_id>/editar/", views.access_role_update, name="access_role_update"),
    path("configuracion/roles/<int:role_id>/eliminar/", views.access_role_delete, name="access_role_delete"),
    path("configuracion/permisos/", views.access_permissions, name="access_permissions"),
    path("configuracion/permisos/nuevo/", views.access_permission_create, name="access_permission_create"),
    path("configuracion/permisos/<int:permission_id>/editar/", views.access_permission_update, name="access_permission_update"),
    path("configuracion/permisos/<int:permission_id>/eliminar/", views.access_permission_delete, name="access_permission_delete"),
]
