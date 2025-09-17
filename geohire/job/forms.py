from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'skills', 'salary_range', 'remote_or_onsite', 'visa_sponsorship']
