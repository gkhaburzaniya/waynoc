from dal.autocomplete import ModelSelect2Multiple, ModelSelect2
from django import forms

from .models import Movie


class MovieForm(forms.ModelForm):

    class Meta:
        model = Movie
        fields = ['title', 'picker', 'attendees', 'date']
        widgets = {
            'picker': ModelSelect2('movienite:person_autocomplete'),
            'attendees': ModelSelect2Multiple('movienite:person_autocomplete'),
        }
