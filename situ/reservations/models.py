from django.db import models
from accounts.models import Cafe

class Seat(models.Model):
    SEAT_STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
    ]
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='seats')
    seat_status = models.CharField(max_length=10, choices=SEAT_STATUS_CHOICES, default='available')
    plug = models.BooleanField(null=True, blank=True)
    backseat = models.BooleanField(null=True, blank=True)
    seat_user = models.ForeignKey(Cafe, on_delete=models.SET_NULL, null=True, blank=True, related_name='reserved_seats')
    seat_start_time = models.DateTimeField(null=True, blank=True)
    seat_use_time = models.DurationField(null=True, blank=True)
    seats_no = models.IntegerField(null=True, blank=True)
    seats_count = models.IntegerField(null=True, blank=True)
    empty_seats = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'seats'

    def __str__(self):
        return f'Seat {self.seats_no} in Cafe {self.cafe.cafe_id}'
