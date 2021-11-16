from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.test import TestCase, Client
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
        self.assertTrue(notification.is_between_dates)

    def test_dont_queue_expire_after_date(self):
        notification = Notification.objects.get(pk=3)
        notification.end_date = (timezone.now() - timedelta(days=1))
        self.assertFalse(notification.is_between_dates())

    def test_queue_start_after_date(self):
        notification = Notification.objects.get(pk=4)
        self.assertTrue(notification.is_between_dates())

    def test_dont_queue_start_after_date(self):
        notification = Notification.objects.get(pk=4)
        notification.start_date = (timezone.now() + timedelta(days=1))
        self.assertFalse(notification.is_between_dates())

    def test_queue_between_start_and_end_date(self):
        notification = Notification.objects.get(pk=5)
        self.assertTrue(notification.is_between_dates())
