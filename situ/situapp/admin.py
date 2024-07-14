from django.contrib import admin
from .models import Cafe, Seat, Reservation,User,TempUser

admin.site.register(Cafe)
admin.site.register(Seat)
admin.site.register(Reservation)
admin.site.register(User)
admin.site.register(TempUser)
# Register your models here.
