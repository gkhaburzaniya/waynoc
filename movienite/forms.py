from django import forms

from .models import Movie, Person


class MovieForm(forms.ModelForm):
    picker = forms.ModelChoiceField(Person.objects.all(), empty_label=None, to_field_name='name')
    attendees = forms.ModelMultipleChoiceField(Person.objects.all(), to_field_name='name')

    def __init__(self, *args, **kwargs):
        self.new_attendees = set()
        return super().__init__(*args, **kwargs)

    def pre_clean_attendees(self):
        attendees = self.data.getlist('attendees')
        for attendee in attendees:
            if not Person.objects.filter(name=attendee).exists():
                self.new_attendees.add(attendee)
                attendees.remove(attendee)
        self.data = self.data.copy()
        self.data.setlist('attendees', attendees)

    def full_clean(self, *args, **kwargs):
        if self.is_bound:
            self.pre_clean_attendees()
        return super().full_clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        for attendee in self.new_attendees:
            Person(name=attendee).save()
            self.cleaned_data['attendees'] |= Person.objects.filter(name=attendee)
        original_attendees = [attendee
                              for attendee in self.instance.attendees.all()
                              if self.instance.id]
        retval = super().save(*args, **kwargs)
        for attendee in self.cleaned_data['attendees']:
            attendee.update_score()
        for attendee in original_attendees:
            attendee.update_score()
        return retval

    class Meta:
        model = Movie
        fields = ['title', 'date', 'picker', 'attendees']
