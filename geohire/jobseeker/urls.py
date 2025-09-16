from django.contrib import admin
from django.urls import path, include
#seperate import to avoid confusion between views.py and django special things
from django.contrib.auth import views as auth_views
from . import views

#yay!!! Urls!
#Note: The logout just redirects back to the homepage instead of to a seperate page (thats what the next_page thing does)
urlpatterns = [
    path('profile/<str:slug>/', views.show_profile, name='jobseeker_profile'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='jobseeker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='logout'),
    path('newLocation/', views.newLocation, name='new_location'),
    path('newWorkExperience/', views.newWorkExperience, name='new_work_experience'),
    path('newEducation/', views.newEducation, name='new_education'),
]