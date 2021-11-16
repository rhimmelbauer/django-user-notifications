from allauth.account.signals import user_logged_in
from django.dispatch import receiver

from .utils import get_site_from_request


@receiver(user_logged_in)
def process_rules(sender, request, user, **kwargs):
    # Insert any logic here to add desired notifications for users upon login.