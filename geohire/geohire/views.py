from django.shortcuts import render
from jobseeker.models import JobSeeker

#defines homepage view, passes a jobseeker object if the user is logged in
#this will need to be updated once we add an employer model
def homepage(request):
    jobseeker = None
    template_data = {}
    template_data['title'] = "Home"

    try:
        if request.user.is_authenticated:
            template_data['jobseeker']=JobSeeker.objects.get(user=request.user)
    except:
        jobseeker = None
    return render(request, 'home.html', {'template_data': template_data})

# Create your views here.
