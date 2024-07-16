from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('', views.startview, name='start'),
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('cafe/<int:cafe_id>/', views.cafe_detail, name='cafe_detail'),
    path('region/<str:region_name>/', views.region_cafes, name='region_cafes'),
    path('cafe_region/<int:region_id>/', views.cafe_region, name='cafe_region'),
    path('search/', views.search, name='search'),
    path('like/<int:user_id>/', views.user_likes, name='user_likes'),
    path('<int:User_id>/', views.user_profile, name='user_profile'),
    path('ajax/search/', views.ajax_search, name='ajax_search'),
    path('accounts/', include('allauth.urls')),
    path('social-signup/', views.social_signup, name='social_signup'),
    path('account/login/', views.user_login, name='account_login'),
    path('account/logout/', views.user_logout, name='account_logout'),
    path('all_cafes/', views.all_cafes, name='all_cafes'),
    path('cafe/<int:cafe_id>/seats/', views.seat_map, name='seat_map'),
    path('reservation/create/<int:cafe_id>/<int:seat_id>/', views.reservation_create, name='reservation_create'),
    path('reservation/success/', views.reservation_success, name='reservation_success'),  # Add this line
    path('cafe/<int:cafe_id>/seat_overview', views.seat_overview, name='seat_view'),  # Add this line
    path('update_seat_status/<int:seat_id>/', views.update_seat_status, name='update_seat_status'),
    path('confirm_reservation/<int:seat_id>/', views.confirm_reservation, name='confirm_reservation'),
    path('cancel_reservation/<int:seat_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('seat_check/<int:seat_id>/', views.seat_check, name='seat_check'),
]
