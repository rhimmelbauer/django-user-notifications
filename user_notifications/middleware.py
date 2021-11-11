from django.contrib import messages
from django.utils.translation import activate
from user_messages import api as user_messages
from user_notifications.models import Reminder
from user_notifications.utils import get_site_from_request

class UserNotificationsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        for reminder in Reminder.objects.filter(site__in=[get_site_from_request(request)], active=True):
            
        if request.user.is_authenticated:
            user_messages.info(request.user, "hello there")
            print("Rob is very slow")

        return response