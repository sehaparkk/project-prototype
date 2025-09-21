from django.contrib import admin
from .models import Recruiter, userLocation, userEducation, workExperience, SavedSearch

admin.site.register(Recruiter)
admin.site.register(userLocation)
admin.site.register(userEducation)
admin.site.register(workExperience)
admin.site.register(SavedSearch)