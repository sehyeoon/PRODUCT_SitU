from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CafeLoginForm

def login_view(request):
    if request.method == 'POST':
        form = CafeLoginForm(request.POST)
        if form.is_valid():
            cafe_id = form.cleaned_data.get('cafe_id')
            cafe_password = form.cleaned_data.get('cafe_password')
            user = authenticate(request, username=cafe_id, password=cafe_password)
            if user is not None:
                login(request, user)
                return redirect('seat_overview')  # 원하는 페이지로 리디렉션
            else:
                form.add_error(None, 'Invalid cafe ID or password')
    else:
        form = CafeLoginForm()
    return render(request, 'accounts/login.html', {'form': form})
