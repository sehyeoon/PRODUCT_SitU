from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('', views.startview, name='start'),
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('cafe/<int:Cafe_id>/', views.cafe_detail, name='cafe_detail'),
    path('region/<str:region_name>/', views.region_cafes, name='region_cafes'),
    path('cafe_region/<int:region_id>/', views.cafe_region, name='cafe_region'),
    path('search/', views.search, name='search'),
    path('like/<int:user_id>/', views.user_likes, name='user_likes'),
    path('<int:User_id>/', views.user_profile, name='user_profile'),
    path('reservation/create/', views.reservation_create, name='reservation_create'),
    path('reservation/<int:reservation_id>/', views.reservation_detail, name='reservation_detail'),
    path('ajax/search/', views.ajax_search, name='ajax_search'),
    path('accounts/', include('allauth.urls')),
    path('social-signup/', views.social_signup, name='social_signup'),
    path('account/login/', views.user_login, name='account_login'),
    path('account/logout/', views.user_logout, name='account_logout'),
    path('all_cafes/', views.all_cafes, name='all_cafes'),
]
