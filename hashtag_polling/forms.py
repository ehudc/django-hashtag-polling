from django import forms
from .models import DateForm

class DateForm(forms.ModelForm):
    class Meta:
        model = DateForm
        widgets = {
            'date' : forms.DateInput(attrs={'type':'date'})
        }
        exclude = []