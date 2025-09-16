from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

#this is the recruiter registration form. The fields in Meta should only have fields for the user model
#other fields are handled in views
class recruiterCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15, required = False)
    headline = forms.CharField(widget=forms.Textarea, required = False)
    urls = forms.CharField(widget = forms.Textarea, required= False)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

#create forms for the subfields for jobseeker
class locationForm(forms.ModelForm):
    class Meta:
        model = userLocation
        fields = ('city', 'state', 'zip_code', 'street_address', 'country')

class educationForm(forms.ModelForm):
    class Meta:
        model = userEducation
        fields = ('institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'GPA', 'description')

class workExperienceForm(forms.ModelForm):
    class Meta:
        model = workExperience
        fields = ('company', 'position', 'start_date', 'end_date', 'description')