# Generated by Django 5.0.4 on 2024-04-25 14:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0021_remove_location_loc_address_ride_host_note_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ride_end_loc', to='website.location'),
        ),
        migrations.AlterField(
            model_name='ride',
            name='start_loc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ride_start_loc', to='website.location'),
        ),
    ]
