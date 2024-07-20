from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Cafe

class CafeCreationForm(forms.ModelForm):
    """A form for creating new cafes. Includes all the required fields, plus a repeated password."""
    cafe_password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    cafe_password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Cafe
        fields = ('cafe_id', 'name', 'telephone')

    def clean_cafe_password2(self):
        # Check that the two password entries match
        cafe_password1 = self.cleaned_data.get("cafe_password1")
        cafe_password2 = self.cleaned_data.get("cafe_password2")
        if cafe_password1 and cafe_password2 and cafe_password1 != cafe_password2:
            raise forms.ValidationError("Passwords don't match")
        return cafe_password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        cafe = super().save(commit=False)
        cafe.set_password(self.cleaned_data["cafe_password1"])
        if commit:
            cafe.save()
        return cafe

class CafeChangeForm(forms.ModelForm):
    """A form for updating cafes. Includes all the fields on the cafe, but replaces the password field with admin's password hash display field."""
    cafe_password = ReadOnlyPasswordHashField()

    class Meta:
        model = Cafe
        fields = ('cafe_id', 'name', 'telephone', 'cafe_password', 'is_active', 'is_admin')

    def clean_cafe_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the field does not have access to the initial value
        return self.initial["cafe_password"]

class CafeLoginForm(forms.Form):
    cafe_id = forms.CharField(label='Cafe ID')
    cafe_password = forms.CharField(label='Password', widget=forms.PasswordInput)
