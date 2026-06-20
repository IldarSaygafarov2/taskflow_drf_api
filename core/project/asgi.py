import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.project.settings")

django_application = get_asgi_application()

from core.apps.notifications import urls

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(urls.websocket_urlpatterns),
    }
)
