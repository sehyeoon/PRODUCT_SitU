from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CafeManager(BaseUserManager):
    def create_user(self, cafe_id, name, telephone, password=None, **extra_fields):
        if not cafe_id:
            raise ValueError("The Cafe ID must be set")
        cafe = self.model(cafe_id=cafe_id, name=name, telephone=telephone, **extra_fields)
        cafe.set_password(password)
        cafe.save(using=self._db)
        return cafe

    def create_superuser(self, cafe_id, name, telephone, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(cafe_id, name, telephone, password, **extra_fields)

class Cafe(AbstractBaseUser, PermissionsMixin):
    cafe_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CafeManager()

    USERNAME_FIELD = 'cafe_id'
    REQUIRED_FIELDS = ['name', 'telephone']

    class Meta:
        db_table = 'cafes'

    def __str__(self):
        return self.cafe_id
