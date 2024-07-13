from django.contrib import admin
from django.urls import path, include
from main.views import CustomLoginView, CustomLogoutView
from main import views

urlpatterns = [
    path('', views.start, name='start'),
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('cafe/<int:cafe_id>/', views.cafe_detail, name='cafe_detail'),
    path('cafe_region/<int:region_id>/', views.cafe_region, name='cafe_region'),
    path('search/', views.search, name='search'),
    path('like/<int:user_id>/', views.user_likes, name='user_likes'),
    path('<int:user_id>/', views.user_profile, name='user_profile'),
    path('reservation/create/', views.reservation_create, name='reservation_create'),
    path('reservation/<int:reservation_id>/', views.reservation_detail, name='reservation_detail'),
    path('ajax/search/', views.ajax_search, name='ajax_search'),
    path('accounts/', include('allauth.urls')),
    path('social-signup/', views.social_signup, name='social_signup'),
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='account_logout'),
]
