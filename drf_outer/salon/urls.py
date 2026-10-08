from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from rest_framework.routers import DefaultRouter

from .views import (
    AvailabilityAPIView,
    AppointmentViewSet,
    RegisterAPIView,
    ServiceViewSet,
    StaffViewSet,
    admin_dashboard,
    booking_page,
    dashboard_page,
    home,
    login,
    register_page,
    services_page,
)


router = DefaultRouter()

router.register(
    "services",
    ServiceViewSet,
    basename="api-service",
)

router.register(
    "staff",
    StaffViewSet,
    basename="api-staff",
)

router.register(
    "appointments",
    AppointmentViewSet,
    basename="api-appointment",
)


page_urlpatterns = [
    path(
        "",
        home,
        name="home",
    ),

    path(
        "services/",
        services_page,
        name="services",
    ),

    path(
        "booking/",
        booking_page,
        name="booking",
    ),

    path(
        "login/",
        login,
        name="login",
    ),

    path(
        "dashboard/",
        dashboard_page,
        name="dashboard",
    ),

    path(
        "admin-dashboard/",
        admin_dashboard,
        name="admin-dashboard",
    ),
]


api_urlpatterns = [
    path(
        "register/",
        register_page,
        name="register-page",
    ),

    path(
        "register/",
        RegisterAPIView.as_view(),
        name="api-register",
    ),

    path(
        "availability/",
        AvailabilityAPIView.as_view(),
        name="api-availability",
    ),
]

api_urlpatterns += router.urls


urlpatterns = [
    *page_urlpatterns, # ye line page_urlpatterns ko urlpatterns me add kar rahi hai

    path(
        "api/",
        include(api_urlpatterns),
    ),

    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema",
        ),
        name="swagger-ui",
    ),

    path(
        "api/redoc/",
        SpectacularRedocView.as_view(
            url_name="schema",
        ),
        name="redoc",
    ),
]