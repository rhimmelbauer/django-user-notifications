from allauth.account.signals import user_logged_in
from django.apps import AppConfig


class UserNotificationsConfig(AppConfig):
    name = 'user_notifications'

    def ready(self):
        from .signals import process_rules
        user_logged_in.connect(process_rules)