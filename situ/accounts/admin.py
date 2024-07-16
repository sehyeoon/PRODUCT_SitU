from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Cafe
from .forms import CafeCreationForm, CafeChangeForm

class CafeAdmin(BaseUserAdmin):
    form = CafeChangeForm
    add_form = CafeCreationForm

    list_display = ('cafe_id', 'name', 'is_admin')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('cafe_id', 'cafe_password')}),
        ('Personal info', {'fields': ('name', 'telephone')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cafe_id', 'name', 'telephone', 'cafe_password1', 'cafe_password2')}
        ),
    )
    search_fields = ('cafe_id',)
    ordering = ('cafe_id',)
    filter_horizontal = ()

admin.site.register(Cafe, CafeAdmin)

