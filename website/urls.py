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
]
