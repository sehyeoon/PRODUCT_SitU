from django.contrib import admin

# Register your models here.
from .models import User, Cafe, Seat, Reservation

admin.site.register(Cafe)
admin.site.register(Seat)
admin.site.register(Reservation)
admin.site.register(User)