from django import forms
from .models import Location

class WeatherQueryForm(forms.Form):
    location = forms.ModelChoiceField(queryset=Location.objects.all(), label="Location")
    date = forms.DateField(widget=forms.SelectDateWidget(), label="Date")
    hour = forms.ChoiceField(choices=[(str(i).zfill(2), str(i).zfill(2)) for i in range(24)], required=False, label="Hour")

