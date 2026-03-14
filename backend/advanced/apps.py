from django.apps import AppConfig
import sys


class AdvancedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'advanced'

    def ready(self):
        # Only start scheduler in the main server process, not during migrations/tests
        if 'runserver' in sys.argv or 'gunicorn' in sys.argv[0:1]:
            from . import scheduler
            scheduler.start()
