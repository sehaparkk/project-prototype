from django import forms
from .models import Job, JobLocation

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "description", "salary_min", "salary_max", "hide_salary",
                  "remote_or_onsite", "visa_sponsorship", "skills"]

class JobLocationForm(forms.ModelForm):
    class Meta:
        model = JobLocation
        fields = ["country", "state", "city", "zip_code", "street_address"]
