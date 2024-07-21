from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CafeManager(BaseUserManager):
    def create_user(self, cafe_id, cafe_name, password=None, telephone=None, email=None):
        if not cafe_id:
            raise ValueError('The Cafe ID must be set')
        cafe = self.model(cafe_id=cafe_id, cafe_name=cafe_name, telephone=telephone, email=email)
        cafe.set_password(password)
        cafe.save(using=self._db)
        return cafe

    def create_superuser(self, cafe_id, cafe_name, password=None, telephone=None, email=None):
        cafe = self.create_user(cafe_id, cafe_name, password, telephone, email)
        cafe.is_superuser = True
        cafe.is_staff = True
        cafe.is_active = True
        cafe.save(using=self._db)
        return cafe

class Cafe(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    cafe_id = models.CharField(max_length=50, unique=True)
    cafe_pw = models.CharField(max_length=100)
    cafe_name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    ceo_name = models.CharField(max_length=100, null=True, blank=True)
    cafe_time = models.CharField(max_length=100, null=True, blank=True)
    ceo_tel = models.CharField(max_length=20, null=True, blank=True)
    cafe_region = models.CharField(max_length=100, null=True, blank=True)
    cafe_tel = models.CharField(max_length=20, null=True, blank=True)
    cafe_address = models.CharField(max_length=255, null=True, blank=True)
    cafe_photo = models.ImageField(upload_to='cafe_photos/', null=True, blank=True)
    seats_count = models.IntegerField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)
    is_guest = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'cafe_id'
    REQUIRED_FIELDS = ['cafe_name', 'email']

    objects = CafeManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='cafe_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='cafe_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.cafe_name

    @property
    def empty_seats(self):
        return self.seat_set.filter(seat_status='available').count()
