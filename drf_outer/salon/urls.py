from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import AvailabilityAPIView, AppointmentViewSet, RegisterAPIView, ServiceViewSet, StaffViewSet, admin_dashboard, booking_page, dashboard_page, home, login, register_page, services_page, customer_profile

router = DefaultRouter()

router.register("services", ServiceViewSet, basename="api-service")

router.register("staff", StaffViewSet, basename="api-staff")
router.register(
    "appointments",
    AppointmentViewSet,
    basename="api-appointment",
)


# Website pages: these URLs do not start with /api/
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
        "register/",
        register_page,
        name="register-page",
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
    path("profile/", customer_profile, name="customer-profile"),
]


# API endpoints: these URLs will get the /api/ prefix
api_urlpatterns = [
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


# Documentation endpoints are optional.
# Leave them commented if you are not using Swagger right now.
urlpatterns = [
    *page_urlpatterns,
    path(
        "api/",
        include(api_urlpatterns),
    ),
]