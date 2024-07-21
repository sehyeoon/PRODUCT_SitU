# reservations/urls.py

from django.urls import path
from .views import seat_overview, update_seat_status, confirm_reservation, cancel_reservation, seat_check, create_reservation

urlpatterns = [
    path('<str:cafe_id>/', seat_overview, name='seat_overview'),
    path('<str:cafe_id>/update_seat_status/<int:seat_id>/<str:status>/', update_seat_status, name='update_seat_status'),
    path('<str:cafe_id>/confirm_reservation/<int:reservation_id>/', confirm_reservation, name='confirm_reservation'),
    path('<str:cafe_id>/cancel_reservation/<int:reservation_id>/', cancel_reservation, name='cancel_reservation'),
    path('<str:cafe_id>/seat_check/<int:seat_id>/', seat_check, name='seat_check'),
    path('<str:cafe_id>/create_reservation/<int:seat_id>/', create_reservation, name='create_reservation'),
]
