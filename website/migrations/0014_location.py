# Generated by Django 5.0.4 on 2024-04-23 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_alter_driver_is_that_host'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=40)),
                ('loc_address', models.CharField(max_length=300)),
                ('latitude', models.CharField(max_length=100)),
                ('longitude', models.CharField(max_length=100)),
            ],
        ),
    ]
