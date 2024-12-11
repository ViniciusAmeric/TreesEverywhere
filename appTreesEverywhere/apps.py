from django.apps import AppConfig


class ApptreeseverywhereConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appTreesEverywhere'
    
    def ready(self):
        import appTreesEverywhere.signals
