from core.rules import apply_notification_rules
from django.test import TestCase, Client
from django.contrib.sites.models import Site

from django.contrib.auth import get_user_model
from user_messages.models import Message
from user_notifications.models import Notification


User = get_user_model()


class ApplyNotificationRulesTests(TestCase):

    fixtures = ['user', 'unit_test']

    def setUp(self):
        self.site_one = Site.objects.get(pk=1)
        self.site_two = Site.objects.get(pk=2)

    def test_queue_one_time_notification(self):
        user = User.objects.get(pk=1)
        notification = Notification.objects.get(pk=1)
        notification.active = True
        notification.save()
        self.assertFalse(Message.objects.filter(user=user).count())
        apply_notification_rules(notification, user)
        self.assertTrue(Message.objects.filter(user=user).count())

    def test_queue_odd_pk_user_rule_success(self):
        user = User.objects.get(pk=1)
        notification = Notification.objects.get(pk=2)
        notification.active = True
        notification.save()
        self.assertFalse(Message.objects.filter(user=user).count())
        apply_notification_rules(notification, user)
        self.assertTrue(Message.objects.filter(user=user).count())

    def test_queue_odd_pk_user_rule_false(self):
        user = User.objects.get(pk=2)
        notification = Notification.objects.get(pk=2)
        notification.active = True
        notification.save()
        self.assertFalse(Message.objects.filter(user=user).count())
        apply_notification_rules(notification, user)
        self.assertFalse(Message.objects.filter(user=user).count())

    def test_queue_notification_two_rules(self):
        user = User.objects.get(pk=1)
        notification = Notification.objects.get(pk=6)
        notification.active = True
        notification.save()
        self.assertFalse(Message.objects.filter(user=user).count())
        apply_notification_rules(notification, user)
        self.assertTrue(Message.objects.filter(user=user).count())

    def test_dont_queue_notification_two_rules(self):
        user = User.objects.get(pk=2)
        notification = Notification.objects.get(pk=6)
        notification.active = True
        notification.save()
        self.assertFalse(Message.objects.filter(user=user).count())
        apply_notification_rules(notification, user)
        self.assertFalse(Message.objects.filter(user=user).count())


