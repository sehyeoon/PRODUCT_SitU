from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class UserManager(BaseUserManager):
    def create_user(self, user_id, name, password=None, telephone=None, is_guest=False):
        if not user_id:
            raise ValueError('The User ID must be set')
        user = self.model(user_id=user_id, name=name, telephone=telephone, is_guest=is_guest)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, name, password=None, telephone=None):
        user = self.create_user(user_id, name, password, telephone, is_guest=False)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
    def get_by_natural_key(self, user_id):
        return self.get(user_id=user_id)

class User(AbstractBaseUser, PermissionsMixin):  # PermissionsMixin을 추가하여 상속합니다.
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    user_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    is_guest = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['name', 'telephone']

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

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
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

class Seat(models.Model):
    id = models.AutoField(primary_key=True)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    seat_status = models.CharField(max_length=20, choices=[('available', 'Available'), ('occupied', 'Occupied'), ('requesting', 'Requesting'), ('reserved', 'Reserved')])
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
    reservation_time = models.DateTimeField(default=timezone.now)
    number_of_people = models.IntegerField(default=1)  # 기본값 설정

    def __str__(self):
        return f"{self.user.name} - {self.cafe.cafe_name} - {self.seat.seats_no}"
