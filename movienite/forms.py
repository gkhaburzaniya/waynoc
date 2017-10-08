from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

from .models import Movie


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'picker', 'attendees']
        widgets = {
            'attendees': CheckboxSelectMultiple()
        }
