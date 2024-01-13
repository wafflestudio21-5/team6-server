from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sample/", include("sample.urls")),
    path("auth/", include("waffleAuth.urls")),
    path("contents/", include("content.urls")),
    path("comments/", include("comment.urls")),
]
