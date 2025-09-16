from django.shortcuts import render

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = "Recruiter Page"
    return render(request, 'recruiter/index.html', {"template_data": template_data})