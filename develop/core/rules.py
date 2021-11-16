from django.db.models import Q
from django.utils import timezone
from user_notifications.models import Notification
from user_notifications.rules import RuleBase, RuleConstructorBase


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

class CoreRuleConstructor(RuleConstructorBase):

    def create_rule(notification, rule_name, user):
        if rule_name == OddRuleExample.RULE_NAME:
            return OddRuleExample(notification, user)
        elif rule_name == RossRuleExample.RULE_NAME:
            return RossRuleExample(notification, user)
        else:
            raise NotImplementedError()


def apply_notification_rules(notification, user):
    apply_rules = []

    # If no rules are found, assume that the notification wants to be delivered.
    if not notification.rules:
        notification.add_user_message(user)
        return None

    for rule_name in notification.rules:
        rule = CoreRuleConstructor.create_rule(notification, rule_name, user)
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