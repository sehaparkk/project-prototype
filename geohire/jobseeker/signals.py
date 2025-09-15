from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import JobSeeker

#custom delete method to be called to delete a users resume when
#the user gets deleted
@receiver(post_delete, sender=JobSeeker)
def delete_resume_file(sender, instance, **kwargs):
    if instance.resume:
        instance.resume.delete(save=False)