# Generated by Django 5.0.3 on 2024-07-20 08:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_status', models.CharField(choices=[('available', 'Available'), ('occupied', 'Occupied'), ('reserved', 'Reserved'), ('requesting', 'Requesting')], default='available', max_length=10)),
                ('plug', models.BooleanField(blank=True, null=True)),
                ('backseat', models.BooleanField(blank=True, null=True)),
                ('seat_start_time', models.DateTimeField(blank=True, null=True)),
                ('seat_use_time', models.DurationField(blank=True, null=True)),
                ('seats_no', models.IntegerField(blank=True, null=True)),
                ('seats_count', models.IntegerField(blank=True, null=True)),
                ('empty_seats', models.IntegerField(blank=True, null=True)),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to=settings.AUTH_USER_MODEL)),
                ('seat_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reserved_seats', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'seats',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('user_id', models.IntegerField()),
                ('seats_no', models.IntegerField(blank=True, null=True)),
                ('reservation_id', models.AutoField(primary_key=True, serialize=False)),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='reservations.seat')),
            ],
        ),
    ]