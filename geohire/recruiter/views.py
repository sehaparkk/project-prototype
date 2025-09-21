from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import Recruiter, SavedSearch
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from jobseeker.models import JobSeeker
from geopy.geocoders import Nominatim
from django.db.models import Q
import json
from job.models import Application, Job
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from job.forms import ApplicationUpdateForm

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
    jobseekers = JobSeeker.objects.filter(
        location__latitude__isnull=False, 
        location__longitude__isnull=False
    ).filter(
        Q(privacy_setting='Public') | Q(privacy_setting='Recruiters Only')
    )
    
    jobseeker_data = []
    for jobseeker in jobseekers:
        jobseeker_data.append({
            'firstName': jobseeker.user.first_name,
            'lat': jobseeker.location.latitude,
            'lng': jobseeker.location.longitude,
            'slug': jobseeker.slug # To link to their profile
        })
    
    return render(request, 'recruiter/map.html', {'jobseekers_data': json.dumps(jobseeker_data)})

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

@login_required
def search_jobseekers(request):
    form = JobSeekerSearchForm(request.GET)
    jobseekers = JobSeeker.objects.all()

    # Filter based on privacy settings
    jobseekers = jobseekers.filter(
        Q(privacy_setting='Public') | Q(privacy_setting='Recruiters Only')
    )

    if form.is_valid():
        skills = form.cleaned_data.get('skills')
        location = form.cleaned_data.get('location')
        projects = form.cleaned_data.get('projects')

        if skills:
            skill_list = [s.strip() for s in skills.split(',')]
            jobseekers = jobseekers.filter(skills__name__in=skill_list).distinct()

        if location:
            jobseekers = jobseekers.filter(
                Q(location__city__icontains=location) |
                Q(location__state__icontains=location) |
                Q(location__country__icontains=location)
            )

        if projects:
            jobseekers = jobseekers.filter(work_experiences__description__icontains=projects).distinct()

    return render(request, 'recruiter/search_results.html', {'form': form, 'jobseekers': jobseekers})

#define recruiter homepage view
def recruiter_homepage(request):
    return render(request, 'recruiter/recruiterHomepage.html')

@login_required
def pipeline(request):
    recruiter = get_object_or_404(Recruiter, user=request.user)
    
    # Get all jobs posted by this recruiter
    recruiter_jobs = Job.objects.filter(recruiter=recruiter)
    
    # Get all applications for these jobs
    applications = Application.objects.filter(job__in=recruiter_jobs).order_by('status')

    # Organize applications by status
    pipeline_data = {
        'Applied': [],
        'Review': [],
        'Interview': [],
        'Offer': [],
        'Closed': [],
    }
    for app in applications:
        if app.status in pipeline_data:
            pipeline_data[app.status].append(app)
    
    return render(request, 'recruiter/pipeline.html', {'pipeline_data': pipeline_data})

@require_POST
def update_application_status(request, pk):
    application = get_object_or_404(Application, pk=pk)
    form = ApplicationUpdateForm(request.POST, instance=application)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
def save_search(request):
    if request.method == 'POST':
        form = SaveSearchForm(request.POST)
        if form.is_valid():
            saved_search = form.save(commit=False)
            saved_search.recruiter = get_object_or_404(Recruiter, user=request.user)
            saved_search.save()
            return redirect('list_saved_searches') # Redirect to saved searches list
    # If GET request or form is invalid, render the search results page with the form
    # This assumes the save_search view is accessed from the search_results page
    # You might need to pass the search results back to this view
    return redirect('search_jobseekers') # Redirect back to search results

@login_required
def list_saved_searches(request):
    recruiter = get_object_or_404(Recruiter, user=request.user)
    saved_searches = SavedSearch.objects.filter(recruiter=recruiter)
    return render(request, 'recruiter/list_saved_searches.html', {'saved_searches': saved_searches})

@login_required
def candidate_recommendations(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter__user=request.user)
    job_skills = job.skills.all()
    
    recommended_jobseekers = JobSeeker.objects.none() # Start with an empty queryset

    if job_skills.exists():
        # Find job seekers that share at least one skill with the job
        for skill in job_skills:
            recommended_jobseekers |= JobSeeker.objects.filter(skills=skill)
        
        # Filter based on privacy settings
        recommended_jobseekers = recommended_jobseekers.filter(
            Q(privacy_setting='Public') | Q(privacy_setting='Recruiters Only')
        ).distinct()

    return render(request, 'recruiter/candidate_recommendations.html', {'job': job, 'recommended_jobseekers': recommended_jobseekers})