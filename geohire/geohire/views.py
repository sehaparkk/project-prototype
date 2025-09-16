from django.shortcuts import redirect, render
from jobseeker.models import JobSeeker
from recruiter.models import Recruiter

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

#login view
def login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        from django.contrib.auth import authenticate, login as auth_login
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            #checks to see if its a recruiter or jobseeker and redirects accordingly
            try:
                recruiterTest = Recruiter.objects.get(user=user)
                return redirect('recruiter_homepage')
            except Recruiter.DoesNotExist:
                return redirect('jobseeker_homepage')
    return render(request, 'login.html', {'error': error})
