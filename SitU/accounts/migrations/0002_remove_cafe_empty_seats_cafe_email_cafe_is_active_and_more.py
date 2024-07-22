# Generated by Django 5.0.4 on 2024-07-21 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cafe',
            name='empty_seats',
        ),
        migrations.AddField(
            model_name='cafe',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='cafe',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='cafe',
            name='is_guest',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cafe',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='cafe_user_set', to='auth.group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='cafe_user_permissions_set', to='auth.permission', verbose_name='user permissions'),
        ),
    ]