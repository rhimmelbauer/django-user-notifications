from django.conf import settings
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _
from user_messages import api as user_messages

def set_default_site_id():
    return Site.objects.get_current()

def set_default_message():
    default = {
        "title": "",
        "description": "",
        "accept_button": "Accept",
        "accept_url": "user_notifications:notification-confirm",
        "decline_button": "Decline",
        "decline_url": "user_notifications:notification-decline"
    }
    return default

class DisplayType(models.IntegerChoices):
    BOOTSTRAP_ALERT = 100, _("Bootstrap Alert")
    MODAL = 200, _("Modal")


# Create your models here.
class Notification(models.Model):
    name = models.CharField(verbose_name=_("Notification Name"), blank=False, null=False, max_length=65)
    active = models.BooleanField(verbose_name=_("Active"), default=False)
    sites = models.ManyToManyField(Site, verbose_name=_("Sites"), blank=True, related_name="notifications")
    display_type = models.IntegerField(verbose_name=_("Message Type"), choices=DisplayType.choices, default=DisplayType.BOOTSTRAP_ALERT)
    message = models.JSONField(verbose_name=_("Message Content"), blank=True, null=True, default=set_default_message)
    start_date = models.DateTimeField(_("Start Date"), blank=True, null=True, help_text=_("Notification Start Date?"))
    end_date = models.DateTimeField(_("End Date"), blank=True, null=True, help_text=_("Notification End Date?"))
    rules = models.JSONField(default=list, blank=True, null=True)
    meta = models.JSONField(default=dict, blank=True, null=True)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    def add_user_message(self, user, deliver_once=True):
        self.message['display_type'] = self.display_type
        self.message['pk'] = self.pk
        user_messages.info(user, self.name, deliver_once=deliver_once, meta=self.message)