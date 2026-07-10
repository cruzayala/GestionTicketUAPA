from django import forms
from django.contrib.auth import get_user_model

from .models import CATEGORY_CHOICES, PRIORITY_CHOICES, STATUS_CHOICES


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

    def __init__(self, *args, staff_users=None, **kwargs):
        super().__init__(*args, **kwargs)
        if staff_users is not None:
            self.fields["assigned_to"].queryset = staff_users


class TicketCommentForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "El correo usado al crear el ticket", "class": "form-control"}))
    message = forms.CharField(min_length=5, widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Escriba informacion adicional o responda al equipo de soporte", "class": "form-control"}))
