from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import home, services_page,ServiceViewSet, StaffViewSet, AppointmentViewSet
router = DefaultRouter()

router.register("services", ServiceViewSet, basename="service")

router.register("staff", StaffViewSet, basename="staff")

router.register("appointments", AppointmentViewSet, basename="appointment")

urlpatterns = [
    path("", home, name="home"),
    path("services/", services_page, name="services"),
    path("login/", obtain_auth_token, name="login"),
]

urlpatterns += router.urls