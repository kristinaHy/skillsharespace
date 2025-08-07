

from django.apps import AppConfig

class SkillsharespaceAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'skillsharespace_app'

    def ready(self):
        import skillsharespace_app.signals 
