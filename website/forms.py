from django import forms
from .models import *

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_type', 'vehicle_model', 'vehicle_reg', 'vehicle_capacity', 'vehicle_color', 'registration_paper']


class DLForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['dl_type', 'is_that_host', 'dl_reg', 'driver_name', 'dl_paper']
