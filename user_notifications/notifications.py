
from django.utils import timezone
from django.utils.translation import activate
from user_messages import api as user_messages
from user_notifications.models import Notification


class RuleBase:
    RULE_NAME = None
    notification = None
    user = None

    def __init__(self, notification, user):
        if not self.RULE_NAME:
            raise NotImplementedError
        if not type(notification) == Notification:
            raise TypeError
        self.notification = notification
        self.user = user
    
    def __str__(self):
        return self.RULE_NAME

    def queue_notification(self):
        raise NotImplemented

    def notification_exists(self):
        if user_messages.get_messages(user=self.user):
            return True
        return False

    def gt(self, value):
        raise NotImplemented

    def gte(self, value):
        raise NotImplemented

    def lt(self, value):
        raise NotImplemented

    def lte(self, value):
        raise NotImplemented


class StartDateRule(RuleBase):
    RULE_NAME = "StartDateRule"
    
    def queue_notification(self):
        return self.gt(timezone.now())

    def gt(self, date):
        if self.notification.start_date and date > self.notification.start_date:
            return True
        return False


class EndDateRule(RuleBase):
    RULE_NAME = "EndDateRule"

    def queue_notification(self):
        return self.lt(timezone.now())

    def lt(self, date):
        if self.notification.end_date and date < self.notification.end_date:
            return True
        return False


class UserConfirmationRule(RuleBase):
    RULE_NAME = "UserConfirmationRule"

    def queue_notification(self):
        if not self.notification_exists():
            self.notification.add_user_message(self.user)


class RuleConstructor:

    def create_rule(notification, rule_name, user):
        if rule_name == UserConfirmationRule.RULE_NAME:
            return UserConfirmationRule(notification, user)
        elif rule_name == StartDateRule.RULE_NAME:
            return StartDateRule(notification, user)
        elif rule_name == EndDateRule.RULE_NAME:
            return EndDateRule(notification, user)


class NotificationRuleChecker:
    """
    Class to process created rules for notifications set for a site or sites
    """
    def process_rules(self, notification, user):
        for rule_name in notification.rules:
            rule = RuleConstructor.create_rule(notification, rule_name, user)
            if rule.queue_notification():
                user_messages.info()

    def process_notifications(self, site, user):
        for notification in Notification.objects.filter(sites__in=[site], active=True):
            self.process_rules(notification, user)

    def queue_notification(self):
        # get messages
        # get active notifications
        # queue new messages
        pass

    def expire_notification(self, notification):
        pass


def available_rules():
    return [UserConfirmationRule, StartDateRule, EndDateRule]


