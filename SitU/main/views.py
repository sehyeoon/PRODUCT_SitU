from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import User, Cafe, Seat, Favorite, Reservation
from .forms import UserSignupForm
from django.db.models import Q

def home(request):
    areas = ['정후', '참살이', '정문', '제기동', '개운사길', '옆살이', '이공계']
    nearby_cafes = []  # 여기에 실제 카페 데이터를 채워넣을 예정
    context = {
        'areas': areas,
        'nearby_cafes': nearby_cafes,
    }
    return render(request, 'home.html', context)

def cafe_detail(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    return render(request, 'cafe_detail.html', {'cafe': cafe})

def cafe_region(request, region_id):
    # 지역별 카페 목록 로직
    cafes = Cafe.objects.filter(region_id=region_id)
    return render(request, 'cafe_region.html', {'cafes': cafes})

def search(request):
    query = request.GET.get('q')
    if query:
        cafes = Cafe.objects.filter(Q(name__icontains=query) | Q(address__icontains=query))
    else:
        cafes = Cafe.objects.all()
    return render(request, 'search.html', {'cafes': cafes, 'query': query})



@login_required
def user_likes(request, user_id):
    user = get_object_or_404(User, id=user_id)
    likes = Favorite.objects.filter(user=user)
    return render(request, 'user_likes.html', {'likes': likes})

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user_profile.html', {'user': user})

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

@login_required
def reservation_create(request):
    if request.method == 'POST':
        # 예약 생성 로직 구현
        pass
    return render(request, 'reservation_create.html')

@login_required
def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'reservation_detail.html', {'reservation': reservation})

def search(request):
    query = request.GET.get('q', '')
    if query:
        cafes = Cafe.objects.filter(Q(name__icontains=query) | Q(address__icontains=query))
    else:
        cafes = Cafe.objects.all()
    return render(request, 'search.html', {'cafes': cafes, 'query': query})