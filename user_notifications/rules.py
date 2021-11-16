from django.utils import timezone
from django.db.models import Q
from user_messages import api as user_messages
from user_notifications.models import Notification


class RuleBase:
    RULE_NAME = None
    notification = None
    user = None
    apply_rule = False

    def __init__(self, notification, user):
        if not self.RULE_NAME:
            raise NotImplementedError
        if not type(notification) == Notification:
            raise TypeError
        self.notification = notification
        self.user = user
    
    def __str__(self):
        return self.RULE_NAME

    def does_rule_apply(self):
        raise NotImplemented

    def notification_exists(self):
        if user_messages.get_messages(user=self.user):
            return True
        return False

    def queue_notification(self):
        if not self.notification_exists():
            self.notification.add_user_message(self.user)

    def expire_notification(self):
        raise NotImplemented

    def gt(self, value):
        raise NotImplemented

    def gte(self, value):
        raise NotImplemented

    def lt(self, value):
        raise NotImplemented

    def lte(self, value):
        raise NotImplemented


class ExampleEvenRule(RuleBase):
    RULE_NAME = "ExampleEvenRule"
    
    def does_rule_apply(self):
        if self.user.pk % 2:
            return  True
        return False


class RuleConstructor:

    def create_rule(notification, rule_name, user):
        if rule_name == ExampleEvenRule.RULE_NAME:
            return ExampleEvenRule(notification, user)
        else:
            raise NotImplemented



def check_for_new_notifications(site, user):
    notifications_to_process = [
        notification for notification in Notification.objects.filter(
            Q(sites__in=[site]), Q(active=True), 
            Q(start_date__lte=timezone.now()) | Q(start_date=None),
            Q(end_date__gte=timezone.now()) | Q(end_date=None))
        if not notification.already_exists(user)
        ]

    for notification in notifications_to_process:
        notification.process_rules(user)
    
