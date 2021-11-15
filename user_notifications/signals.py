from allauth.account.signals import user_logged_in
from django.dispatch import receiver

from .notifications import NotificationRuleChecker
from .utils import get_site_from_request


notification_checker = NotificationRuleChecker()

@receiver(user_logged_in)
def process_rules(sender, request, user, **kwargs):
    notification_checker.process_notifications(get_site_from_request(request), user)
    print("I just logged in")