# Generated by Django 5.0.4 on 2024-04-23 20:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_location_distance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_loc', models.CharField(max_length=40)),
                ('destination', models.CharField(max_length=40)),
                ('riderpays', models.DecimalField(decimal_places=2, max_digits=6)),
                ('hosted_by', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_method', models.CharField(max_length=10)),
                ('ride_status', models.CharField(max_length=10)),
                ('ride_capacity', models.IntegerField()),
                ('ride_type', models.CharField(max_length=4)),
                ('rider_review', models.IntegerField(default=5)),
                ('host_review', models.IntegerField(default=5)),
                ('rider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.profile')),
            ],
        ),
    ]