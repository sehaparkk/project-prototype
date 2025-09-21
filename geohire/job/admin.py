from django.contrib import admin
from .models import Job, JobLocation, Application
import csv
from django.http import HttpResponse

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'posted_at', 'remote_or_onsite', 'visa_sponsorship', 'is_reviewed')
    list_filter = ('remote_or_onsite', 'visa_sponsorship', 'is_reviewed')
    search_fields = ('title', 'description')
    actions = ['mark_as_reviewed', 'export_as_csv']

    def mark_as_reviewed(self, request, queryset):
        queryset.update(is_reviewed=True)
    mark_as_reviewed.short_description = "Mark selected jobs as reviewed"

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response
    export_as_csv.short_description = "Export selected as CSV"

admin.site.register(JobLocation)
admin.site.register(Application)