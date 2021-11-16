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

    def gt(self, value):
        raise NotImplemented

    def gte(self, value):
        raise NotImplemented

    def lt(self, value):
        raise NotImplemented

    def lte(self, value):
        raise NotImplemented


class OddRuleExample(RuleBase):
    RULE_NAME = "OddRuleExample"
    
    def does_rule_apply(self):
        if self.user.pk % 2:
            return  True
        return False

class RossRuleExample(RuleBase):
    RULE_NAME = "RossRuleExample"
    
    def does_rule_apply(self):
        if self.user.last_name == "Ross":
            return  True
        return False


class RuleConstructor:

    def create_rule(notification, rule_name, user):
        if rule_name == OddRuleExample.RULE_NAME:
            return OddRuleExample(notification, user)
        else:
            raise NotImplemented

def apply_notification_rules(notification, user):
    apply_rules = []

    for rule_name in notification.rules:
        rule = RuleConstructor.create_rule(notification, rule_name, user)
        apply_rules.append(rule.does_rule_apply())

    if False not in apply_rules:
        notification.add_user_message(user)


def check_for_new_notifications(site, user):
    notifications_to_process = [
        notification for notification in Notification.objects.filter(
            Q(sites__in=[site]), Q(active=True), 
            Q(start_date__lte=timezone.now()) | Q(start_date=None),
            Q(end_date__gte=timezone.now()) | Q(end_date=None))
        if not notification.already_exists(user)
        ]

    for notification in notifications_to_process:
        apply_notification_rules(notification, user)
    
