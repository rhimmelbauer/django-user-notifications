from django.contrib.sites.models import Site
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import resolve
from django.utils import timezone
from user_notifications.models import DisplayType, Notification

class NotificationRedirctMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if getattr(request, "site", None):
            site = request.site
        else:
            site = Site.objects.get_current()
        notification = Notification.objects.filter(
            Q(sites__in=[site]), Q(active=True), Q(display_type=DisplayType.REDIRECT),
            Q(start_date__lte=timezone.now()) | Q(start_date=None),
            Q(end_date__gte=timezone.now()) | Q(end_date=None)).first()

        if notification and notification.message and "redirect_to" in notification.message:
            redirect_to = notification.message["redirect_to"]

            # only redirect if we're not already there
            url_name = resolve(request.path_info).url_name
            if not redirect_to == request.path and not redirect_to == url_name:
                return redirect(redirect_to)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response