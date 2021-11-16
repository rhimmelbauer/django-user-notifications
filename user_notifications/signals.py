from allauth.account.signals import user_logged_in
from django.dispatch import receiver

from .rule_processor import NotificationRuleProcessor
from .utils import get_site_from_request


notification_checker = NotificationRuleProcessor()

@receiver(user_logged_in)
def process_rules(sender, request, user, **kwargs):
    notification_checker.process_notifications(get_site_from_request(request), user)
    print("I just logged in")