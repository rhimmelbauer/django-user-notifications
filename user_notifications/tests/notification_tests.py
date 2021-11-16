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