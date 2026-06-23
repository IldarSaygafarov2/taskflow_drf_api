from asgiref.sync import async_to_sync
import json

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.apps.notifications.consumers import NotificationConsumer
from core.apps.notifications.models import Notification
from core.apps.users.models import CustomUser


class NotificationsAppTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="notifyuser",
            email="notify@example.com",
            password="password123",
            first_name="Notify",
            last_name="User",
        )
        self.url = reverse("notifications-page")

    def test_notifications_page_without_authentication(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertEqual(list(response.context["notifications"]), [])

    def test_notifications_page_with_unread_notifications(self):
        Notification.objects.create(
            user=self.user,
            title="Test notification",
            message="Hello world",
        )

        self.client.login(username="notifyuser", password="password123")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("notifications", response.context)
        self.assertEqual(len(response.context["notifications"]), 1)
        self.assertEqual(
            response.context["notifications"][0].title, "Test notification"
        )

    def test_notifications_form_login_redirects(self):
        response = self.client.post(
            self.url,
            {"username": "notifyuser", "password": "password123"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["request"].user.is_authenticated)

    def test_notification_consumer_send_notification(self):
        consumer = NotificationConsumer()
        consumer.scope = {"type": "websocket"}

        sent_messages = []

        async def fake_send(text_data=None, bytes_data=None):
            sent_messages.append(text_data)

        consumer.send = fake_send

        event = {
            "type": "send_notification",
            "message": "New update",
            "title": "Hello",
            "created_at": timezone.now().isoformat(),
        }

        async_to_sync(consumer.send_notification)(event)

        self.assertEqual(len(sent_messages), 1)
        message = json.loads(sent_messages[0])
        self.assertEqual(message["type"], "notification")
        self.assertIn("Hello", message["message"])
        self.assertIn("New update", message["message"])
