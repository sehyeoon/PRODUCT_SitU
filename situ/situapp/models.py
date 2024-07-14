from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    user_id = models.CharField(max_length=50, unique=True)
    user_pw = models.CharField(max_length=100)
    
class TempUser(models.Model):
    tempuser_tel = models.CharField(max_length=20)
    temp_pw = models.CharField(max_length=100)
    
class Cafe(models.Model):
    cafe_id = models.CharField(max_length=50, unique=True)
    cafe_pw = models.CharField(max_length=100)
    cafe_name = models.CharField(max_length=100)
    ceo_name = models.CharField(max_length=100)
    cafe_time = models.CharField(max_length=100)
    ceo_tel = models.CharField(max_length=20)
    cafe_region = models.CharField(max_length=100)
    cafe_tel = models.CharField(max_length=20)
    cafe_address = models.CharField(max_length=255, default="Default Address")
    seats_count = models.IntegerField()
    empty_seats = models.IntegerField()
    cafe_photo = models.ImageField(upload_to='cafe_photos/', null=True, blank=True)

class Seat(models.Model):
    SEAT_STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied'),
    ]
    status = models.CharField(max_length=10, choices=SEAT_STATUS_CHOICES, default='available')
    seat_id =  models.CharField(max_length=50, unique=True)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    plug = models.BooleanField()
    backseat = models.BooleanField()
    seat_start_time = models.DateTimeField(null=True, blank=True)
    seat_use_time = models.DateTimeField(null=True, blank=True)
    seats_no = models.CharField(max_length=128)    
    
    
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField()
    number_of_people = models.IntegerField()
    seat_status = models.CharField(max_length=10, choices=[('available', 'Available'),('reserve','Reserve'),('occupied', 'Occupied')])
