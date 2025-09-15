from django.shortcuts import render
from jobseeker.models import JobSeeker

#defines homepage view, passes a jobseeker object if the user is logged in
#this will need to be updated once we add an employer model
def homepage(request):
    jobseeker = None
    try:
        if request.user.is_authenticated:
            jobseeker= JobSeeker.objects.get(user=request.user)
    except:
        jobseeker = None
    return render(request, 'base.html', {'jobseeker': jobseeker})

# Create your views here.
