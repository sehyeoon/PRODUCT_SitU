from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import get_user,authenticate, login
from django.contrib.auth.decorators import login_required
from .models import User, Cafe, Seat, Reservation
from .forms import UserSignupForm
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse,  HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.functional import SimpleLazyObject

import json

# start
def startview(request):
    return render(request, 'start.html')

# home & login 
def home(request):
    areas = ['정후', '참살이', '정문', '제기동', '개운사길', '옆살이', '이공계']
    nearby_cafes = []  # 여기에 실제 카페 데이터를 채워넣을 예정
    context = {
        'areas': areas,
        'nearby_cafes': nearby_cafes,
    }
    return render(request, 'home.html', context)

# signup
def user_signup(request):
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            form = UserSignupForm()
        return render(request, 'user_signup.html', {'form': form})

# login
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # 로그인 후 리다이렉트할 페이지
        else:
            # 인증 실패 시
            return render(request, 'user_login.html', {'error': 'Invalid username or password'})
    else:
        # GET 요청 시 로그인 폼을 렌더링
        return render(request, 'user_login.html')

@login_required
def user_logout(request):
    auth_logout(request)
    return redirect('home')

#cafe_detail
def cafe_detail(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    seats = Seat.objects.filter(cafe=cafe)
    return render(request, 'cafe_detail.html', {'cafe': cafe , 'seats': seats})


#reserve
@login_required
def seat_map(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    seats = Seat.objects.filter(cafe_id=cafe_id)
    template_name = f'seat_map/seat_map_{cafe_id}.html' 
    
    return render(request, template_name, {'cafe': cafe, 'seats': seats})



@login_required
def reservation_create(request, cafe_id, seat_id):
    user = get_user(request)
    template_name = f'seat_map/seat_map_{cafe_id}.html' 
    cafe = get_object_or_404(Cafe, id=cafe_id)
    seats = Seat.objects.filter(cafe_id=cafe_id)

    
    if request.method == 'POST':
        cafe = get_object_or_404(Cafe, cafe_id=cafe_id)
        seat = get_object_or_404(Seat, id=seat_id)
        user = get_user(request)

        reservation = Reservation.objects.create(
            user=user,
            cafe=cafe,
            seat=seat,
            reservation_time=request.POST.get('reservation_time'),
            number_of_people=request.POST.get('number_of_people'),
            status='reserved',
        )
        reservation.save()

        return redirect('reservation_success.html')

    return render(request, template_name, {'cafe': cafe, 'seats': seats})

def reservation_success(request):
    return render(request, 'reservation_success.html') 



#store


@login_required
def seat_overview(request, cafe_id):
    seats = Seat.objects.filter(cafe_id=cafe_id)
    cafe = get_object_or_404(Cafe, id=cafe_id)
    reservations = Reservation.objects.filter(seat__cafe_id=cafe_id, status='예약중')
    return render(request, 'reservations/seat_overview.html', {'cafe': cafe, 'seats': seats, 'reservations': reservations, 'user': request.user})


@login_required
def update_seat_status(request, seat_id):
    if request.method == 'POST':
        try:
            seat = get_object_or_404(Seat, id=seat_id)
            data = json.loads(request.body)
            status = data.get('status')

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
            else:
                return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)

            seat.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@login_required
def confirm_reservation(request, reservation_id, seat_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.status = '사용중'  # '예약중'에서 '사용중'으로 변경
    reservation.save()

    seat = get_object_or_404(Seat, id=seat_id)
    seat.seat_status = 'reserved'
    seat.save()
    
    return redirect('seat_overview', cafe_id=seat.cafe.id)

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