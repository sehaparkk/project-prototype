from django.shortcuts import render

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = "Job"
    return render(request, "job/index.html", {"template_data": template_data})
    
def job_list(request):
    jobs = Job.objects.all().order_by('-posted_at')
    return render(request, 'job/job_list.html', {'jobs': jobs})

def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'job/create_job.html', {'form': form})

def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobForm(instance=job)
    return render(request, 'job/edit_job.html', {'form': form})
