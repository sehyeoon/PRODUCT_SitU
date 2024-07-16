from django.urls import path
from . import views

urlpatterns = [
    path('', views.seat_overview, name='seat_overview'),
    path('update_seat_status/<int:seat_id>/<str:status>/', views.update_seat_status, name='update_seat_status'),
    path('confirm_reservation/<int:seat_id>/', views.confirm_reservation, name='confirm_reservation'),
    path('cancel_reservation/<int:seat_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('seat_check/<int:seat_id>/', views.seat_check, name='seat_check'),
]
