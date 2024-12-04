from core.rules import apply_notification_rules
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase, Client
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


class NotificationTemplateTests(TestCase):

    fixtures = ['user', 'unit_test']

    def setUp(self):
        self.user_one = User.objects.get(pk=1)
        self.client = Client()
        self.index_url = reverse('notification-index')

    def test_anonymous_user_no_messages(self):
        response = self.client.get(self.index_url)
        self.assertNotContains( response, '<div class="alert alert-dismissible')
        self.assertNotContains(response, '<div id="notification-modal" class="modal" tabindex="-1">')

    def test_show_alert_message_after_login(self):
        notification = Notification.objects.get(pk=1)
        notification.active = True
        notification.save()

        response = self.client.post(reverse('account_login'), {"login": "rob", "password": "django321"})
        response = self.client.get(self.index_url)

        self.assertContains(response, '<div class="alert alert-dismissible')
        self.assertNotContains(response, '<div id="notification-modal" class="modal" tabindex="-1">')

    def test_show_alert_only_once(self):
        notification = Notification.objects.get(pk=1)
        notification.active = True
        notification.save()

        response = self.client.post(reverse('account_login'), {"login": "rob", "password": "django321"})
        response = self.client.get(self.index_url)

        self.assertContains(response, '<div class="alert alert-dismissible')
        self.assertNotContains(response, '<div id="notification-modal" class="modal" tabindex="-1">')
        
        response = self.client.get(self.index_url)
        self.assertNotContains(response, '<div class="alert alert-dismissible')
        self.assertNotContains(response, '<div id="notification-modal" class="modal" tabindex="-1">')

    def test_show_alert_always(self):
        notification = Notification.objects.get(pk=1)
        notification.deliver_once = False
        notification.active = True
        notification.save()

        response = self.client.post(reverse('account_login'), {"login": "rob", "password": "django321"})
        response = self.client.get(self.index_url)

        self.assertContains(response, '<div class="alert alert-dismissible')
        self.assertNotContains(response, '<div id="notification-modal" class="modal" tabindex="-1">')
        
        response = self.client.get(self.index_url)
        self.assertContains(response, '<div class="alert alert-dismissible')
        self.assertNotContains(response, '<div id="notification-modal" class="modal" tabindex="-1">')


class AcceptDeclineEndpointTests(TestCase):

    fixtures = ['user', 'unit_test']

    def setUp(self):
        self.user_one = User.objects.get(pk=1)
        self.client = Client()
        self.index_url = reverse('notification-index')
        self.accept_url = reverse('notification-confirm')
        self.decline_url = reverse('notification-decline')

    def test_accept_notification_success(self):
        notification = Notification.objects.get(pk=2)
        notification.active = True
        notification.save()

        response = self.client.post(reverse('account_login'), {"login": "rob", "password": "django321"})
        response = self.client.get(self.index_url)

        self.assertContains(response, '<div class="alert alert-dismissible')
        self.assertContains(response, '<div id="notification-modal" class="modal" tabindex="-1">')

        response = self.client.post(self.accept_url, data={"pk": 2})

        response = self.client.get(self.index_url)
        self.assertNotContains(response, '<div class="alert alert-dismissible')
        self.assertNotContains(response, '<div id="notification-modal" class="modal" tabindex="-1">')

        notification.refresh_from_db()
        self.assertIn('accepted', notification.meta.keys())
        self.assertIn(self.user_one.username, notification.meta['accepted'][Site.objects.get(pk=1).domain].keys())


class RedirectTests(TestCase):

    fixtures = ['user', 'unit_test']

    def setUp(self):
        self.user_one = User.objects.get(pk=1)
        self.client = Client()
        self.index_url = reverse('notification-index')

    def test_redirect_path_name_success(self):
        notification = Notification.objects.get(pk=7)
        notification.active = True
        notification.save()

        response = self.client.post(reverse('account_login'), {"login": "rob", "password": "django321"})
        redirect_to = notification.message["redirect_to"]
        redirect_url = reverse(redirect_to)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, redirect_url)

    def test_redirect_url_success(self):
        notification = Notification.objects.get(pk=8)
        notification.active = True
        notification.save()

        response = self.client.post(reverse('account_login'), {"login": "rob", "password": "django321"})
        redirect_url = notification.message["redirect_to"]

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, redirect_url)

