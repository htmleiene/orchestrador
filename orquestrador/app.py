from django.apps import AppConfig

class OrquestradorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orquestrador'

    def ready(self):
        from .schedule import scheduler
        scheduler.start()
