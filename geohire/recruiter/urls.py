from django.contrib import admin
from django.urls import path, include
#seperate import to avoid confusion between views.py and django special things
from django.contrib.auth import views as auth_views
from . import views

#yay!!! Urls!
#Note: The logout just redirects back to the homepage instead of to a seperate page (thats what the next_page thing does)
urlpatterns = [
    path('profile/<str:slug>/', views.show_profile, name='recruiter_profile'),
    path('register/', views.register, name='recruiter_register'),
    path('login/', auth_views.LoginView.as_view(template_name='recruiter/login.html', next_page = 'recruiter_homepage'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='recruiter_homepage'), name='logout'),
    path('newLocation/', views.newLocation, name='new_location'),
    path('newWorkExperience/', views.newWorkExperience, name='new_work_experience'),
    path('newEducation/', views.newEducation, name='new_education'),
    path('delete_location/<int:pk>/', views.delete_location, name='delete_location'),
    path('delete_work_experience/<int:pk>/', views.delete_work_experience, name='delete_work_experience'),
    path('delete_education/<int:pk>/', views.delete_education, name='delete_education'),
    path('recruiterHomepage/', views.recruiter_homepage, name='recruiter_homepage'),
]