from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import get_user,authenticate, login
from django.contrib.auth.decorators import login_required
from .models import User, Cafe, Seat, Reservation, Favorite
from .forms import UserSignupForm
from django.http import JsonResponse,  HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
import json
import pytz
from django.core.serializers.json import DjangoJSONEncoder

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

#like
@login_required
def like_cafe(request, cafe_id):
    if request.method == 'POST':
        cafe = get_object_or_404(Cafe, cafe_id=cafe_id)
        user = request.user
        
        favorite, created = Favorite.objects.get_or_create(user=user, cafe=cafe)
        if not created:
            favorite.liked = not favorite.liked
            favorite.save()
        
        return JsonResponse({'liked': favorite.liked})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)



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
        )
        reservation.save()
        
        seat.seat_status = 'requesting'
        seat.save()
    

        return redirect('reservation_success.html')

    return render(request, template_name, {'cafe': cafe, 'seats': seats})


def reservation_success(request):
    return render(request, 'reservation_success.html') 


#store

@login_required
def seat_overview(request, cafe_id):
    seats = Seat.objects.filter(cafe_id=cafe_id)
    cafe = get_object_or_404(Cafe, id=cafe_id)
    reservations = Reservation.objects.filter(seat__cafe_id=cafe_id)
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
def confirm_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    seat = reservation.seat
    seat_id = reservation.seat.id
    seat.seat_status = 'reserved'
    seat.save()
    
    return redirect('seat_overview', cafe_id=seat.cafe.id)

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    seat = reservation.seat
    seat_id = reservation.seat.id
    seat.seat_status = 'available'
    reservation.delete()
    seat.save()
    
    return redirect('seat_overview', cafe_id=seat.cafe.id )

@login_required
def seat_check(request, seat_id):
    seat = get_object_or_404(Seat, id=seat_id)
    if seat.seat_status == 'reserved':
        seat.seat_status = 'occupied'
        seat.seat_start_time = timezone.now()
    seat.save()
    return redirect('seat_overview')

#dashboard

@login_required
def dashboard_overview(request, cafe_id):
    cafe = Cafe.objects.get(id=cafe_id)
    seoul_tz = pytz.timezone('Asia/Seoul')
    today = timezone.now().astimezone(seoul_tz)  
    
    start_of_week = today - timezone.timedelta(days=today.weekday())
    end_of_week = start_of_week + timezone.timedelta(days=7)

    reservations_week = Reservation.objects.filter(
        cafe=cafe, 
        reservation_time__date__range=(start_of_week.date(), end_of_week.date())
    )
    reservations_by_day = reservations_week.extra({'day': "strftime('%%w', reservation_time)"}).values('day').annotate(count=Count('id')).order_by('day')
    
    # Days of the week and counts initialization
    days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    counts = [0] * 7

    # Populate counts for each day of the week
    for res in reservations_by_day:
        day = int(res['day'])
        counts[day] = res['count']
        
#시간대별 예약
    reservations_today = Reservation.objects.filter(cafe=cafe, reservation_time__date=today.date())
    reservations_by_hour = reservations_today.extra({'hour': "strftime('%%H', reservation_time)"}).values('hour').annotate(count=Count('id')).order_by('hour')
    hours = list(range(10, 23))
    counts = [0] * len(hours)
    
    for res in reservations_by_hour:
        hour = int(res['hour'])
        counts[hour - 10] = res['count']

    # Determine the hour with the most reservations
    max_hour = None
    if counts:
        max_count = max(counts)
        max_hour = hours[counts.index(max_count)]
        
    # 좋아요 누른 고객 수
    favorite_count = Favorite.objects.filter(cafe=cafe, liked=True).count()

    # 오늘 예약 생성 수
    today_reservations_count = reservations_today.count()

    context = {
        'cafe': cafe,
        'favorite_count': favorite_count,
        'today_reservations_count': today_reservations_count,
        'hours': hours,
        'counts': counts,
        'max_hour': max_hour,
        'days_of_week': days_of_week,


    }

    return render(request, 'dashboard/overview.html', context)
