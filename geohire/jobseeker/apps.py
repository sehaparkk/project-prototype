from django.apps import AppConfig


class JobseekerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobseeker'

    #gets the custom delete method
    def ready(self):
        import jobseeker.signals
