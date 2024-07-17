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
from django.urls import path, include
from situapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('start/', views.startview, name='start'),
    path('accounts/', include('allauth.urls')),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('cafe/<int:cafe_id>/', views.cafe_detail, name='cafe_detail'),
    path('cafe/<int:cafe_id>/seats/', views.seat_map, name='seat_map'),
    path('reservation/create/<int:cafe_id>/<int:seat_id>', views.reservation_create, name='reservation_create'),
    path('reservation_success/', views.reservation_success, name='reservation_success'),  # Add this line
    path('cafe/<int:cafe_id>/seat_overview', views.seat_overview, name='seat_overview'),  # Add this line
    path('update_seat_status/<int:seat_id>/', views.update_seat_status, name='update_seat_status'),
    path('confirm_reservation/<int:reservation_id>/<int:seat_id>/', views.confirm_reservation, name='confirm_reservation'),
    path('cancel_reservation/<int:seat_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('seat_check/<int:seat_id>/', views.seat_check, name='seat_check'),
]


