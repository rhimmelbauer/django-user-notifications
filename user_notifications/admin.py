from django.contrib import admin
from user_notifications.models import Notification

# Register your models here.
###############
# MODEL ADMINS
###############
class NotificationAdmin(admin.ModelAdmin):
    fields = ('active', 'deliver_once', 'name', 'sites', 'display_type', 'message', 'rules')


admin.site.register(Notification, NotificationAdmin)