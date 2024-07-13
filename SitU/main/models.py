# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=15)
    is_guest = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='main_user_set',  # related_name 추가
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )


    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='main_user_permissions_set',  # related_name 추가
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
class Cafe(models.Model):
    business_code = models.CharField(max_length=20, unique=True)
    business_password = models.CharField(max_length=128)
    name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=50)
    opening_hours = models.CharField(max_length=100)
    owner_phone = models.CharField(max_length=15)
    region = models.CharField(max_length=50)
    cafe_phone = models.CharField(max_length=15)
    address = models.TextField()
    photo = models.ImageField(upload_to='cafe_photos/', null=True, blank=True)

class Seat(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    seat_number = models.IntegerField()

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField()
    number_of_people = models.IntegerField()
    status = models.CharField(max_length=50)