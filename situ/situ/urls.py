"""
URL configuration for situ project.

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
from django.urls import path
from situapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('start/', views.start, name='start'),
    path('login/', views.user_login, name='user_login'),
    path('signup/', views.user_signup, name='user_signup'),
    path('cafe/<int:cafe_id>/', views.cafe_detail, name='cafe_detail'),
    path('cafe/<int:cafe_id>/seats/', views.seat_map, name='seat_map'),
    path('reserve/<int:seat_id>/', views.reserve_seat, name='reserve_seat'),
    path('reservation_complete/', views.reservation_complete, name='reservation_complete'),  # Add this line
    path('cafe/<int:cafe_id>/seat_view', views.seat_view, name='seat_view'),  # Add this line
    path('update_seat_status/<int:seat_id>/', views.update_seat_status, name='update_seat_status'),

]
