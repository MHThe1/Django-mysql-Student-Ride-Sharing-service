# Generated by Django 5.0.4 on 2024-04-23 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_driver'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='dl_approved',
            field=models.BooleanField(default=False),
        ),
    ]
