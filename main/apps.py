import json

from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self) -> None:
        from .models import AppSettings

        # Define application settings if not exist
        # Content based recommender settings
        # Timeout: integer of seconds, values less than 30s means None
        # Update_on_new_stories: boolean, indicate if cbr will update every story create|delete|update
        if not AppSettings.objects.filter(key='cbr').first():
            values = {
                'timeout': 0,
                'update_on_alter_stories': True
            }
            values = json.dumps(values)
            AppSettings.objects.create(
                key='cbr',
                value=values
            )

        if not AppSettings.objects.filter(key='ubr').first():
            values = {
                'timeout': 1800
            }
            values = json.dumps(values)
            AppSettings.objects.create(
                key='ubr',
                value=values
            )

        from . import signals
        return super().ready()
    