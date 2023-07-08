from django.apps import AppConfig
from django.db.models.signals import post_migrate


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self) -> None:
        
        post_migrate.connect(self.initializationConfig, sender=self)
        from . import signals
        return super().ready()
    

    def initializationConfig(self, **kwargs):
        from .models import CBRSettings, UBRSettings

        # Define application settings if not exist
        # Recommenders settings
        # Timeout: value less than 30 seconds means None
        # Update_on_new_stories: indicate if cbr will update every story create|delete|update

        if not CBRSettings.objects.exists():
            CBRSettings.objects.create()

        if not UBRSettings.objects.exists():
            UBRSettings.objects.create()