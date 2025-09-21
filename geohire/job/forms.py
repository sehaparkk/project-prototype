from django import forms
from .models import Application, Job, JobLocation

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['note']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'salary_min', 'salary_max', 'hide_salary', 'remote_or_onsite', 'visa_sponsorship', 'skills']

class JobLocationForm(forms.ModelForm):
    class Meta:
        model = JobLocation
        fields = ['city', 'state', 'zip_code', 'street_address', 'country']

class JobSearchForm(forms.Form):
    title = forms.CharField(required=False)
    skills = forms.CharField(required=False)
    location = forms.CharField(required=False)
    salary_min = forms.IntegerField(required=False)
    salary_max = forms.IntegerField(required=False)
    remote_or_onsite = forms.ChoiceField(choices=[('', 'Any'), ('Remote', 'Remote'), ('Onsite', 'Onsite')], required=False)
    visa_sponsorship = forms.BooleanField(required=False)

class ApplicationUpdateForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'recruiter_note']
