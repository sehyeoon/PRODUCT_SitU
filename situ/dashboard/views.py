from django.shortcuts import render

def dashboard_overview(request):
    return render(request, 'dashboard/overview.html')
