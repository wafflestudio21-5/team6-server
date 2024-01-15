from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/sample/", include("sample.urls")),
    path("api/auth/", include("waffleAuth.urls")),
    path("api/users/", include("userprofile.urls")),
]
