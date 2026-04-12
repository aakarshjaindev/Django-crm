"""
Forms for the website (CRM) application.

Provides Django ModelForms for user registration and CRUD operations
on customer records, with Bootstrap-compatible widget styling.
"""

from django import forms
from django.contrib.auth.models import User

from .models import Record


class SignUpForm(forms.ModelForm):
    """
    User registration form.

    Extends Django's User model form to include password and
    confirmation fields with built-in mismatch validation.
    """

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}
        ),
        min_length=8,
        help_text="Must be at least 8 characters.",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}
        ),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Username'}
            ),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'First Name'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Last Name'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Email Address'}
            ),
        }

    def clean(self):
        """Validate that password and confirm_password fields match."""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data


class RecordForm(forms.ModelForm):
    """
    Form for creating and updating customer records.

    Uses explicit ``fields`` instead of ``exclude`` to prevent
    accidental exposure of new fields added to the model.
    """

    class Meta:
        model = Record
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
            'city',
            'state',
            'zipcode',
        ]
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'First Name'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Last Name'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Email'}
            ),
            'phone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Phone Number'}
            ),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Address'}
            ),
            'city': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'City'}
            ),
            'state': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'State'}
            ),
            'zipcode': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Zipcode'}
            ),
        }
