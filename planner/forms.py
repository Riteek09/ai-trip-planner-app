from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Trip


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['destination', 'days', 'mood', 'group_type', 'budget']
        widgets = {
            'destination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Goa'}),
            'days': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 3', 'min': 1}),
            'mood': forms.Select(attrs={'class': 'form-select'}),
            'group_type': forms.Select(attrs={'class': 'form-select'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 15000', 'min': 1000}),
        }
