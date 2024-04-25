from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from .forms import *
from django.http import JsonResponse

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
        else:
            messages.success(request, "There was an Error, try loging in again!")
            return redirect('home')
    return render(request, 'home.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out Succesfully!")
    return redirect('home')

   
def register_user(request):
    if request.method=='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        student_id = request.POST.get('student_id')
        phone_number = request.POST.get('phone_number')
        fullname = request.POST.get('fullname')
      
        try:
            if not (email.endswith("@g.bracu.ac.bd") or email.endswith("@bracu.ac.bd")):
                messages.success(request, 'Must be a BRACU G-suite email address!')
                return redirect('/register')
            if User.objects.filter(username=username).first():
                messages.success(request, 'Username is taken!')
                return redirect('/register')
            
            if User.objects.filter(email=email).first():
                messages.success(request, 'There already exists an account with this email!')
                return redirect('/register')
            
            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj,
                                                 auth_token = auth_token,
                                                 fullname=fullname,
                                                 student_id=student_id,
                                                 phone_number=phone_number)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)

    return render(request, 'register.html')

def success(request):
    return render(request, 'success.html')

def token_sent(request):
    return render(request, 'token_sent.html')

def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified!')
                return redirect('/')
            profile_obj.is_verified=True
            profile_obj.save()
            messages.success(request, 'Your account has been verified successfully.')
            return redirect('/')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)

def error_page(request):
    return render(request, 'error_page.html')


def send_mail_after_registration(email, token):
    subject = "Your account needs to be verified"
    message = f'Hi, follow this link to verify your STuber account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

def send_mail_to_approve_vehicle(subject):
    subject = subject
    message = f'An user has registered a vehicle with this registration paper, please take a look and verify from admin panel. Link to admin panel: http://127.0.0.1:8000/admin'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['mehedihtanvir@gmail.com']
    send_mail(subject, message, email_from, recipient_list)

def vehicle_registration(request):
    if request.method == 'POST':
        current_user_profile = request.user.profile
        form = VehicleForm(request.POST, request.FILES)
        
        if form.is_valid():
            new_vehicle = form.save(commit=False)
            new_vehicle.host = current_user_profile
            new_vehicle.save()

            subject = "A new vehicle awaiting approval"
            send_mail_to_approve_vehicle(subject)
            messages.success(request, "Vehicle registered successfully! Wait for Approval")
            return redirect('/')
        else:
            messages.error(request, "Form validation failed!")

    else:
        form = VehicleForm()
        
    return render(request, 'vehicle_registration.html', {'form': form})



def send_mail_to_approve_dl(subject):
    subject = subject
    message = f'An user has registered a DL with DL paper, please take a look and verify from admin panel. Link to admin panel: http://127.0.0.1:8000/admin'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['mehedihtanvir@gmail.com']
    send_mail(subject, message, email_from, recipient_list)


def dl_registration(request):
    if request.method == 'POST':
        current_user_profile = request.user.profile
        form = DLForm(request.POST, request.FILES)
        
        if form.is_valid():
            new_dl = form.save(commit=False)
            new_dl.host = current_user_profile
            new_dl.save()

            subject = "A new DL needs approval"
            send_mail_to_approve_dl(subject)
            messages.success(request, "DL registered successfully! Wait for Approval")
            return redirect('/')
        else:
            messages.error(request, "Form validation failed!")

    else:
        form = DLForm()
        
    return render(request, 'driver_registration.html', {'form': form})



def cost_estimate(request):
    if 'term' in request.GET:
        qs = Location.objects.filter(location_name__istartswith=request.GET.get('term'))
        lnames = list()
        for loca in qs:
            lnames.append(loca.location_name)
        return JsonResponse(lnames, safe=False)

    return render(request, 'cost_estimate.html')


def ridebracu(request):
    if 'term' in request.GET:
        qs = Location.objects.filter(location_name__istartswith=request.GET.get('term'))
        lnames = list()
        for loca in qs:
            lnames.append(loca.location_name)
        return JsonResponse(lnames, safe=False)
    
    if request.method == 'POST':
        form = RideForm(request.POST, request.FILES)
        
        if form.is_valid():
            new_ride = form.save(commit=False)
            new_ride.rider = request.user
            new_ride.riderpays = ride_cost(new_ride.start_loc, new_ride.destination, new_ride.ride_type, new_ride.ride_capacity)
            new_ride.save()
            
            return redirect('ride_monitor', ride_id=new_ride.pk)
        else:
            messages.error(request, "Form validation failed!")

    else:
        form = RideForm()
        
    return render(request, 'from_bracu.html', {'form': form})


def tobracu(request):
    if 'term' in request.GET:
        qs = Location.objects.filter(location_name__istartswith=request.GET.get('term'))
        lnames = list()
        for loca in qs:
            lnames.append(loca.location_name)
        return JsonResponse(lnames, safe=False)
    
    if request.method == 'POST':
        current_user_profile = request.user.profile
        form = RideForm(request.POST, request.FILES)
        
        if form.is_valid():
            new_ride = form.save(commit=False)
            new_ride.rider = current_user_profile
            new_ride.riderpays = ride_cost(new_ride.start_loc, new_ride.destination, new_ride.ride_type, new_ride.ride_capacity)
            new_ride.save()
            
            return redirect('ride_monitor', ride_id=new_ride.pk)
        else:
            messages.error(request, "Form validation failed!")

    else:
        form = RideForm()
        
    return render(request, 'to_bracu.html', {'form': form})


def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="distance_calculator")
    location = geolocator.geocode(location_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None

def calculate_distance(location1_name, location2_name):
    location1_coords = get_coordinates(location1_name)
    location2_coords = get_coordinates(location2_name)

    if location1_coords and location2_coords:
        distance = geodesic(location1_coords, location2_coords).kilometers
        return distance
    else:
        return None


def ride_cost(start_loc, destination, r_type, r_capacity):

    r_distance = calculate_distance(start_loc, destination)
    if r_type == "bike":
        r_cost = r_distance*30
    else:
        if r_capacity < 4:
            r_cost = r_distance*80
        else:
            r_cost = r_distance*r_capacity*30

    return r_cost




def ride_created(request, ride_id):
    return redirect('ride_monitor', ride_id=ride_id)

def ride_monitor(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    form = BookRideForm(request.POST or None, user=request.user)

    if (ride.ride_status == 'scheduled') and (request.method == 'POST' and form.is_valid()):
        ride.rider = request.user
        ride.ride_status = 'accepted'
        ride.save()

        host_email = ride.hosted_by.email
        rider_name = ride.rider.profile.fullname
        rider_phone_number = ride.rider.profile.phone_number
        ride_url = request.build_absolute_uri(reverse('ride_details', kwargs={'ride_id': ride_id}))
        send_mail_ride_booked(host_email, rider_name, rider_phone_number, ride_url)

        return redirect('ride_monitor', ride_id=ride_id)
    
    if ride.ride_status != 'scheduled' and request.method == 'POST':
        form = HostReviewForm(request.POST)
        if form.is_valid():
            ride.host_review = form.cleaned_data['host_review']
            ride.save()
            return redirect('/')
    else:
        form = HostReviewForm()
    return render(request, 'ride_monitor.html', {'ride': ride, 'form': form})


def send_mail_ride_booked(email, rider, rider_phone, ride_url):
    subject = f"{rider} has booked your scheduled ride"
    message = f'{rider} has booked your scheduled ride, to contact here is his/her/their phone number: {rider_phone}\nView Ride: {ride_url}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def requested_rides(request):
    requested_rides = Ride.objects.filter(ride_status='requested').order_by('-created_at')

    ride_type = request.GET.get('ride_type')

    if ride_type:
        if ride_type == 'both':
            pass
        else:
            requested_rides = requested_rides.filter(ride_type=ride_type)

    return render(request, 'requested_rides.html', {'requested_rides': requested_rides})



def ride_details(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    form = AcceptRideForm(request.POST or None, user=request.user)
    
    if (ride.ride_status == 'requested') and (request.method == 'POST' and form.is_valid()):
        ride.hosted_by = request.user
        ride.ride_status = 'accepted'
        ride.save()

        rider_email = ride.rider.email
        host_name = ride.hosted_by.profile.fullname
        host_phone_number = ride.hosted_by.profile.phone_number
        send_mail_ride_accepted(rider_email, host_name, host_phone_number)

        return redirect('ride_details', ride_id=ride_id)
    
    if not ride.ride_status == 'scheduled':
        rider_phone_number = ride.rider.profile.phone_number

        return render(request, 'ride_details.html', {'ride': ride, 'form': form, 'rider_phone_number': rider_phone_number})

    else:
        return render(request, 'ride_details.html', {'ride': ride, 'form': form})



def send_mail_ride_accepted(email, host, host_phone):
    subject = f"{host} has accepted your ride request"
    message = f'{host} has accepted your ride request, to contact here is his/her/their phone number: {host_phone}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

def start_ride(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    ride.ride_status = 'started'
    ride.save()
    return redirect('ride_details', ride_id=ride_id)

def end_ride(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    if request.method == 'POST':
        form = RideReviewForm(request.POST)
        if form.is_valid():
            ride.rider_review = form.cleaned_data['rider_review']
            ride.ride_status = 'ended'
            ride.save()
            return redirect('ride_details', ride_id=ride_id)
    else:
        form = RideReviewForm()
    return render(request, 'end_ride.html', {'form': form})



def schridebracu(request):
    if 'term' in request.GET:
        qs = Location.objects.filter(location_name__istartswith=request.GET.get('term'))
        lnames = list()
        for loca in qs:
            lnames.append(loca.location_name)
        return JsonResponse(lnames, safe=False)
    
    if request.method == 'POST':
        form = RideForm(request.POST, request.FILES)
        
        if form.is_valid():
            new_ride = form.save(commit=False)
            new_ride.hosted_by = request.user
            new_ride.ride_status = 'scheduled'
            new_ride.riderpays = ride_cost(new_ride.start_loc, new_ride.destination, new_ride.ride_type, new_ride.ride_capacity)
            new_ride.save()
            
            return redirect('ride_details', ride_id=new_ride.pk)
        else:
            messages.error(request, "Form validation failed!")

    else:
        form = RideForm()
        
    return render(request, 'schedule_from_bracu.html', {'form': form})




def scheduled_rides(request):
    scheduled_rides = Ride.objects.filter(ride_status='scheduled').order_by('start_time')

    ride_type = request.GET.get('ride_type')

    if ride_type:
        if ride_type == 'both':
            pass
        else:
            scheduled_rides = scheduled_rides.filter(ride_type=ride_type)

    return render(request, 'scheduled_rides.html', {'scheduled_rides': scheduled_rides})




