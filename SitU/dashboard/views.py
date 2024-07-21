from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import pytz
from accounts.models import Cafe
from reservations.models import Reservation
from .models import Favorite

@login_required
def dashboard_overview(request, cafe_id):
    cafe = Cafe.objects.get(cafe_id=cafe_id)
    seoul_tz = pytz.timezone('Asia/Seoul')
    today = timezone.now().astimezone(seoul_tz)

    start_of_week = today - timezone.timedelta(days=today.weekday())
    end_of_week = start_of_week + timezone.timedelta(days=7)

    reservations_week = Reservation.objects.filter(
        cafe=cafe,
        reservation_time__date__range=(start_of_week.date(), end_of_week.date())
    )
    reservations_by_day = reservations_week.extra({'day': "DAYOFWEEK(reservation_time)"}).values('day').annotate(count=Count('reservation_id')).order_by('day')

    # Days of the week and counts initialization
    days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    counts_by_day = [0] * 7

    # Populate counts for each day of the week
    for res in reservations_by_day:
        day = int(res['day']) - 1  # Adjust to 0-indexed list (Sunday=1, Monday=2, ..., Saturday=7)
        counts_by_day[day] = res['count']

    # 시간대별 예약
    reservations_today = Reservation.objects.filter(cafe=cafe, reservation_time__date=today.date())
    reservations_by_hour = reservations_today.extra({'hour': "HOUR(reservation_time)"}).values('hour').annotate(count=Count('reservation_id')).order_by('hour')
    hours = list(range(10, 23))
    counts_by_hour = [0] * len(hours)

    for res in reservations_by_hour:
        hour = int(res['hour'])
        if 10 <= hour < 23:
            counts_by_hour[hour - 10] = res['count']

    # Determine the hour with the most reservations
    max_hour = None
    if counts_by_hour:
        max_count = max(counts_by_hour)
        max_hour = hours[counts_by_hour.index(max_count)]

    # 좋아요 누른 고객 수
    favorite_count = cafe.favorites.filter(liked=True).count()

    # 오늘 예약 생성 수
    today_reservations_count = reservations_today.count()

    context = {
        'cafe': cafe,
        'favorite_count': favorite_count,
        'today_reservations_count': today_reservations_count,
        'hours': hours,
        'counts_by_hour': counts_by_hour,
        'max_hour': max_hour,
        'days_of_week': days_of_week,
        'counts_by_day': counts_by_day,
    }

    return render(request, 'dashboard/overview.html', context)
