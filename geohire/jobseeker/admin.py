from django.contrib import admin
from .models import JobSeeker, userLocation, userEducation, workExperience, userLink, Skill

admin.site.register(JobSeeker)
admin.site.register(userLocation)
admin.site.register(userEducation)
admin.site.register(workExperience)
admin.site.register(userLink)
admin.site.register(Skill)