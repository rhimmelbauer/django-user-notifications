from django.test import TestCase, Client
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from user_messages.models import Message
from user_notifications.models import Notification
from user_notifications.rule_processor import NotificationRuleProcessor


User = get_user_model()

# Create your tests here.
class RuleProcessorTests(TestCase):

    fixtures = ['user', 'unit_test']

    def setUp(self):
        self.site_one = Site.objects.get(pk=1)
        self.site_two = Site.objects.get(pk=2)
        self.user = User.objects.get(pk=1)

    def test_queue_one_time_notification(self):
        notification = Notification.objects.get(pk=1)
        notification.active = True
        notification.save()
        self.assertFalse(Message.objects.filter(user=self.user).count())
        NotificationRuleProcessor().process_notifications(self.site_one, self.user)
        self.assertTrue(Message.objects.filter(user=self.user).count())

    def test_queue_user_confirm_notification(self):
        notification = Notification.objects.get(pk=2)
        notification.active = True
        notification.save()
        self.assertFalse(Message.objects.filter(user=self.user).count())
        NotificationRuleProcessor().process_notifications(self.site_one, self.user)
        self.assertTrue(Message.objects.filter(user=self.user).count())

    def test_queue_expire_after_date(self):
        notification = Notification.objects.get(pk=3)
        notification.active = True
        notification.save()
        self.assertFalse(Message.objects.filter(user=self.user).count())
        NotificationRuleProcessor().process_notifications(self.site_one, self.user)
        self.assertTrue(Message.objects.filter(user=self.user).count())

    def test_queue_start_after_date(self):
        notification = Notification.objects.get(pk=4)
        notification.active = True
        notification.save()
        self.assertFalse(Message.objects.filter(user=self.user).count())
        NotificationRuleProcessor().process_notifications(self.site_one, self.user)
        self.assertTrue(Message.objects.filter(user=self.user).count())

    def test_queue_between_start_and_end_date(self):
        notification = Notification.objects.get(pk=5)
        notification.active = True
        notification.save()
        self.assertFalse(Message.objects.filter(user=self.user).count())
        NotificationRuleProcessor().process_notifications(self.site_one, self.user)
        self.assertTrue(Message.objects.filter(user=self.user).count())

    def test_queue_user_confirm_between_start_and_end_date(self):
        notification = Notification.objects.get(pk=6)
        notification.active = True
        notification.save()
        self.assertFalse(Message.objects.filter(user=self.user).count())
        NotificationRuleProcessor().process_notifications(self.site_one, self.user)
        self.assertTrue(Message.objects.filter(user=self.user).count())


