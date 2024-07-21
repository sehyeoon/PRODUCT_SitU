from django.urls import path
from .views import login_view

urlpatterns = [
    path('login/', login_view, name='login'),
    # 다른 URL 패턴들
]
