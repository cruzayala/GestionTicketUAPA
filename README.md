# GestionTicket UAPA

Sistema web para gestion de tickets de soporte.

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
