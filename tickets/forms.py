from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import CATEGORY_CHOICES, PRIORITY_CHOICES, STATUS_CHOICES


FUNCTIONAL_PERMISSION_CHOICES = [
    ("view_reports", "Ver reportes"),
    ("manage_access", "Administrar usuarios, roles y permisos"),
]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"placeholder": "Usuario", "class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Contrasena", "class": "form-control"}))


class SearchTicketForm(forms.Form):
    number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"placeholder": "GT-2026-001", "class": "form-control"}))


class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={"placeholder": "Escriba su nombre", "class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "usuario@correo.com", "class": "form-control"}))
    enrollment = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={"placeholder": "00-0000", "class": "form-control"}))


class TicketDetailForm(forms.Form):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
    subject = forms.CharField(max_length=160, widget=forms.TextInput(attrs={"placeholder": "Resumen breve del caso", "class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "placeholder": "Describa con detalle lo que esta ocurriendo", "class": "form-control"}))


class AdminTicketCreateForm(forms.Form):
    full_name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={"placeholder": "Nombre completo del solicitante", "class": "form-control", "list": "client-name-options"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "correo@ejemplo.com", "class": "form-control", "list": "client-email-options"}))
    enrollment = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={"placeholder": "Opcional", "class": "form-control"}))
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, initial="Media", widget=forms.Select(attrs={"class": "form-select"}))
    subject = forms.CharField(max_length=160, widget=forms.TextInput(attrs={"placeholder": "Resumen claro del caso", "class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 6, "placeholder": "Detalle importante para atender la solicitud", "class": "form-control"}))


class TicketUpdateForm(forms.Form):
    assigned_to = forms.ModelChoiceField(queryset=get_user_model().objects.none(), required=False, empty_label="Sin asignar", widget=forms.Select(attrs={"class": "form-select"}))
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
    subject = forms.CharField(max_length=160, widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "class": "form-control"}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Escriba una respuesta o actualizacion para el solicitante", "class": "form-control"}))

    def __init__(self, *args, support_users=None, **kwargs):
        super().__init__(*args, **kwargs)
        if support_users is not None:
            self.fields["assigned_to"].queryset = support_users


class TicketCommentForm(forms.Form):
    message = forms.CharField(min_length=5, widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Escriba informacion adicional o responda al equipo de soporte", "class": "form-control"}))


class TicketAccessForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Correo usado al crear el ticket", "class": "form-control"}))


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre", max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Apellido", max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Correo", widget=forms.EmailInput(attrs={"class": "form-control"}))
    groups = forms.ModelMultipleChoiceField(label="Roles", queryset=Group.objects.order_by("name"), required=False, widget=forms.CheckboxSelectMultiple)
    is_active = forms.BooleanField(label="Cuenta activa", required=False, initial=True)
    is_staff = forms.BooleanField(label="Acceso administrativo", required=False, initial=False)

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "groups", "is_staff", "is_active", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class UserUpdateForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(label="Roles", queryset=Group.objects.order_by("name"), required=False, widget=forms.CheckboxSelectMultiple)
    password1 = forms.CharField(label="Nueva contrasena", required=False, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Confirmar contrasena", required=False, widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "groups", "is_staff", "is_active")
        labels = {
            "username": "Nombre de usuario",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "email": "Correo",
            "is_staff": "Acceso administrativo",
            "is_active": "Cuenta activa",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 or password2:
            if password1 != password2:
                self.add_error("password2", "Las contrasenas no coinciden.")
            else:
                try:
                    password_validation.validate_password(password1, self.instance)
                except ValidationError as errors:
                    self.add_error("password1", errors)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get("password1"):
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            self.save_m2m()
        return user


class PermissionChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, permission):
        functional_labels = dict(FUNCTIONAL_PERMISSION_CHOICES)
        if permission.codename in functional_labels:
            return functional_labels[permission.codename]
        action = permission.codename.split("_", 1)[0]
        action_labels = {"add": "Crear", "change": "Editar", "delete": "Eliminar", "view": "Ver"}
        model_labels = {"group": "roles", "permission": "permisos", "user": "usuarios", "ticket": "tickets", "ticketevent": "seguimiento de tickets"}
        if action in action_labels and permission.content_type.model in model_labels:
            return f"{action_labels[action]} {model_labels[permission.content_type.model]}"
        return permission.name


class RoleForm(forms.ModelForm):
    permissions = PermissionChoiceField(
        label="Permisos",
        queryset=Permission.objects.select_related("content_type").filter(content_type__app_label__in=["tickets", "auth"]).order_by("content_type__model", "name"),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Group
        fields = ("name", "permissions")
        labels = {"name": "Nombre del rol"}
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


class CustomPermissionForm(forms.ModelForm):
    codename = forms.ChoiceField(
        label="Codigo",
        choices=FUNCTIONAL_PERMISSION_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Permission
        fields = ("codename",)

    def __init__(self, *args, content_type=None, **kwargs):
        self.content_type = content_type
        super().__init__(*args, **kwargs)
        current_codename = self.instance.codename if self.instance.pk else None
        existing = set(Permission.objects.filter(content_type=content_type).values_list("codename", flat=True))
        self.fields["codename"].choices = [
            choice for choice in FUNCTIONAL_PERMISSION_CHOICES
            if choice[0] == current_codename or choice[0] not in existing
        ]

    def clean_codename(self):
        codename = self.cleaned_data["codename"]
        existing = Permission.objects.filter(content_type=self.content_type, codename=codename)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise forms.ValidationError("Ya existe un permiso con este codigo.")
        return codename

    def save(self, commit=True):
        permission = super().save(commit=False)
        permission.content_type = self.content_type
        permission.name = dict(FUNCTIONAL_PERMISSION_CHOICES)[permission.codename]
        if commit:
            permission.save()
        return permission
