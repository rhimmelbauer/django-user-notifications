from typing import Callable
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _


def set_default_site_id():
    return Site.objects.get_current()

def set_default_message():
    default = {
        "title": "",
        "description": "",
        "accept_button": "Accept",
        "accept_url": "",
        "decline_button": "Decline",
        "decline_url": ""
    }
    return default

class MessageType(models.IntegerChoices):
    BOOTSTRAP_ALERT = 100, _("Bootstrap Alert")
    MODAL = 200, _("Modal")


# Create your models here.
class Reminder(models.Model):
    name = models.CharField(verbose_name=_("Reminder Name"), blank=False, null=False, max_length=65)
    sites = models.ManyToManyField(Site, verbose_name=_("Sites"), blank=True, related_name="reminders")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("Users"), blank=True, related_name="reminders")
    message_type = models.IntegerField(verbose_name=_("Message Type"), choices=MessageType.choices, default=MessageType.BOOTSTRAP_ALERT)
    message = models.JSONField(verbose_name=_("Message Content"), blank=True, null=True, default=set_default_message)
    active = models.BooleanField(verbose_name=_("Active"), default=False)

    objects = models.Manager()
    on_site = CurrentSiteManager()


class Rule(models.Model):
    name = models.CharField(verbose_name=_("Rule Name"), blank=False, null=False, max_length=65)
    reminders = models.ForeignKey(Reminder, related_name="rule", blank=True, on_delete=CASCADE)
    confirmation = models.BooleanField(verbose_name=_("User Confirmation"), default=True, help_text=_("Stops after user confirms?"))
    always = models.BooleanField(verbose_name=_("Always"), default=False, help_text=_("Display on every view?"))
    retries = models.IntegerField(verbose_name=_("Retries"), default=0)
    start_date = models.DateTimeField(_("Start Date"), blank=True, null=True, help_text=_("Reminder Starts at?"))
    end_date = models.DateTimeField(_("End Date"), blank=True, null=True, help_text=_("Reminder Stops at?"))

    objects = models.Manager()