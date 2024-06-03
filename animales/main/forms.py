from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
     class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']