from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import HttpResponse

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if request.user.is_anonymous:
            return HttpResponse('You must be logged in to connect your social account.')

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        return user