from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import User, Cafe, Seat, Favorite, Reservation
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from geopy.distance import distance
from django.utils import timezone
from django.contrib.auth.hashers import check_password
import json

def home(request):
    areas = ['정후', '참살이', '정문', '제기동', '개운사길', '옆살이', '이공계']
    nearby_cafes = []

    user_lat = request.GET.get('lat')
    user_lng = request.GET.get('lng')
    
    if user_lat and user_lng:
        user_lat = float(user_lat)
        user_lng = float(user_lng)
        for cafe in Cafe.objects.all():
            if cafe.latitude and cafe.longitude:
                cafe_location = (cafe.latitude, cafe.longitude)
                user_location = (user_lat, user_lng)
                dist = distance(user_location, cafe_location).km
                if dist <= 3:
                    nearby_cafes.append({
                        'cafe_id': cafe.cafe_id,
                        'cafe_name': cafe.cafe_name,
                        'cafe_time': cafe.cafe_time,
                        'empty_seats': cafe.empty_seats,
                        'cafe_photo': cafe.cafe_photo.url if cafe.cafe_photo else '',
                        'distance': round(dist, 2)
                    })

    context = {
        'areas': areas,
        'nearby_cafes': nearby_cafes,
    }
    return render(request, 'home.html', context)

def region_cafes(request, region_name):
    cafes = Cafe.objects.filter(cafe_region=region_name)
    context = {
        'region_name': region_name,
        'cafes': cafes,
    }
    return render(request, 'region.html', context)

def nearby_cafes(request):
    user_lat = float(request.GET.get('lat'))
    user_lng = float(request.GET.get('lng'))

    cafes = []
    for cafe in Cafe.objects.all():
        if cafe.latitude and cafe.longitude:
            cafe_location = (cafe.latitude, cafe.longitude)
            user_location = (user_lat, user_lng)
            dist = distance(user_location, cafe_location).km
            if dist <= 3:
                cafes.append({
                    'cafe_id': cafe.cafe_id,
                    'cafe_name': cafe.cafe_name,
                    'cafe_time': cafe.cafe_time,
                    'empty_seats': cafe.empty_seats,
                    'cafe_photo': cafe.cafe_photo.url if cafe.cafe_photo else '',
                    'distance': round(dist, 2)
                })

    return JsonResponse(cafes, safe=False)

def all_cafes(request):
    user_lat = request.GET.get('lat')
    user_lng = request.GET.get('lng')
    
    cafes = []
    for cafe in Cafe.objects.all():
        cafe_data = {
            'cafe_id': cafe.cafe_id,
            'cafe_name': cafe.cafe_name,
            'cafe_time': cafe.cafe_time,
            'empty_seats': cafe.empty_seats,
            'cafe_photo': cafe.cafe_photo.url if cafe.cafe_photo else '',
        }
        
        if user_lat and user_lng and cafe.latitude and cafe.longitude:
            user_location = (float(user_lat), float(user_lng))
            cafe_location = (cafe.latitude, cafe.longitude)
            dist = distance(user_location, cafe_location).km
            cafe_data['distance'] = round(dist, 2)
        else:
            cafe_data['distance'] = None
        
        cafes.append(cafe_data)
    
    # 거리 정보가 있는 경우에만 정렬
    cafes_with_distance = [c for c in cafes if c['distance'] is not None]
    cafes_without_distance = [c for c in cafes if c['distance'] is None]
    
    sorted_cafes = sorted(cafes_with_distance, key=lambda x: x['distance']) + cafes_without_distance

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(sorted_cafes, safe=False)
    else:
        context = {
            'region_name': '전체',
            'cafes': sorted_cafes,
        }
        return render(request, 'region.html', context)

def cafe_detail(request, cafe_id):
    cafe = get_object_or_404(Cafe, cafe_id=cafe_id)
    seats = Seat.objects.filter(cafe=cafe)
    return render(request, 'cafe_detail.html', {'cafe': cafe, 'seats': seats})

def cafe_region(request, region_id):
    cafes = Cafe.objects.filter(cafe_region=region_id)
    return render(request, 'cafe_region.html', {'cafes': cafes})

def search(request):
    query = request.GET.get('q')
    if query:
        cafes = Cafe.objects.filter(Q(cafe_name__icontains=query))
    else:
        cafes = Cafe.objects.all()
    return render(request, 'search.html', {'cafes': cafes, 'query': query})

def ajax_search(request):
    query = request.GET.get('q', '')
    plug_filter = request.GET.get('plug') == 'true'
    backseat_filter = request.GET.get('backseat') == 'true'
    filters_applied = request.GET.get('filtersApplied') == 'true'

    cafes = Cafe.objects.all()

    if query:
        cafes = cafes.filter(Q(cafe_name__icontains=query) | Q(cafe_address__icontains=query))

    if filters_applied:
        if plug_filter and backseat_filter:
            cafes = cafes.filter(seat__seat_status='available', seat__plug=True, seat__backseat=True).distinct()
        elif plug_filter:
            cafes = cafes.filter(seat__seat_status='available', seat__plug=True).distinct()
        elif backseat_filter:
            cafes = cafes.filter(seat__seat_status='available', seat__backseat=True).distinct()

    results = [{'id': cafe.id, 'cafe_name': cafe.cafe_name, 'cafe_address': cafe.cafe_address} for cafe in cafes]
    return JsonResponse(results, safe=False)


@login_required
def user_likes(request, user_id):
    user = get_object_or_404(User, id=user_id)
    likes = Favorite.objects.filter(user=user)
    return render(request, 'user_likes.html', {'likes': likes})

@login_required
def like_cafe(request, cafe_id):
    cafe = get_object_or_404(Cafe, cafe_id=cafe_id)
    user = request.user

    favorite, created = Favorite.objects.get_or_create(user=user, cafe=cafe)
    if not created:
        favorite.liked = not favorite.liked
        favorite.save()

    return redirect('cafe_detail', cafe_id=cafe_id)

def user_profile(request, User_id):
    if User_id == 0:
        return redirect('user_login')
    user = get_object_or_404(User, id=User_id)
    current_reservations = Reservation.objects.filter(
        user=user,
        reservation_time__gte=timezone.now()
    ).order_by('reservation_time')
    
    # 현재 시간 이전의 예약을 가져옵니다 (과거 예약)
    past_reservations = Reservation.objects.filter(
        user=user,
        reservation_time__lt=timezone.now()
    ).order_by('-reservation_time')
    
    context = {
        'user': user,
        'current_reservations': current_reservations,
        'past_reservations': past_reservations,
    }
    return render(request, 'user_profile.html', context)

def user_signup(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        name = request.POST.get('name')
        telephone = request.POST.get('telephone')
        agree = request.POST.get('agree')

        if not agree:
            messages.error(request, '개인정보 수집 및 이용에 동의하셔야 합니다.')
            return redirect('account/signup')
        if User.objects.filter(user_id=user_id).exists():
            messages.error(request, '이미 사용 중인 아이디입니다.')
            return redirect('account/signup')

        User = User.objects.create(
            user_id=user_id,
            name=name,
            telephone=telephone
        )
        User.set_password(password)  # 비밀번호 해시 저장
        User.save()

        auth_login(request, User, backend='django.contrib.auth.backends.ModelBackend')

        return redirect('home')
    else:
        return render(request, 'account/signup.html')

def social_signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone')

        user = request.user
        user.first_name = name
        user.phone_number = phone_number
        user.save()

        return redirect('home')
    else:
        return render(request, 'social_signup.html')


def user_login(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        user = User.objects.filter(user_id=user_id).first()
        if user is not None and user.check_password(password):
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')  
        else:
            if User.objects.filter(user_id=user_id).exists():
                messages.error(request, '비밀번호를 잘못 입력했습니다.')
            else:
                messages.error(request, '등록되지 않은 ID입니다.')
    return render(request, 'account/login.html')

@login_required
def user_logout(request):
    auth_logout(request)
    return redirect('home')

#reserve
@login_required
def seat_map(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    seats = Seat.objects.filter(cafe_id=cafe_id)
    template_name = f'seat_map/seat_map_{cafe_id}.html' 
    
    return render(request, template_name, {'cafe': cafe, 'seats': seats})

@login_required
def reservation_create(request, cafe_id, seat_id):
    user = request.user
    template_name = f'seat_map/seat_map_{cafe_id}.html' 
    cafe = get_object_or_404(Cafe, id=cafe_id)
    seats = Seat.objects.filter(cafe_id=cafe_id)

    if request.method == 'POST':
        cafe = get_object_or_404(Cafe, cafe_id=cafe_id)
        seat = get_object_or_404(Seat, id=seat_id)
        user = request.user

        reservation = Reservation.objects.create(
            user=user,
            cafe=cafe,
            seat=seat,
            reservation_time=timezone.now(),
            number_of_people=request.POST.get('number_of_people'),
            status='reserved',
        )
        reservation.save()

        return redirect('reservation_success')

    return render(request, template_name, {'cafe': cafe, 'seats': seats})

def reservation_success(request):
    return render(request, 'reservation_success.html') 

@login_required
def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'reservation_detail.html', {'reservation': reservation})

def startview(request):
    return render(request, 'start.html')


#store

def cafe_login(request):
    if request.method == 'POST':
        cafe_id = request.POST.get('cafe_id')
        cafe_pw = request.POST.get('cafe_pw')
        try:
            cafe = Cafe.objects.get(cafe_id=cafe_id)
            if cafe.cafe_pw == cafe_pw:
                # 로그인 성공 처리
                request.session['cafe_id'] = cafe.id
                return redirect('cafe_dashboard')  # 로그인 후 리다이렉트할 페이지
            else:
                messages.error(request, '비밀번호가 올바르지 않습니다.')
        except Cafe.DoesNotExist:
            messages.error(request, '존재하지 않는 카페 ID입니다.')
    return render(request, 'cafe_login.html')

@login_required
def seat_overview(request, cafe_id):
    seats = Seat.objects.all()
    cafe = get_object_or_404(Cafe, id=cafe_id)
    return render(request, 'reservations/seat_overview.html', {'cafe': cafe,'seats': seats, 'user': request.user})

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