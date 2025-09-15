from django.shortcuts import render
from jobseeker.models import JobSeeker

def homepage(request):
    jobseeker = None
    try:
        if request.user.is_authenticated:
            jobseeker= JobSeeker.objects.get(user=request.user)
    except:
        jobseeker = None
    return render(request, 'base.html', {'jobseeker': jobseeker})

# Create your views here.
