from django.shortcuts import render

from django.views.generic import ListView
from user_notifications.models import Reminder
from user_notifications.utils import get_site_from_request

class ReminderIndexView(ListView):
    template_name = "core/index.html"
    model = Reminder

    def get_queryset(self):
        if hasattr(self.request, 'site'):
            return self.model.objects.filter(site=get_site_from_request(self.request))
        return self.model.on_site.all()
