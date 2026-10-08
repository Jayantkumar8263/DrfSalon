"""
URL configuration for drf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from rest_framework.authtoken.views import obtain_auth_token

from salon.urls import api_urlpatterns, page_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),

    path("",include(page_urlpatterns)),

    path(
        "api/",
        include(api_urlpatterns),
    ),

    path(
        "api/login/",
        obtain_auth_token,
        name="api-login",
    ),
    path("", include("salon.urls")),
    
]