from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CafeAuthenticationForm

def login_view(request):
    if request.method == "POST":
        form = CafeAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            cafe_id = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=cafe_id, password=password)
            if user is not None:
                login(request, user)
                return redirect("seat_overview")  # seat_overview URL 패턴 이름으로 수정
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = CafeAuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})
