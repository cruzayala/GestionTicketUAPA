from django import forms

from .models import CATEGORY_CHOICES, PRIORITY_CHOICES, STATUS_CHOICES


class LoginForm(forms.Form):
    username = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"placeholder": "Usuario"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Contrasena"}))


class SearchTicketForm(forms.Form):
    number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"placeholder": "GT-2026-001"}))


class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={"placeholder": "Escriba su nombre"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "usuario@correo.com"}))
    enrollment = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={"placeholder": "00-0000"}))


class TicketDetailForm(forms.Form):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES)
    subject = forms.CharField(max_length=160, widget=forms.TextInput(attrs={"placeholder": "Resumen breve del caso"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "placeholder": "Describa con detalle lo que esta ocurriendo"}))


class StatusForm(forms.Form):
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Nota del cambio de estado"}))
