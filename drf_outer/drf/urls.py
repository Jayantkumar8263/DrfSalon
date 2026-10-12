from django.contrib import admin
from django.urls import include, path

from rest_framework.authtoken.views import obtain_auth_token

from salon.urls import (
    api_urlpatterns,
    page_urlpatterns,
)


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "",
        include(page_urlpatterns),
    ),
    path(
        "api/",
        include(api_urlpatterns),
    ),
    path(
        "api/login/",
        obtain_auth_token,
        name="api-login",
    ),
]