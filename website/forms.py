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


class RideForm(forms.ModelForm):
    rider_note = forms.CharField(required=False)
    host_note = forms.CharField(required=False)
    start_time = forms.DateTimeField(required=False)
    class Meta:
        model = Ride
        fields = ['start_loc', 'destination', 'ride_type', 'ride_capacity', 'payment_method', 'rider_note', 'host_note', 'start_time']

class AcceptRideForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AcceptRideForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(AcceptRideForm, self).clean()
        return cleaned_data
    

class BookRideForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(BookRideForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(BookRideForm, self).clean()
        return cleaned_data



class RideReviewForm(forms.Form):
    rider_review = forms.ChoiceField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    
class HostReviewForm(forms.Form):
    host_review = forms.ChoiceField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
                                     widget=forms.Select(attrs={'class': 'form-control'}))