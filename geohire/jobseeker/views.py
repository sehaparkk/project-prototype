from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import jobseekerCreationForm
from .models import JobSeeker
from django.utils.text import slugify

# basic show profile view, just takes a slug, finds the jobseeker, and then passes both along
def show_profile(request, slug):
    jobseeker = get_object_or_404(JobSeeker, slug=slug)
    return render(request, 'jobseeker/profile.html', {'slug' : jobseeker.slug, 'jobseeker': jobseeker})

#the register view, passes two HTML POST things (one to handle the form, one for the files)
#and then creates a user and jobseeker object if the form is valid
def register(request):
    if request.method == 'POST':
        form = jobseekerCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            phone = form.cleaned_data.get('phone')
            resume = form.cleaned_data.get('resume')
            headline = form.cleaned_data.get('headline')
            urls = form.cleaned_data.get('urls')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            zip_code = form.cleaned_data.get('zip_code')
            street_address = form.cleaned_data.get('street_address')
            country = form.cleaned_data.get('country')

            counter = 0
            slug = slugify(form.cleaned_data.get('first_name'))
            while JobSeeker.objects.filter(slug=slug).exists():
                slug = f"{slug}-{counter}" 
                counter += 1
            #ensures there will always be a numeric character after the slug
            slug = f"{slug}-{counter}"
            JobSeeker.objects.create(
                user = user,
                phone = phone,
                resume = resume,
                headline = headline,
                created_at = user.date_joined,
                updated_at = user.date_joined,
                slug = slug,
                urls = urls,
                city = city,
                state = state,
                zip_code = zip_code,
                street_address = street_address,
                country = country,
            )
            return redirect('login')
    else:
        form = jobseekerCreationForm()
    return render(request, 'jobseeker/register.html', {'form': form})

#basic login view, just renders the login HTML
def login(request):
    return render(request, 'jobseeker/login.html')
