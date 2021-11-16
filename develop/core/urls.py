from django.urls import path

from core import views

urlpatterns = [
    path("", views.NotificationIndexView.as_view(), name="notification-index"),
    path('notification/confirm', views.AcceptNotification.as_view(), name='notification-confirm'),
    path('notification/decline', views.DeclineNotification.as_view(), name='notification-decline')
]
