from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import User, Cafe, Seat, Favorite, Reservation
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from geopy.distance import distance
from django.contrib.auth.hashers import check_password

def home(request):
    areas = ['정후', '참살이', '정문', '제기동', '개운사길', '옆살이', '이공계']
    nearby_cafes = Cafe.objects.all()
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

def get_all_cafes(user_lat, user_lng):
    cafes = []
    for cafe in Cafe.objects.all():
        if cafe.latitude and cafe.longitude:
            cafe_location = (cafe.latitude, cafe.longitude)
            user_location = (user_lat, user_lng)
            dist = distance(user_location, cafe_location).km
            cafes.append({
                'cafe_id': cafe.cafe_id,
                'cafe_name': cafe.cafe_name,
                'cafe_time': cafe.cafe_time,
                'empty_seats': cafe.empty_seats,
                'cafe_photo': cafe.cafe_photo.url if cafe.cafe_photo else '',
                'distance': round(dist, 2)
            })
    return sorted(cafes, key=lambda x: x['distance'])

def all_cafes(request):
    user_lat = float(request.GET.get('lat'))
    user_lng = float(request.GET.get('lng'))
    all_cafes = get_all_cafes(user_lat, user_lng)
    context = {
        'region_name': '전체보기',
        'cafes': all_cafes,
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
    cafes = Cafe.objects.filter(Q(cafe_name__icontains=query) | Q(cafe_address__icontains=query))
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
    return render(request, 'user_profile.html', {'user': user})

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

@login_required
def reservation_create(request, cafe_id, seat_id):
    if request.method == 'POST':
        cafe = get_object_or_404(Cafe, cafe_id=cafe_id)
        seat = get_object_or_404(Seat, id=seat_id)

        reservation = Reservation.objects.create(
            user=request.user,
            cafe=cafe,
            seat=seat,
            reservation_time=request.POST.get('reservation_time'),
            number_of_people=request.POST.get('number_of_people'),
            status='reserved'
        )
        reservation.save()

        return redirect('reservation_success')

    return render(request, 'reservation_create.html') #추가 수정 필요

@login_required
def reservation_success(request):
    messages.success(request, '예약이 성공적으로 완료되었습니다.')
    return redirect('home')

@login_required
def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'reservation_detail.html', {'reservation': reservation})

def startview(request):
    return render(request, 'start.html')