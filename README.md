# GestionTicket UAPA

Sistema web para gestion de tickets de soporte.

## Funcionalidades

- Crear tickets de soporte.
- Consultar estado por numero de ticket.
- Listar y filtrar tickets desde el panel administrativo.
- Actualizar estado e historial del ticket.
- Eliminar tickets desde el detalle administrativo.
- Asignar tickets a integrantes del equipo.
- Administrar usuarios, roles y permisos.
- Consultar reportes de operacion.

## Instalacion

En Windows PowerShell:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

En Windows CMD:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Acceso

```text
http://127.0.0.1:8000/
```

El acceso administrativo se valida contra los usuarios de Django. Utilice las credenciales creadas con `python manage.py createsuperuser`.

## Base de datos

```text
database/schema.sql
database/export.sql
```

El archivo `schema.sql` contiene la estructura actual de la base de datos y `export.sql` contiene una base limpia generada luego de ejecutar todas las migraciones.

## Produccion

Configure las siguientes variables antes de desplegar:

```text
DJANGO_DEBUG=false
DJANGO_SECRET_KEY=una-clave-larga-y-segura
DJANGO_ALLOWED_HOSTS=dominio.com,www.dominio.com
```

Prepare los archivos estaticos con:

```bash
python manage.py collectstatic --noinput
```

## Verificacion

```bash
python manage.py check
python manage.py test
python manage.py migrate
python manage.py runserver
```
