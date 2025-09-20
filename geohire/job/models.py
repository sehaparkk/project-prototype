from django.db import models
from jobseeker.models import Skill
from recruiter.models import Recruiter

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

    def __str__(self):
        return self.title

class JobLocation(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name="location")
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.job.title} - {self.city}, {self.country}"
