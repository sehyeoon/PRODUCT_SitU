from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cafe
from .forms import CafeCreationForm, CafeChangeForm

class CafeAdmin(UserAdmin):
    form = CafeChangeForm
    add_form = CafeCreationForm

    list_display = ('cafe_id', 'name', 'telephone', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('cafe_id', 'password')}),
        ('Personal info', {'fields': ('name', 'telephone')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cafe_id', 'name', 'telephone', 'password1', 'password2', 'is_admin', 'is_active'),
        }),
    )
    search_fields = ('cafe_id', 'name')
    ordering = ('cafe_id',)
    filter_horizontal = ()

admin.site.register(Cafe, CafeAdmin)
