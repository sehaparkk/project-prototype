from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import JobSeeker
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

# basic show profile view, just takes a slug, finds the jobseeker, and then passes both along
def show_profile(request, slug):
    jobseeker = get_object_or_404(JobSeeker, slug=slug)
    return render(request, 'jobseeker/profile.html', {'slug' : jobseeker.slug, 'jobseeker': jobseeker})

#the register view, passes two HTML POST things (one to handle the form, one for the files)
#and then creates a user and jobseeker object if the form is valid
def register(request):
    if request.method == 'POST':
        form = jobseekerCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            phone = form.cleaned_data.get('phone')
            resume = form.cleaned_data.get('resume')
            headline = form.cleaned_data.get('headline')
            urls = form.cleaned_data.get('urls')

            counter = 0
            slug = slugify(form.cleaned_data.get('first_name'))
            while JobSeeker.objects.filter(slug=slug).exists():
                slug = f"{slug}-{counter}" 
                counter += 1
            #ensures there will always be a numeric character after the slug
            slug = f"{slug}-{counter}-jobseeker"
            JobSeeker.objects.create(
                user = user,
                phone = phone,
                resume = resume,
                headline = headline,
                created_at = user.date_joined,
                updated_at = user.date_joined,
                slug = slug,
                urls = urls,
            )
            return redirect('login')
    else:
        form = jobseekerCreationForm()
    return render(request, 'jobseeker/register.html', {'form': form})

#create view for creating a new location
@login_required
def newLocation(request):
    try:
        if JobSeeker.objects.get(user=request.user).location:
            return redirect('jobseeker_profile', slug=request.user.jobseeker.slug)
    except userLocation.DoesNotExist:
        pass
    if request.method == 'POST':
        form = locationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.jobseeker = JobSeeker.objects.get(user=request.user)
            location.save()
            return redirect('jobseeker_profile', slug=location.jobseeker.slug)
    else:
        form = locationForm()
    return render(request, 'jobseeker/newLocation.html', {'form': form})

#create view for creating new work experience
@login_required
def newWorkExperience(request):
    if request.method == 'POST':
        form = workExperienceForm(request.POST)
        if form.is_valid():
            work = form.save(commit=False)
            work.jobseeker = JobSeeker.objects.get(user=request.user)
            work.save()
            return redirect('jobseeker_profile', slug=work.jobseeker.slug)
    else:
        form = workExperienceForm()
    return render(request, 'jobseeker/newWorkExperience.html', {'form': form})

#create view for creating new education
@login_required
def newEducation(request):
    if request.method == 'POST':
        form = educationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.jobseeker = JobSeeker.objects.get(user=request.user)
            education.save()
            return redirect('jobseeker_profile', slug=education.jobseeker.slug)
    else:
        form = educationForm()
    return render(request, 'jobseeker/newEducation.html', {'form': form})


#deletion views
@login_required
def delete_location(request, pk):
    location = get_object_or_404(userLocation, pk=pk, jobseeker__user=request.user)
    location.delete()
    return redirect('jobseeker_profile', slug=location.jobseeker.slug)

@login_required
def delete_work_experience(request, pk):
    work = get_object_or_404(workExperience, pk=pk, jobseeker__user=request.user)
    work.delete()
    return redirect('jobseeker_profile', slug=work.jobseeker.slug)

@login_required
def delete_education(request, pk):
    education = get_object_or_404(userEducation, pk=pk, jobseeker__user=request.user)
    education.delete()
    return redirect('jobseeker_profile', slug=education.jobseeker.slug)

#define jobseeker homepage view
def jobseeker_homepage(request):
    return render(request, 'jobseeker/jobseekerHomepage.html')