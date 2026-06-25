from django import forms

from .models import CATEGORY_CHOICES, PRIORITY_CHOICES, STATUS_CHOICES


class LoginForm(forms.Form):
    username = forms.CharField(max_length=80)
    password = forms.CharField(widget=forms.PasswordInput)


class SearchTicketForm(forms.Form):
    number = forms.CharField(max_length=20)


class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=120)
    email = forms.EmailField()
    enrollment = forms.CharField(max_length=30, required=False)


class TicketDetailForm(forms.Form):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES)
    subject = forms.CharField(max_length=160)
    description = forms.CharField(widget=forms.Textarea)


class StatusForm(forms.Form):
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    note = forms.CharField(required=False, widget=forms.Textarea)
