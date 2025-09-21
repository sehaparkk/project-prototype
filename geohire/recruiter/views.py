from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import Recruiter
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from jobseeker.models import JobSeeker
from geopy.geocoders import Nominatim

# basic show profile view, just takes a slug, finds the jobseeker, and then passes both along
def show_profile(request, slug):
    recruiter = get_object_or_404(Recruiter, slug=slug)
    return render(request, 'recruiter/profile.html', {'slug' : recruiter.slug, 'recruiter': recruiter})

#the register view, passes two HTML POST things (one to handle the form, one for the files)
#and then creates a user and jobseeker object if the form is valid
def register(request):
    if request.method == 'POST':
        form = recruiterCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            phone = form.cleaned_data.get('phone')
            headline = form.cleaned_data.get('headline')
            urls = form.cleaned_data.get('urls')

            counter = 0
            slug = slugify(form.cleaned_data.get('first_name'))
            while Recruiter.objects.filter(slug=slug).exists():
                slug = f"{slug}-{counter}" 
                counter += 1
            #ensures there will always be a numeric character after the slug
            slug = f"{slug}-{counter}-recruiter"
            Recruiter.objects.create(
                user = user,
                phone = phone,
                headline = headline,
                created_at = user.date_joined,
                updated_at = user.date_joined,
                slug = slug,
                urls = urls,
            )
            return redirect('login')
    else:
        form = recruiterCreationForm()
    return render(request, 'recruiter/register.html', {'form': form})

def map(request):
    jobseekers = JobSeeker.objects.all()
    #you have to do json cause js :(:(
    jobseeker_data = [
        {
            'firstName' : jobseeker.user.first_name,
            'lat' : jobseeker.location.latitude if jobseeker.location else None,
            'lng' : jobseeker.location.longitude if jobseeker.location else None,
        }
        for jobseeker in jobseekers
    ]
    return render (request, 'recruiter/map.html', {'jobseekers_data' : jobseeker_data})

#create view for creating a new location
@login_required
def newLocation(request):
    try:
        if Recruiter.objects.get(user=request.user).location:
            return redirect('recruiter_profile', slug=request.user.recruiter.slug)
    except userLocation.DoesNotExist:
        pass
    if request.method == 'POST':
        form = locationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.recruiter = Recruiter.objects.get(user=request.user)
            address = f"{form.cleaned_data.get('street_address')}, {form.cleaned_data.get('city')}, {form.cleaned_data.get('state')}, {form.cleaned_data.get('zip_code')}, {form.cleaned_data.get('country')}"
            lat, lng = geocode_address(address)
            location.latitude = lat
            location.latitude = lng
            location.save()
            return redirect('recruiter_profile', slug=location.recruiter.slug)
    else:
        form = locationForm()
    return render(request, 'recruiter/newLocation.html', {'form': form})

#create view for creating new work experience
@login_required
def newWorkExperience(request):
    if request.method == 'POST':
        form = workExperienceForm(request.POST)
        if form.is_valid():
            work = form.save(commit=False)
            work.recruiter = Recruiter.objects.get(user=request.user)
            work.save()
            return redirect('recruiter_profile', slug=work.recruiter.slug)
    else:
        form = workExperienceForm()
    return render(request, 'recruiter/newWorkExperience.html', {'form': form})

#create view for creating new education
@login_required
def newEducation(request):
    if request.method == 'POST':
        form = educationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.recruiter = Recruiter.objects.get(user=request.user)
            education.save()
            return redirect('recruiter_profile', slug=education.recruiter.slug)
    else:
        form = educationForm()
    return render(request, 'recruiter/newEducation.html', {'form': form})


#deletion views
@login_required
def delete_location(request, pk):
    location = get_object_or_404(userLocation, pk=pk, recruiter__user=request.user)
    location.delete()
    return redirect('recruiter_profile', slug=location.recruiter.slug)

@login_required
def delete_work_experience(request, pk):
    work = get_object_or_404(workExperience, pk=pk, recruiter__user=request.user)
    work.delete()
    return redirect('recruiter_profile', slug=work.recruiter.slug)

@login_required
def delete_education(request, pk):
    education = get_object_or_404(userEducation, pk=pk, recruiter__user=request.user)
    education.delete()
    return redirect('recruiter_profile', slug=education.recruiter.slug)

#define recruiter homepage view
def recruiter_homepage(request):
    return render(request, 'recruiter/recruiterHomepage.html')