from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    fullname = models.CharField(max_length=100, default='None')
    student_id = models.CharField(max_length=8, default='None')
    phone_number = models.CharField(max_length=11, default='None')
    address = models.CharField(null=True, blank=True, max_length=300)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile_pics', default='default.png')

    is_bike_host = models.BooleanField(default=False)
    is_car_host = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    

class Vehicle(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
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
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    dl_type = models.CharField(max_length=4, default='Car')
    is_that_host = models.BooleanField(default=True)
    driver_name = models.CharField(max_length=100, null=True, blank=True,)
    dl_reg = models.CharField(max_length=20, unique=True)
    dl_paper = models.ImageField(upload_to='dl_pics', null=True, blank=True)
    dl_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.host.username


class Location(models.Model):
    location_name = models.CharField(max_length=300)

    def __str__(self):
        return self.location_name
    

class Ride(models.Model):
    rider = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='rides_as_rider')
    start_loc = models.CharField(max_length=500)
    destination = models.CharField(max_length=500)
    riderpays = models.DecimalField(max_digits=10, decimal_places=2)
    ride_distance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hosted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='rides_as_host')
    payment_method = models.CharField(max_length=10)
    ride_status = models.CharField(default='requested', max_length=10)
    ride_capacity = models.IntegerField()
    ride_type = models.CharField(max_length=4)
    rider_review = models.IntegerField(default=5)
    host_review = models.IntegerField(default=5)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    start_time = models.DateTimeField(null=True, default=None)
    rider_note = models.CharField(max_length=100, null=True, default=None)
    host_note = models.CharField(max_length=100, null=True, default=None)

    def __str__(self):
        return f"{self.start_loc} to {self.destination}"
    
    def delete_if_requested(self):
        if self.ride_status == 'requested' and timezone.now() > self.created_at + timezone.timedelta(hours=5):
            self.delete()

    @property
    def time_since_creation(self):
        time_diff = timezone.now() - self.created_at
        hours = time_diff.total_seconds() // 3600
        minutes = (time_diff.total_seconds() % 3600) // 60
        if hours==0:
            return f"{int(minutes)} minutes ago"
        return f"{int(hours)} hour(s), {int(minutes)} minutes ago"
    
    @property
    def time_since_updation(self):
        time_diff = timezone.now() - self.updated_at
        hours = time_diff.total_seconds() // 3600
        minutes = (time_diff.total_seconds() % 3600) // 60
        if hours==0:
            return f"{int(minutes)} minutes ago"
        return f"{int(hours)} hour(s), {int(minutes)} minutes ago"
    
    @property
    def time_till_start(self):
        time_diff = self.start_time - timezone.now()
        hours = time_diff.total_seconds() // 3600
        minutes = (time_diff.total_seconds() % 3600) // 60
        if hours == 0:
            return f"{int(minutes)} minutes"
        return f"{int(hours)} hour(s), {int(minutes)} minutes"
    