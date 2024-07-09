"""
URL configuration for SitU project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main import views  # 올바른 경로로 views 모듈을 가져옵니다.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('cafe/<int:cafe_id>/', views.cafe_detail, name='cafe_detail'),
    path('cafe_region/<int:region_id>/', views.cafe_region, name='cafe_region'),
    path('search/', views.search, name='search'),
    path('like/<int:user_id>/', views.user_likes, name='user_likes'),
    path('<int:user_id>/', views.user_profile, name='user_profile'),
    path('signup/', views.user_signup, name='user_signup'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('reservation/create/', views.reservation_create, name='reservation_create'),
    path('reservation/<int:reservation_id>/', views.reservation_detail, name='reservation_detail'),
]
