from django.shortcuts import render

# Create your views here.
def index(request):
    template_data = {}
    return render(request, "job/index.html", {"template_data": template_data})