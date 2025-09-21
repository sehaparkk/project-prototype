from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('jobseeker/', include('jobseeker.urls')),  # This links the jobseeker app
    path('job/', include('job.urls')), # links job app
    path('recruiter/', include('recruiter.urls')), # links recruiter app
    path('messages/', include('messaging.urls')), # links messaging app
    path('login/', views.login, name='login'),  # Custom login view
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='logout'),
]

#this allows to app the server media files during development (it basically makes them static)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)