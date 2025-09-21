from django.db import models
from jobseeker.models import Skill, JobSeeker
from recruiter.models import Recruiter
from django.urls import reverse

class Job(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name="jobs", null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    hide_salary = models.BooleanField(default=False)
    remote_or_onsite = models.CharField(
        max_length=20,
        choices=[("Remote", "Remote"), ("Onsite", "Onsite")],
        default="Remote"
    )
    visa_sponsorship = models.BooleanField(default=False)
    skills = models.ManyToManyField(Skill, related_name="jobs", blank=True)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('job_detail', args=[str(self.id)])


class JobLocation(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name="location")
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.job.title} - {self.city}, {self.country}"

class Application(models.Model):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Review', 'Review'),
        ('Interview', 'Interview'),
        ('Offer', 'Offer'),
        ('Closed', 'Closed'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    jobseeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')
    note = models.TextField(blank=True, null=True)
    recruiter_note = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('job', 'jobseeker')

    def __str__(self):
        return f'{self.jobseeker.user.username} applied for {self.job.title}'