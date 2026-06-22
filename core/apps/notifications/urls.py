from django.urls import path

from . import views
from .consumers import NotificationConsumer

urlpatterns = [
    path("", views.show_notifications_example_page, name="notifications-page"),
]

websocket_urlpatterns = [
    path("ws/notifications/", NotificationConsumer.as_asgi()),
]
