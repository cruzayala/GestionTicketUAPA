# GestionTicket UAPA

Sistema web para gestion de tickets de soporte.

## Funcionalidades

- Crear tickets de soporte.
- Consultar estado por numero de ticket.
- Listar y filtrar tickets desde el panel administrativo.
- Actualizar estado e historial del ticket.
- Eliminar tickets desde el detalle administrativo.

## Instalacion

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Acceso

```text
http://127.0.0.1:8000/
usuario: admin
clave: 1234
```

El acceso administrativo se valida contra la tabla de usuarios de Django en la base de datos. La migracion inicial crea el usuario de soporte `admin` con permisos de staff.

## Base de datos

```text
database/schema.sql
```
