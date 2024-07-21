# Generated by Django 5.0.7 on 2024-07-17 07:11

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cafe',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cafe_id', models.CharField(max_length=50, unique=True)),
                ('cafe_pw', models.CharField(max_length=100)),
                ('cafe_name', models.CharField(max_length=100)),
                ('ceo_name', models.CharField(blank=True, max_length=100, null=True)),
                ('cafe_time', models.CharField(blank=True, max_length=100, null=True)),
                ('ceo_tel', models.CharField(blank=True, max_length=20, null=True)),
                ('cafe_region', models.CharField(blank=True, max_length=100, null=True)),
                ('cafe_tel', models.CharField(blank=True, max_length=20, null=True)),
                ('cafe_address', models.CharField(blank=True, max_length=255, null=True)),
                ('cafe_photo', models.ImageField(blank=True, null=True, upload_to='cafe_photos/')),
                ('seats_count', models.IntegerField(blank=True, null=True)),
                ('empty_seats', models.IntegerField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('telephone', models.CharField(blank=True, max_length=20, null=True)),
                ('user_id', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('is_guest', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('liked', models.BooleanField(default=False)),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.cafe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('seat_status', models.CharField(choices=[('available', 'Available'), ('occupied', 'Occupied'), ('requesting', 'Requesting'), ('reserved', 'Reserved')], max_length=20)),
                ('plug', models.BooleanField(blank=True, null=True)),
                ('backseat', models.BooleanField(blank=True, null=True)),
                ('seat_start_time', models.DateTimeField(blank=True, null=True)),
                ('seat_use_time', models.DateTimeField(blank=True, null=True)),
                ('seats_no', models.IntegerField(blank=True, null=True)),
                ('seats_count', models.IntegerField(blank=True, null=True)),
                ('empty_seats', models.IntegerField(blank=True, null=True)),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.cafe')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reservation_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('number_of_people', models.IntegerField(default=1)),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='main.cafe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL)),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='main.seat')),
            ],
        ),
    ]