from django.urls import path 
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('profile/<str:username>/', views.viewprofile, name='view_profile'),
    path('token/', views.token_sent, name='token'),
    path('success/', views.success, name='success'),
    path('verify/<auth_token>', views.verify, name='verify'),
    path('verificaiton_required/', views.verification_required, name='verification_required'),
    path('error/', views.error_page, name='error'),
    path('vehicle_registration/', views.vehicle_registration, name='vehicle_registration'),
    path('dl_registration/', views.dl_registration, name='dl_registration'),
    path('become_host/', views.become_host, name='become_host'),
    path('inspect_host_status/<str:username>/', views.inspect_host_status, name='inspect_host_status'),
    path('approve_bike_host/<str:username>/', views.approve_bike_host, name='approve_bike_host'),
    path('approve_car_host/<str:username>/', views.approve_car_host, name='approve_car_host'),
    path('book_ride/', views.bookride, name='book_ride'),
    path('from_bracu/', views.ridebracu, name='from_bracu'),
    path('to_bracu/', views.tobracu, name='to_bracu'),
    path('ride_requests/', views.requested_rides, name='requested_rides'),
    path('ride/<int:ride_id>/', views.ride_details, name='ride_details'),
    path('ride/<int:ride_id>/start/', views.start_ride, name='start_ride'),
    path('ride/<int:ride_id>/end/', views.end_ride, name='end_ride'),
    path('ride_created/<int:ride_id>/', views.ride_created, name='ride_created'),
    path('ride_monitor/<int:ride_id>/', views.ride_monitor, name='ride_monitor'),
    path('schedule_ride/', views.scheduleride, name='schedule_ride'),
    path('schedule_from_bracu/', views.schridebracu, name='schedule_from_bracu'),
    path('schedule_to_bracu/', views.schtobracu, name='schedule_to_bracu'),
    path('scheduled_rides/', views.scheduled_rides, name='scheduled_rides'),
    path('ride/<int:ride_id>/delete/', views.delete_ride, name='delete_ride'),
    path('rides_taken/', views.rides_taken, name='rides_taken'),
    path('rides_hosted/', views.rides_hosted, name='rides_hosted'),
    path('rides_ongoing/', views.rides_ongoing, name='rides_ongoing'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

]
