from django.apps import AppConfig
from allauth.account.signals import user_logged_in


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self) -> None:
        from core.signals import user_login_notifications
        user_logged_in.connect(user_login_notifications)
