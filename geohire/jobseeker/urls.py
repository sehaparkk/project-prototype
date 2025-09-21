from django.contrib import admin
from django.urls import path, include
#seperate import to avoid confusion between views.py and django special things
from django.contrib.auth import views as auth_views
from . import views

#yay!!! Urls!
#Note: The logout just redirects back to the homepage instead of to a seperate page (thats what the next_page thing does)
urlpatterns = [
    path('profile/<str:slug>/', views.show_profile, name='jobseeker_profile'),
    path('register/', views.register, name='jobseeker_register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='jobseeker_logout'),
    path('newLocation/', views.newLocation, name='jobseeker_new_location'),
    path('newWorkExperience/', views.newWorkExperience, name='jobseeker_new_work_experience'),
    path('newEducation/', views.newEducation, name='jobseeker_new_education'),
    path('delete_location/<int:pk>/', views.delete_location, name='jobseeker_delete_location'),
    path('delete_work_experience/<int:pk>/', views.delete_work_experience, name='jobseeker_delete_work_experience'),
    path('delete_education/<int:pk>/', views.delete_education, name='jobseeker_delete_education'),
    path('jobSeekerHomepage/', views.jobseeker_homepage, name='jobseeker_homepage'),
    path('newURL/', views.newURL, name = 'jobseeker_url_adder_form'),
    path('deleteURL/<str:urlText>/', views.deleteURL, name='jobseeker_delete_url'),
    path('newSkills/', views.newSkill, name = 'jobseeker_skill_adder_form'),
    path('deleteSkill/<int:pk>/', views.deleteSkill, name='jobseeker_delete_skill'),
    path('skill-autocomplete/', views.skill_autocomplete, name='skill_autocomplete'),
    path('applications/', views.view_applications, name='view_applications'),
    path('editLocation/<int:pk>/', views.editLocation, name='jobseeker_edit_location'),
    path('editWorkExperience/<int:pk>/', views.editWorkExperience, name='jobseeker_edit_work_experience'),
    path('editEducation/<int:pk>/', views.editEducation, name='jobseeker_edit_education'),
    path('editProfile/', views.editJobSeekerProfile, name='jobseeker_edit_profile'),
    path('recommendations/', views.job_recommendations, name='job_recommendations'),
]