from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_type', 'vehicle_model', 'vehicle_reg', 'vehicle_capacity', 'vehicle_color', 'registration_paper']
