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
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='recruiter_logout'),
    path('newLocation/', views.newLocation, name='recruiter_new_location'),
    path('newWorkExperience/', views.newWorkExperience, name='recruiter_new_work_experience'),
    path('newEducation/', views.newEducation, name='recruiter_new_education'),
    path('delete_location/<int:pk>/', views.delete_location, name='recruiter_delete_location'),
    path('delete_work_experience/<int:pk>/', views.delete_work_experience, name='recruiter_delete_work_experience'),
    path('delete_education/<int:pk>/', views.delete_education, name='recruiter_delete_education'),
    path('recruiterHomepage/', views.recruiter_homepage, name='recruiter_homepage'),
    path('recruiter/map.html', views.map, name='recruiter_map'),
    path('pipeline/', views.pipeline, name='recruiter_pipeline'),
    path('update_application_status/<int:pk>/', views.update_application_status, name='update_application_status'),
    path('save_search/', views.save_search, name='save_search'),
    path('saved_searches/', views.list_saved_searches, name='list_saved_searches'),
    path('job/<int:job_id>/candidate_recommendations/', views.candidate_recommendations, name='candidate_recommendations'),
]