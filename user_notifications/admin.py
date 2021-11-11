from django.contrib import admin
from user_notifications.models import Reminder, Rule

# Register your models here.
###############
# MODEL ADMINS
###############
class ReminderAdmin(admin.ModelAdmin):
    fields = ('active', 'name', 'sites', 'users', 'message_type', 'message')


# class RuleAdmin(admin.ModelAdmin):
#     list_display = ('__all__')


admin.site.register(Reminder, ReminderAdmin)
admin.site.register(Rule)