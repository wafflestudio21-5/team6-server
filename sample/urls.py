from django.urls import path
from .views import ConnectionCheckAPIView

urlpatterns = [
    path("connection-check", ConnectionCheckAPIView.as_view(), name="connection-check"),
]
