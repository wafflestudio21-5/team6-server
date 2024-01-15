from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/sample/", include("sample.urls")),
    path("auth/", include("waffleAuth.urls")),
]
