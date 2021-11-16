from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import ListView, View

from user_notifications.models import Notification
from user_notifications.utils import get_site_from_request

class NotificationIndexView(ListView):
    template_name = "core/index.html"
    model = Notification

    def get_queryset(self):
        if hasattr(self.request, 'site'):
            return self.model.objects.filter(site=get_site_from_request(self.request))
        return self.model.on_site.all()

class AcceptNotification(View):

    def post(self, request, *args, **kwargs):
        if 'pk' not in request.POST:
            return Http404
        notification = Notification.objects.get(pk=request.POST['pk'])
        notification.save_user_acknowledgement(request.user, True)
        return redirect(request.META.get('HTTP_REFERER'))

class DeclineNotification(View):

    def post(self, request, *args, **kwargs):
        if 'pk' not in request.POST:
            return Http404
        notification = Notification.objects.get(pk=request.POST['pk'])
        notification.save_user_acknowledgement(request.user, False)
        return redirect(request.META.get('HTTP_REFERER', self.success_url))