from django import forms

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


class TicketUpdateForm(forms.Form):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
    subject = forms.CharField(max_length=160, widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "class": "form-control"}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Nota del cambio de estado", "class": "form-control"}))


class TicketCommentForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "El correo usado al crear el ticket", "class": "form-control"}))
    message = forms.CharField(min_length=5, widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Escriba informacion adicional o responda al equipo de soporte", "class": "form-control"}))
