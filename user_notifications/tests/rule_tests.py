from django.test import TestCase, Client
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from user_messages.models import Message
from user_notifications.models import Notification
from user_notifications.rules import OddRuleExample, RossRuleExample
from user_notifications.tests.example_rules import DoesNotApplyRuleExample, NoRuleNameExample


User = get_user_model()
    

class RuleBaseTests(TestCase):

    def test_rule_name_not_implemented_error(self):
        with self.assertRaises(NotImplementedError) as error:
            invalid_rule = NoRuleNameExample()
        self.assertIn("passed notification variable is not a Notification type", error)

    def test_rule_notification_incorrect_type_implemented_error(self):
        with self.assertRaises(TypeError) as error:
            invalid_rule = DoesNotApplyRuleExample("str instead of notification", User.objects.get(pk=1))
        self.assertIn("user cannot be None type", error)

    def test_does_rule_apply_not_implemented_error(self):
        with self.assertRaises(NotImplementedError):
            invalid_rule = DoesNotApplyRuleExample(Notification.objects.all().first(), User.objects.get(pk=1))
            invalid_rule.does_rule_apply()
        
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


