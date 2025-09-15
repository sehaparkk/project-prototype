from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#this is the jobseeker registration form. The fields in Meta should only have fields for the user model
#other fields are handled in views
class jobseekerCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15, required = False)
    resume = forms.FileField(required = False)
    headline = forms.CharField(widget=forms.Textarea, required = False)
    urls = forms.CharField(widget = forms.Textarea, required= False)
    city = forms.CharField(max_length=100, required = False)
    state = forms.CharField(max_length=100, required = False)
    zip_code = forms.CharField(max_length=20, required = False)
    street_address = forms.CharField(max_length=255, required = False)
    country = forms.CharField(max_length=100, required = False)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')