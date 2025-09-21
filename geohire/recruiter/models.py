from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#JobSeeker class to hold data for the jobseeker
class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #unique, non important field to use to search for jobSeekers without exposing the id to the web
    #consists on name + number of other people with that name
    slug = models.SlugField(unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    headline = models.CharField(max_length=255, blank=True, null=True)
    urls = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.slug
    
class userLocation(models.Model):
    recruiter = models.OneToOneField(Recruiter, on_delete=models.CASCADE, related_name='location')
    city = models.CharField(max_length=100,  blank=True, null=True)
    state = models.CharField(max_length=100,  blank=True, null=True)
    zip_code = models.CharField(max_length=20,  blank=True, null=True)
    street_address = models.CharField(max_length=255,  blank=True, null=True)
    country = models.CharField(max_length=100,  blank=True, null=True)
    latitude = models.FloatField(blank = True, null = True)
    longitude = models.FloatField(blank = True, null = True)
    
    def __str__(self):
        return f"{self.recruiter.slug} - {self.country} at {self.zip_code}" 

#creates a class for user eduction that holds information about the users education
#this is linked to a user with a foreign key, meaning it belongs to the user even though
#it isnt delcared in the user/JobSeeker class (I swear Django is so weird)
class userEducation(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    GPA = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.recruiter.slug} - {self.degree} at {self.institution}" 

#creates a work experience class in the same manner as user education
class workExperience(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='work_experiences')
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.recruiter.slug} - {self.position} at {self.company}"

class SavedSearch(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='saved_searches')
    name = models.CharField(max_length=255)
    skills = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    projects = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} by {self.recruiter.user.username}'