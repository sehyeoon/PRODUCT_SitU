from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from accounts.models import Cafe

class StoreIDBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Cafe.objects.get(cafe_id=username)
            if user.check_password(password):
                return user
        except Cafe.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Cafe.objects.get(pk=user_id)
        except Cafe.DoesNotExist:
            return None
