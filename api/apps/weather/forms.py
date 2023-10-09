from django import forms
from .models import Location

class WeatherQueryForm(forms.Form):
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        label='Location',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    hour = forms.ChoiceField(
        choices=[('', 'All Hours')] + [(i, f"{i:02d}:00") for i in range(24)],
        required=False,
        label='Hour',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
