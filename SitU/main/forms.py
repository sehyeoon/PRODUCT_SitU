from django import forms
from .models import User

class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'phone_number', 'is_guest']
        widgets = {
            'password': forms.PasswordInput(),
        }