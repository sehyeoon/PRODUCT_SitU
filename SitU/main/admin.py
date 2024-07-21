from django.contrib import admin
from .models import User, Seat, Reservation, Favorite

admin.site.register(User)
admin.site.register(Seat)
admin.site.register(Reservation)
admin.site.register(Favorite)
