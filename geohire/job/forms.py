from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title',
            'description',
            'salary_min',
            'salary_max',
            'hide_salary',
            'remote_or_onsite',
            'visa_sponsorship',
            'skills'
        ]
