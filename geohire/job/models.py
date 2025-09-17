from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    posted_at = models.DateTimeField(auto_now_add=True)
    skills = models.TextField(help_text="Required skills")  
    salary_range = models.CharField(max_length=50)  
    remote_or_onsite = models.CharField(
        max_length=20,
        choices=[("Remote", "Remote"), ("Onsite", "Onsite")]
        default="Remote"
    )
    visa_sponsorship = models.BooleanField(default=False)
    def __str__(self):
        return self.title
