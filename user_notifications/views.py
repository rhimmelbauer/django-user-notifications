from django.http.response import Http404
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View
from django.utils import timezone

from user_messages.models import Message
from .models import Notification

# Create your views here.
class AcceptNotification(View):

    def post(self, request, *args, **kwargs):
        if 'pk' not in request.POST:
            return Http404
        notification = Notification.objects.get(pk=request.POST['pk'])
        user_message = Message.objects.get(user=request.user, message=notification.name)
        user_message.delivered_at = timezone.now()
        user_message.deliver_once = True
        user_message.save()
        return redirect(request.META.get('HTTP_REFERER'))

class DeclineNotification(View):

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return redirect(request.META.get('HTTP_REFERER', self.success_url))