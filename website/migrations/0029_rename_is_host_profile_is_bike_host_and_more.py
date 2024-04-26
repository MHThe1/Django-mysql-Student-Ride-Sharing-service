# Generated by Django 5.0.4 on 2024-04-26 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0028_remove_profile_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='is_host',
            new_name='is_bike_host',
        ),
        migrations.AddField(
            model_name='profile',
            name='is_car_host',
            field=models.BooleanField(default=False),
        ),
    ]