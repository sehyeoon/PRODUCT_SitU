from allauth.account.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import User, Cafe, Seat, Favorite, Reservation
from django.db.models import Q
from django.http import JsonResponse

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
    cafes = Cafe.objects.filter(region_id=region_id)
    return render(request, 'cafe_region.html', {'cafes': cafes})

def search(request):
    query = request.GET.get('q', '')  # 빈 문자열을 기본값으로 설정
    if query:
        cafes = Cafe.objects.filter(Q(name__icontains=query) | Q(address__icontains=query))
    else:
        cafes = Cafe.objects.all()
    return render(request, 'search.html', {'cafes': cafes, 'query': query})

def ajax_search(request):
    query = request.GET.get('q', '')
    cafes = Cafe.objects.filter(name__icontains=query) | Cafe.objects.filter(address__icontains=query)
    results = [{'id': cafe.id, 'name': cafe.name, 'address': cafe.address} for cafe in cafes]
    return JsonResponse(results, safe=False)

@login_required
def user_likes(request, user_id):
    user = get_object_or_404(User, id=user_id)
    likes = Favorite.objects.filter(user=user)
    return render(request, 'user_likes.html', {'likes': likes})

def user_profile(request, user_id):
    if user_id == 0:
        return redirect('user_login')
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user_profile.html', {'user': user})

def account_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        phone_number = request.POST.get('phone')
        agree = request.POST.get('agree')

        if not agree:
            messages.error(request, '개인정보 수집 및 이용에 동의하셔야 합니다.')
            return redirect('account_signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, '이미 사용 중인 아이디입니다.')
            return redirect('account_signup')

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=name,
            phone_number=phone_number
        )
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'user_signup.html')

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

class CustomLoginView(LoginView):
    def form_invalid(self, form):
        response = super().form_invalid(form)
        for error in form.errors.values():
            messages.error(self.request, error[0])
        return response
class CustomLogoutView(LogoutView):
    pass

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

def start(request):
    return render(request, 'start.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # 로그인 성공 시 홈페이지로 리디렉션
        else:
            # 사용자 존재 여부 확인
            if User.objects.filter(username=username).exists():
                messages.error(request, '비밀번호를 잘못 입력했습니다.', extra_tags='login_error_password')
            else:
                messages.error(request, '등록되지 않은 ID입니다.', extra_tags='login_error_username')
    return render(request, 'account/login.html')  # Allauth 템플릿을 사용할 수 있습니다.

