from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('token/', views.token_sent, name='token'),
    path('success/', views.success, name='success'),
    path('verify/<auth_token>', views.verify, name='verify'),
    path('error/', views.error_page, name='error'),
    path('vehicle_registration/', views.vehicle_registration, name='vehicle_registration'),
    path('dl_registration/', views.dl_registration, name='dl_registration'),
    path('cost_estimate/', views.cost_estimate, name='cost_estimate'),
    path('from_bracu/', views.ridebracu, name='from_bracu'),
    path('to_bracu/', views.tobracu, name='to_bracu'),
    path('ride_requests/', views.requested_rides, name='requested_rides'),
    path('ride/<int:ride_id>/', views.ride_details, name='ride_details'),
    path('ride/<int:ride_id>/start/', views.start_ride, name='start_ride'),
    path('ride/<int:ride_id>/end/', views.end_ride, name='end_ride'),
    path('ride_created/<int:ride_id>/', views.ride_created, name='ride_created'),
    path('ride_monitor/<int:ride_id>/', views.ride_monitor, name='ride_monitor'),
]
