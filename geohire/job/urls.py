from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.job_list, name="job_list"),
    path("create/", views.create_job, name="create_job"),
    path("edit/<int:job_id>/", views.edit_job, name="edit_job"),
    path("apply/<int:job_id>/", views.apply_for_job, name="apply_for_job"),
    path("<int:job_id>/", views.job_detail, name="job_detail"),
    path("map/", views.job_map, name="job_map"),
]