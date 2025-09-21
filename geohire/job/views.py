from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Application
from .forms import JobForm, JobLocationForm, ApplicationForm, JobSearchForm
from django.contrib.auth.decorators import login_required
from jobseeker.models import JobSeeker
from django.db.models import Q
from geopy.geocoders import Nominatim
from django.http import JsonResponse
import json

def job_list(request):
    jobs = Job.objects.all()
    form = JobSearchForm(request.GET)

    if form.is_valid():
        title = form.cleaned_data.get('title')
        skills = form.cleaned_data.get('skills')
        location = form.cleaned_data.get('location')
        salary_min = form.cleaned_data.get('salary_min')
        salary_max = form.cleaned_data.get('salary_max')
        remote_or_onsite = form.cleaned_data.get('remote_or_onsite')
        visa_sponsorship = form.cleaned_data.get('visa_sponsorship')

        if title:
            jobs = jobs.filter(title__icontains=title)
        if skills:
            skill_list = [s.strip() for s in skills.split(',')]
            jobs = jobs.filter(skills__name__in=skill_list).distinct()
        if location:
            jobs = jobs.filter(
                Q(location__city__icontains=location) |
                Q(location__state__icontains=location) |
                Q(location__country__icontains=location)
            )
        if salary_min:
            jobs = jobs.filter(salary_min__gte=salary_min)
        if salary_max:
            jobs = jobs.filter(salary_max__lte=salary_max)
        if remote_or_onsite:
            jobs = jobs.filter(remote_or_onsite=remote_or_onsite)
        if visa_sponsorship:
            jobs = jobs.filter(visa_sponsorship=visa_sponsorship)

    return render(request, "job/job_list.html", {"jobs": jobs, "form": form})

@login_required
def create_job(request):
    if request.method == "POST":
        job_form = JobForm(request.POST)
        location_form = JobLocationForm(request.POST)
        if job_form.is_valid() and location_form.is_valid():
            job = job_form.save(commit=False)
            job.recruiter = request.user.recruiter
            job.save()
            job_form.save_m2m()
            location = location_form.save(commit=False)
            location.job = job
            
            address = f"{location_form.cleaned_data.get('street_address')}, {location_form.cleaned_data.get('city')}, {location_form.cleaned_data.get('state')}, {location_form.cleaned_data.get('zip_code')}, {location_form.cleaned_data.get('country')}"
            geolocator = Nominatim(user_agent="geohire_app")
            try:
                geolocation = geolocator.geocode(address)
                if geolocation:
                    location.latitude = geolocation.latitude
                    location.longitude = geolocation.longitude
            except:
                pass # Or handle the error

            location.save()
            return redirect("job_list")
    else:
        job_form = JobForm()
        location_form = JobLocationForm()
    return render(request, "job/create_job.html", {"job_form": job_form, "location_form": location_form})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == "POST":
        job_form = JobForm(request.POST, instance=job)
        location_form = JobLocationForm(request.POST, instance=job.location)
        if job_form.is_valid() and location_form.is_valid():
            job = job_form.save(commit=False)
            job.save()
            job_form.save_m2m()
            
            location = location_form.save(commit=False)
            
            address = f"{location_form.cleaned_data.get('street_address')}, {location_form.cleaned_data.get('city')}, {location_form.cleaned_data.get('state')}, {location_form.cleaned_data.get('zip_code')}, {location_form.cleaned_data.get('country')}"
            geolocator = Nominatim(user_agent="geohire_app")
            try:
                geolocation = geolocator.geocode(address)
                if geolocation:
                    location.latitude = geolocation.latitude
                    location.longitude = geolocation.longitude
            except:
                pass # Or handle the error

            location.save()
            return redirect("job_list")
    else:
        job_form = JobForm(instance=job)
        location_form = JobLocationForm(instance=job.location)
    return render(request, "job/edit_job.html", {"job_form": job_form, "location_form": location_form})

@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    jobseeker = get_object_or_404(JobSeeker, user=request.user)

    if Application.objects.filter(job=job, jobseeker=jobseeker).exists():
        # User has already applied for this job
        return redirect('job_list') # Or show a message

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.jobseeker = jobseeker
            application.save()
            return redirect('job_list') # Or a confirmation page
    else:
        form = ApplicationForm()

    return render(request, 'job/apply_for_job.html', {'form': form, 'job': job})

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job/job_detail.html', {'job': job})

def job_map(request):
    jobs = Job.objects.filter(location__latitude__isnull=False, location__longitude__isnull=False)
    job_data = []
    for job in jobs:
        job_data.append({
            'title': job.title,
            'lat': job.location.latitude,
            'lng': job.location.longitude,
            'url': job.get_absolute_url()
        })
    
    return render(request, 'job/job_map.html', {'job_data': json.dumps(job_data)})