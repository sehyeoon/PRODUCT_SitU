from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Cafe

class CafeCreationForm(forms.ModelForm):
    """A form for creating new cafes. Includes all the required fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Cafe
        fields = ('cafe_id', 'cafe_name', 'telephone')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        cafe = super().save(commit=False)
        cafe.set_password(self.cleaned_data["password1"])
        if commit:
            cafe.save()
        return cafe

class CafeChangeForm(forms.ModelForm):
    """A form for updating cafes. Includes all the fields on the cafe, but replaces the password field with admin's password hash display field."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Cafe
        fields = ('cafe_id', 'cafe_name', 'telephone', 'password', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the field does not have access to the initial value
        return self.initial["password"]


class CafeLoginForm(forms.Form):
    cafe_id = forms.CharField(max_length=100, label='Cafe ID')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')