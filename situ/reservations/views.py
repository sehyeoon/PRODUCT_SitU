from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Seat
from django.contrib.auth.decorators import login_required
from datetime import timedelta

@login_required
def seat_overview(request):
    seats = Seat.objects.all()
    return render(request, 'reservations/seat_overview.html', {'seats': seats, 'user': request.user})

@login_required
def update_seat_status(request, seat_id, status):
    seat = get_object_or_404(Seat, id=seat_id)
    if status == 'occupied':
        seat.seat_status = 'occupied'
        seat.seat_start_time = timezone.now()
    elif status == 'reserved':
        seat.seat_status = 'reserved'
        seat.reserved_by = request.user
    elif status == 'available':
        seat.seat_status = 'available'
        seat.seat_start_time = None
        seat.reserved_by = None
    seat.save()
    return redirect('seat_overview')

@login_required
def confirm_reservation(request, seat_id):
    seat = get_object_or_404(Seat, id=seat_id)
    seat.seat_status = 'reserved'
    seat.reserved_by = request.user
    seat.save()
    return redirect('seat_overview')

@login_required
def cancel_reservation(request, seat_id):
    seat = get_object_or_404(Seat, id=seat_id)
    seat.seat_status = 'available'
    seat.reserved_by = None
    seat.seat_start_time = None
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