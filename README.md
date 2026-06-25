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

## Base de datos

```text
database/schema.sql
```
