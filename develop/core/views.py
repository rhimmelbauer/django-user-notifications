from django.http import Http404
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
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
    success_url = reverse_lazy('notification-index')

    def post(self, request, *args, **kwargs):
        if 'pk' not in request.POST:
            return Http404
        notification = Notification.objects.get(pk=request.POST['pk'])
        notification.save_user_acknowledgement(request.user, get_site_from_request(self.request), True)
        return redirect(request.META.get('HTTP_REFERER', self.success_url))

class DeclineNotification(View):
    success_url = reverse_lazy('notification-index')

    def post(self, request, *args, **kwargs):
        if 'pk' not in request.POST:
            return Http404
        notification = Notification.objects.get(pk=request.POST['pk'])
        notification.save_user_acknowledgement(request.user, get_site_from_request(self.request), False)
        return redirect(request.META.get('HTTP_REFERER', self.success_url))