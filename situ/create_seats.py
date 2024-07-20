import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'situ.settings')
django.setup()

from reservations.models import Seat, Reservation
from accounts.models import Cafe

# 기존 좌석 데이터 및 예약 데이터 삭제
Reservation.objects.all().delete()
Seat.objects.all().delete()

# 특정 카페 객체 가져오기 (예: cafe_id가 'store_001'인 카페)
cafe = Cafe.objects.get(cafe_id='store_001')

# 예시 좌석 데이터 생성
seats_data = [
    {"seats_no": 1, "seat_status": "available", "cafe": cafe},
    {"seats_no": 2, "seat_status": "available", "cafe": cafe},
    {"seats_no": 3, "seat_status": "available", "cafe": cafe},
    {"seats_no": 4, "seat_status": "available", "cafe": cafe},
    {"seats_no": 5, "seat_status": "available", "cafe": cafe}
]

for seat_data in seats_data:
    Seat.objects.create(**seat_data)

print("좌석 데이터가 성공적으로 생성되었습니다.")
