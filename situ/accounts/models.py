from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CafeManager(BaseUserManager):
    def create_user(self, cafe_id, name, telephone, password=None):
        if not cafe_id:
            raise ValueError('The Cafe ID field is required')
        cafe = self.model(
            cafe_id=cafe_id,
            name=name,
            telephone=telephone
        )
        cafe.set_password(password)
        cafe.save(using=self._db)
        return cafe

    def create_superuser(self, cafe_id, name, telephone, password=None):
        cafe = self.create_user(
            cafe_id=cafe_id,
            name=name,
            telephone=telephone,
            password=password,
        )
        cafe.is_admin = True
        cafe.is_superuser = True
        cafe.save(using=self._db)
        return cafe

class Cafe(AbstractBaseUser):
    cafe_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CafeManager()

    USERNAME_FIELD = 'cafe_id'
    REQUIRED_FIELDS = ['name', 'telephone']

    def __str__(self):
        return self.cafe_id

    @property
    def is_staff(self):
        return self.is_admin
