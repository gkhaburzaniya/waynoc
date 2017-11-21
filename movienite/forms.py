from django import forms

from .models import Movie, Person


class MovieForm(forms.ModelForm):
    picker = forms.ModelChoiceField(Person.objects.all(), empty_label=None)
    attendees = forms.ModelMultipleChoiceField(Person.objects.all(), to_field_name='name')

    def __init__(self, *args, **kwargs):
        self.new_attendees = set()
        super().__init__(*args, **kwargs)

    def pre_clean_attendees(self):
        attendees = self.data.getlist('attendees')
        for attendee in attendees:
            if not Person.objects.filter(name=attendee).exists():
                self.new_attendees.add(attendee)
                attendees.remove(attendee)
        self.data = self.data.copy()
        self.data.setlist('attendees', attendees)

    def full_clean(self):
        if self.is_bound:
            self.pre_clean_attendees()
        super().full_clean()

    def save(self, *args, **kwargs):
        for attendee in self.new_attendees:
            Person(name=attendee).save()
            self.cleaned_data['attendees'] |= Person.objects.filter(name=attendee)
        return super().save(*args, **kwargs)

    class Meta:
        model = Movie
        fields = ['title', 'date', 'picker', 'attendees']
