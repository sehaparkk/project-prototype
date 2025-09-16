from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='job_index'),
    path('list/', views.job_list, name='job_list'),
    path('create/', views.create_job, name='create_job'),
    path('edit/<int:job_id>/', views.edit_job, name='edit_job'),
]
