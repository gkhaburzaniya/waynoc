from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from .models import Movie


class MovieForm(forms.ModelForm):
    other_attendees = forms.CharField(required=False)

    class Meta:
        model = Movie
        fields = ['title', 'picker', 'attendees']
        widgets = {
            'attendees': CheckboxSelectMultiple()
        }
