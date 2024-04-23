from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from .forms import *

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