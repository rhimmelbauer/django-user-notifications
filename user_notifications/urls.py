from user_notifications import views
from django.urls import path

app_name = "user_notifications"

urlpatterns = [
    path('notification/confirm', views.AcceptNotification.as_view(), name='notification-confirm'),
    path('notification/decline', views.DeclineNotification.as_view(), name='notification-decline')
]
