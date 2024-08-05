from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=21)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=64)
    password2 = forms.CharField(max_length=64)
        
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']