from django.db import models
from django.contrib.auth.models import AbstractUser,  BaseUserManager, PermissionsMixin
from django.utils import timezone

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    user_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    
class TempUser(models.Model):
    tempuser_tel = models.CharField(max_length=20)
    temp_pw = models.CharField(max_length=100)
    
class Cafe(models.Model):
    id = models.AutoField(primary_key=True)
    cafe_id = models.CharField(max_length=50, unique=True)
    cafe_pw = models.CharField(max_length=100)
    cafe_name = models.CharField(max_length=100)
    ceo_name = models.CharField(max_length=100, null=True, blank=True)
    cafe_time = models.CharField(max_length=100, null=True, blank=True)
    ceo_tel = models.CharField(max_length=20, null=True, blank=True)
    cafe_region = models.CharField(max_length=100, null=True, blank=True)
    cafe_tel = models.CharField(max_length=20, null=True, blank=True)
    cafe_address = models.CharField(max_length=255, null=True, blank=True)
    cafe_photo = models.ImageField(upload_to='cafe_photos/', null=True, blank=True)
    seats_count = models.IntegerField(null=True, blank=True)
    empty_seats = models.IntegerField(null=True, blank=True)


class Seat(models.Model):
    id = models.AutoField(primary_key=True)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    seat_status = models.CharField(max_length=20, choices=[('available', 'Available'), ('occupied', 'Occupied'), ('reserved', 'Reserved'),('requesting','Requesting')])
    plug = models.BooleanField(null=True, blank=True)
    backseat = models.BooleanField(null=True, blank=True)
    seat_start_time = models.DateTimeField(null=True, blank=True)
    seat_use_time = models.DateTimeField(null=True, blank=True)
    seats_no = models.IntegerField(null=True, blank=True)
    seats_count = models.IntegerField(null=True, blank=True)
    empty_seats = models.IntegerField(null=True, blank=True)
    

class Favorite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    
class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE, related_name='reservations')
    cafe = models.ForeignKey(Cafe, to_field='id', on_delete=models.CASCADE, related_name='reservations')
    seat = models.ForeignKey(Seat, to_field='id', on_delete=models.CASCADE, related_name='reservations')
    reservation_time = models.DateTimeField(default=timezone.now)  # 기본값 설정
    number_of_people = models.IntegerField(default=1)  # 기본값 설정
 
    def __str__(self):
        return f"{self.user.name} - {self.cafe.cafe_name} - {self.seat.seats_no}"