from allauth.account.signals import user_logged_in
from django.dispatch import receiver

from user_notifications.utils import get_site_from_request
from user_notifications.rules import check_for_new_notifications

@receiver(user_logged_in)
def user_login_notifications(sender, request, user, **kwargs):
    check_for_new_notifications(get_site_from_request(request), user)