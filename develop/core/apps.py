from django.apps import AppConfig
from core.signals import user_login_notifications


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self) -> None:
        from allauth.account.signals import user_logged_in
        user_logged_in.connect(user_login_notifications)
