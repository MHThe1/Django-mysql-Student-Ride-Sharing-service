from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    fullname = models.CharField(max_length=100, default='None')
    student_id = models.CharField(max_length=8, default='None')
    phone_number = models.CharField(max_length=11, default='None')
    rating = models.FloatField(default=5)

    def __str__(self):
        return self.user.username
    

class Vehicle(models.Model):
    host = models.ForeignKey(Profile, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=4, default='Car')
    vehicle_model = models.CharField(max_length=25)
    vehicle_reg = models.CharField(max_length=20, unique=True)
    vehicle_capacity = models.CharField(max_length=2)
    vehicle_color = models.CharField(max_length=20)

    def __str__(self):
        return self.vehicle_model