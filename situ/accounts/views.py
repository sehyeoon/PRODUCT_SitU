from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import CafeLoginForm
from accounts.models import Cafe

def login_view(request):
    if request.method == 'POST':
        form = CafeLoginForm(request.POST)
        if form.is_valid():
            cafe_id = form.cleaned_data.get('cafe_id')
            password = form.cleaned_data.get('password')
            print(f"cafe_id: {cafe_id}, password: {password}")  # 디버깅 출력
            if not cafe_id or not password:
                form.add_error(None, 'Cafe ID and Password are required')
            else:
                try:
                    cafe = Cafe.objects.get(cafe_id=cafe_id)
                    user = authenticate(request, username=cafe.cafe_id, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('seat_overview', cafe_id=cafe_id)
                    else:
                        form.add_error(None, 'Invalid Cafe ID or Password')
                except Cafe.DoesNotExist:
                    form.add_error('cafe_id', 'Invalid Cafe ID or Password')
    else:
        form = CafeLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})
