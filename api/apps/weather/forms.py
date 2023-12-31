from django import forms
from .models import Location

class WeatherQueryForm(forms.Form):
    location = forms.CharField(max_length=100)
    date = forms.DateField(
        widget=forms.SelectDateWidget(attrs={'id': 'date-input'}),
        label="Date"
    )
    hour = forms.ChoiceField(
        choices=[('', '----')] + [(str(i).zfill(2), str(i).zfill(2)) for i in range(24)],
        required=False,
        widget=forms.Select(attrs={'id': 'hour-input'}),
        label="Hour"
    )


