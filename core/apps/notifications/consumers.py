import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.template import Context, Template


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("notifications", self.channel_name)
        # return await super().connect()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications", self.channel_name)

    async def send_notification(self, event):
        message = event["message"]
        created_at = event["created_at"]

        template = Template(f"""
<li class="list-group-item d-flex justify-content-between align-items-start">
    <div class="ms-2 me-auto">
        <div class="fw-bold">{created_at}</div>
        {message}
    </div>
</li>
""")
        context = Context({"message": message})
        rendered_notification = template.render(context)
        await self.send(
            text_data=json.dumps(
                {
                    "type": "notification",
                    "message": rendered_notification,
                }
            )
        )
