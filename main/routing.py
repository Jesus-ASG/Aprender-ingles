from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/report-notifications/", consumers.ReportNotificationsConsumer.as_asgi()),
]
