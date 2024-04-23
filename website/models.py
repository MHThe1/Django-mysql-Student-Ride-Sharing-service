from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    fullname = models.CharField(max_length=100, default='None')
    student_id = models.CharField(max_length=8, default='None')
    phone_number = models.CharField(max_length=11, default='None')
    rating = models.FloatField(default=5)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile_pics', default='default.png')

    def __str__(self):
        return self.user.username
    

class Vehicle(models.Model):
    host = models.ForeignKey(Profile, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=4, default='Car')
    vehicle_model = models.CharField(max_length=25)
    vehicle_reg = models.CharField(max_length=20, unique=True)
    vehicle_capacity = models.CharField(max_length=2)
    vehicle_color = models.CharField(max_length=20)
    registration_paper = models.ImageField(upload_to='registration_pics', null=True, blank=True)
    v_is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.vehicle_model
    

class Driver(models.Model):
    host = models.ForeignKey(Profile, on_delete=models.CASCADE)
    dl_type = models.CharField(max_length=4, default='Car')
    is_that_host = models.BooleanField(default=True)
    driver_name = models.CharField(max_length=100, null=True, blank=True,)
    dl_reg = models.CharField(max_length=20, unique=True)
    dl_paper = models.ImageField(upload_to='dl_pics', null=True, blank=True)
    dl_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.host.user.username