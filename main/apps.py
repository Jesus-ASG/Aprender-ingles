import json

from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self) -> None:
        from .models import CBRSettings, UBRSettings

        # Define application settings if not exist
        # Recommenders settings
        # Timeout: value less than 30 seconds means None
        # Update_on_new_stories: indicate if cbr will update every story create|delete|update
        
        if not CBRSettings.objects.exists():
            CBRSettings.objects.create()

        if not UBRSettings.objects.exists():
            UBRSettings.objects.create()
        

        from . import signals
        return super().ready()
    