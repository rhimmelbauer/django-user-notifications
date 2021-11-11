from user_notifications import views
from django.urls import path

urlpatters = [
    path('reminder/confirm', views.ReminderConfirmation.as_view(), name='reminder-confirm'),
    path('reminder/decline', views.ReminderDecline.as_view(), name='reminder-decline')
]
