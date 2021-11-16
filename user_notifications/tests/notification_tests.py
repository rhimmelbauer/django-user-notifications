from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from user_notifications.models import Notification

User = get_user_model()

# Create your tests here.
class NotificationModelTests(TestCase):

    fixtures = ['user', 'unit_test']

    def setUp(self):

        self.client = Client()
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_queue_expire_after_date(self):
        notification = Notification.objects.get(pk=3)
        notification.active = True
        notification.save()
        self.assertFalse(Message.objects.filter(user=self.user).count())
        apply_notification_rules(notification, self.user)
        self.assertTrue(Message.objects.filter(user=self.user).count())

    def test_queue_start_after_date(self):
        notification = Notification.objects.get(pk=4)
        notification.active = True
        notification.save()
        self.assertFalse(Message.objects.filter(user=self.user).count())
        apply_notification_rules(notification, self.user)
        self.assertTrue(Message.objects.filter(user=self.user).count())

    def test_queue_between_start_and_end_date(self):
        notification = Notification.objects.get(pk=5)
        notification.active = True
        notification.save()
        self.assertFalse(Message.objects.filter(user=self.user).count())
        apply_notification_rules(notification, self.user)
        self.assertTrue(Message.objects.filter(user=self.user).count())