from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from accounts.models import Cafe

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

class User(AbstractBaseUser, PermissionsMixin): 
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

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

class Seat(models.Model):
    id = models.AutoField(primary_key=True)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    seat_status = models.CharField(max_length=20, choices=[('available', '사용 가능'), ('occupied', '사용중'), ('requesting', '예약 진행중'), ('reserved', '예약 완료')])
    plug = models.BooleanField(null=True, blank=True)
    backseat = models.BooleanField(null=True, blank=True)
    seat_start_time = models.DateTimeField(null=True, blank=True)
    seat_use_time = models.DateTimeField(null=True, blank=True)
    seats_no = models.IntegerField(null=True, blank=True)
    seats_count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.cafe.cafe_name} - {self.seats_no}"

class Favorite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)

class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE, related_name='reservations')
    cafe = models.ForeignKey(Cafe, to_field='id', on_delete=models.CASCADE, related_name='cafe_reservations')
    seat = models.ForeignKey(Seat, to_field='id', on_delete=models.CASCADE, related_name='reservations')
    reservation_time = models.DateTimeField(default=timezone.now)
    number_of_people = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.name} - {self.cafe.cafe_name} - {self.seat.seats_no}"
