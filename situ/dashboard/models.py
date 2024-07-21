from django.db import models
from django.conf import settings
from accounts.models import Cafe

class Favorite(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_favorites')
    liked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} likes {self.cafe.cafe_name}"
