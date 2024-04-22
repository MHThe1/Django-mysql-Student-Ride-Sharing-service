from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail


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


from .models import Vehicle

def vehicle_registration(request):
    if request.method == 'POST':
        current_user_profile = request.user.profile
        
        vehicle_type = request.POST.get('vehicle_type')
        vehicle_model = request.POST.get('vehicle_model')
        vehicle_reg = request.POST.get('vehicle_reg')
        vehicle_capacity = request.POST.get('vehicle_capacity')
        vehicle_color = request.POST.get('vehicle_color')
        
        try:
            new_vehicle = Vehicle.objects.create(
                host=current_user_profile,
                vehicle_type=vehicle_type,
                vehicle_model=vehicle_model,
                vehicle_reg=vehicle_reg,
                vehicle_capacity=vehicle_capacity,
                vehicle_color=vehicle_color
            )
            new_vehicle.save()

            messages.success(request, "Vehicle registered successfully!")

            return redirect('/')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

            return redirect('/vehicle_registration')
        
    return render(request, 'vehicle_registration.html')
