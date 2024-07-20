from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Seat, Reservation
from django.contrib.auth.decorators import login_required
from datetime import timedelta

@login_required
def seat_overview(request):
    seats = Seat.objects.all()
    seats_with_reservations = []
    for seat in seats:
        reservations = seat.reservations.all()
        if reservations.exists():
            seats_with_reservations.append({
                'seat': seat,
                'reservation': reservations.first()
            })
        else:
            seats_with_reservations.append({
                'seat': seat,
                'reservation': None
            })
    return render(request, 'reservations/seat_overview.html', {'seats_with_reservations': seats_with_reservations, 'user': request.user})

@login_required
def update_seat_status(request, seat_id, status):
    seat = get_object_or_404(Seat, id=seat_id)
    if status == 'occupied':
        seat.seat_status = 'occupied'
        seat.seat_start_time = timezone.now()
    elif status == 'reserved':
        seat.seat_status = 'reserved'
    elif status == 'available':
        seat.seat_status = 'available'
        seat.seat_start_time = None
        seat.reserved_by = None
    seat.save()
    return redirect('seat_overview')

@login_required
def confirm_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    seat = reservation.seat
    seat.seat_status = 'reserved'
    seat.save()
    return redirect('seat_overview')

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    seat = reservation.seat
    seat.seat_status = 'available'
    reservation.delete()
    seat.save()
    return redirect('seat_overview')

@login_required
def seat_check(request, seat_id):
    seat = get_object_or_404(Seat, id=seat_id)
    if seat.seat_status == 'reserved':
        seat.seat_status = 'occupied'
        seat.seat_start_time = timezone.now()
    seat.save()
    return redirect('seat_overview')

@login_required
def create_reservation(request, seat_id):
    seat = get_object_or_404(Seat, id=seat_id)
    reservation = Reservation.objects.create(seat=seat, cafe=request.user, user_id=request.user.id)
    seat.seat_status = 'requesting'
    seat.save()
    return redirect('seat_overview')
