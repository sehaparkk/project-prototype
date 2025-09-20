from django.shortcuts import render, redirect, get_object_or_404
from .models import Job
from .forms import JobForm, JobLocationForm

def job_list(request):
    jobs = Job.objects.all()
    return render(request, "job/job_list.html", {"jobs": jobs})

def create_job(request):
    if request.method == "POST":
        job_form = JobForm(request.POST)
        location_form = JobLocationForm(request.POST)
        if job_form.is_valid() and location_form.is_valid():
            job = job_form.save()
            location = location_form.save(commit=False)
            location.job = job
            location.save()
            job_form.save_m2m()
            return redirect("job_list")
    else:
        job_form = JobForm()
        location_form = JobLocationForm()
    return render(request, "job/create_job.html", {"job_form": job_form, "location_form": location_form})

def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == "POST":
        job_form = JobForm(request.POST, instance=job)
        location_form = JobLocationForm(request.POST, instance=job.location)
        if job_form.is_valid() and location_form.is_valid():
            job_form.save()
            location_form.save()
            job_form.save_m2m()
            return redirect("job_list")
    else:
        job_form = JobForm(instance=job)
        location_form = JobLocationForm(instance=job.location)
    return render(request, "job/edit_job.html", {"job_form": job_form, "location_form": location_form})
