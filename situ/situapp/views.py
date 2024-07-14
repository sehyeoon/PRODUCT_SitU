from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from .models import User, TempUser, Cafe, Seat, Reservation
from .forms import UserSignupForm
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def main(request):
    return render(request, 'main.html')

#start 로딩
def start(request):
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
    if request.method == 'POST':
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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

#reserve
def seat_map(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    seats = Seat.objects.filter(cafe_id=cafe_id)
    template_name = f'seat_map/seat_map_{cafe_id}.html' 
    
    print(seats.get(seat_id=1).seat_id)
    return render(request, template_name, {'cafe': cafe, 'seats': seats})

# def seat_map_view(request, cafe_id):
    #seats = Seat.objects.filter(cafe_id=cafe_id)
    return render(request, 'seat_map/seat_map_1.html', {'seats': seats})

@login_required
def reserve_seat(request, seat_id):
    seat = get_object_or_404(Seat, id=seat_id)
    if request.method == 'POST':
        user = request.user if isinstance(request.user, User) else None
        if user:
            reservation = Reservation.objects.create(
                user=user,
                seat=seat,
                reservation_time=timezone.now(),
                number_of_people=request.POST.get('number_of_people', 1),
                seat_status='reserved'

            )
            seat.status='reserved'        
            seat.save()

            return redirect('reservation_complete')
    return render(request, 'reserve_seat.html', {'seat_id': seat_id, 'seat': seat})

@csrf_exempt
@login_required
def update_seat_status(request, seat_id):
    if request.method == 'POST':
        seat = get_object_or_404(Seat, id=seat_id)
        
        data = json.loads(request.body)
        status = data.get('status', 'available')

        seat.status = status
        seat.save()
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


def reservation_complete(request):
    return render(request, 'reservation_complete.html') 


# 카페 상세 페이지를 위한 뷰
def cafe_detail(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    return render(request, 'cafe_detail.html', {'cafe': cafe})

def seat_view(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    seats = Seat.objects.filter(cafe_id=cafe_id)
    return render(request,'seat_view.html', {'cafe': cafe, 'seats': seats})    