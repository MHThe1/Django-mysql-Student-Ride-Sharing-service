# Generated by Django 5.0.4 on 2024-04-23 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicle',
            old_name='registraion_paper',
            new_name='registration_paper',
        ),
    ]
