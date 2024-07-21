from django.db import models
from accounts.models import Cafe

class Seat(models.Model):
    SEAT_STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('requesting', 'Requesting'),
    ]
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='seats')
    seat_status = models.CharField(max_length=10, choices=SEAT_STATUS_CHOICES, default='available')
    plug = models.BooleanField(null=True, blank=True)
    backseat = models.BooleanField(null=True, blank=True)
    seat_start_time = models.DateTimeField(null=True, blank=True)
    seat_use_time = models.DurationField(null=True, blank=True)
    seats_no = models.IntegerField(null=True, blank=True)
    seats_count = models.IntegerField(null=True, blank=True)
    empty_seats = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'seats'

    def __str__(self):
        return f'Seat {self.seats_no} in Cafe {self.cafe.cafe_id}'

class Reservation(models.Model):
    user_id = models.IntegerField(default=1)  # 기본값 설정
    seats_no = models.IntegerField(null=True, blank=True)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='reservations')
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField(auto_now_add=True)  # 새로운 필드 추가
    reservation_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f'Reservation {self.reservation_id} for Seat {self.seat.seats_no} in Cafe {self.cafe.cafe_id}'
