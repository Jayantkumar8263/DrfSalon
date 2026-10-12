from datetime import date, time, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Appointment, Services, Staff


class ServiceAPITests(APITestCase):
    def setUp(self):
        self.service = Services.objects.create(
            name="Hair Cut",
            description="Professional haircut",
            price=500,
            duration_minutes=45,
            is_active=True,
        )

    def test_anyone_can_list_services(self):
        url = reverse(
            "api-service-list"
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_service_data_is_returned(self):
        url = reverse(
            "api-service-list"
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data[0]["name"],
            "Hair Cut",
        )


class AppointmentAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testcustomer",
            password="StrongPassword123",
        )

        self.other_user = User.objects.create_user(
            username="othercustomer",
            password="StrongPassword123",
        )

        self.admin_user = User.objects.create_superuser(
            username="adminuser",
            email="admin@example.com",
            password="StrongPassword123",
        )

        self.service = Services.objects.create(
            name="Hair Cut",
            description="Professional haircut",
            price=500,
            duration_minutes=45,
            is_active=True,
        )

        self.staff = Staff.objects.create(
            name="Rahul",
            age=28,
            designation="Hair Stylist",
            phone="9876543210",
            email="rahul@example.com",
            is_active=True,
        )

        self.future_date = (
            date.today()
            + timedelta(days=1)
        )

    def create_appointment(
        self,
        customer=None,
        status_value="pending",
        appointment_time=time(11, 0),
    ):
        if customer is None:
            customer = self.user

        return Appointment.objects.create(
            customer=customer,
            service=self.service,
            staff=self.staff,
            appointment_date=self.future_date,
            appointment_time=appointment_time,
            status=status_value,
        )

    def test_unauthenticated_user_cannot_list_appointments(
        self,
    ):
        url = reverse(
            "api-appointment-list"
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_authenticated_user_can_create_appointment(
        self,
    ):
        self.client.force_authenticate(
            user=self.user
        )

        url = reverse(
            "api-appointment-list"
        )

        data = {
            "service": self.service.id,
            "staff": self.staff.id,
            "appointment_date": self.future_date,
            "appointment_time": time(11, 0),
            "notes": "Use scissors.",
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["customer"],
            self.user.id,
        )

    def test_user_sees_only_own_appointments(self):
        self.create_appointment(
            customer=self.user,
            appointment_time=time(11, 0),
        )

        self.create_appointment(
            customer=self.other_user,
            appointment_time=time(12, 0),
        )

        self.client.force_authenticate(
            user=self.user
        )

        url = reverse(
            "api-appointment-list"
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["customer"],
            self.user.id,
        )

    def test_admin_can_see_all_appointments(self):
        self.create_appointment(
            customer=self.user,
            appointment_time=time(11, 0),
        )

        self.create_appointment(
            customer=self.other_user,
            appointment_time=time(12, 0),
        )

        self.client.force_authenticate(
            user=self.admin_user
        )

        url = reverse(
            "api-appointment-list"
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )

    def test_customer_can_cancel_own_appointment(self):
        appointment = self.create_appointment(
            status_value="pending"
        )

        self.client.force_authenticate(
            user=self.user
        )

        url = reverse(
            "api-appointment-cancel",
            args=[appointment.id],
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        appointment.refresh_from_db()

        self.assertEqual(
            appointment.status,
            "cancelled",
        )

    def test_customer_cannot_cancel_other_users_appointment(
        self,
    ):
        appointment = self.create_appointment(
            customer=self.other_user,
            status_value="pending",
        )

        self.client.force_authenticate(
            user=self.user
        )

        url = reverse(
            "api-appointment-cancel",
            args=[appointment.id],
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_customer_cannot_cancel_completed_appointment(
        self,
    ):
        appointment = self.create_appointment(
            status_value="completed"
        )

        self.client.force_authenticate(
            user=self.user
        )

        url = reverse(
            "api-appointment-cancel",
            args=[appointment.id],
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        appointment.refresh_from_db()

        self.assertEqual(
            appointment.status,
            "completed",
        )

    def test_customer_cannot_cancel_cancelled_appointment(
        self,
    ):
        appointment = self.create_appointment(
            status_value="cancelled"
        )

        self.client.force_authenticate(
            user=self.user
        )

        url = reverse(
            "api-appointment-cancel",
            args=[appointment.id],
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        appointment.refresh_from_db()

        self.assertEqual(
            appointment.status,
            "cancelled",
        )

    def test_customer_cannot_confirm_appointment(self):
        appointment = self.create_appointment(
            status_value="pending"
        )

        self.client.force_authenticate(
            user=self.user
        )

        url = reverse(
            "api-appointment-confirm",
            args=[appointment.id],
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        appointment.refresh_from_db()

        self.assertEqual(
            appointment.status,
            "pending",
        )

    def test_admin_can_confirm_pending_appointment(self):
        appointment = self.create_appointment(
            status_value="pending"
        )

        self.client.force_authenticate(
            user=self.admin_user
        )

        url = reverse(
            "api-appointment-confirm",
            args=[appointment.id],
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        appointment.refresh_from_db()

        self.assertEqual(
            appointment.status,
            "confirmed",
        )

    def test_admin_cannot_confirm_confirmed_appointment(
        self,
    ):
        appointment = self.create_appointment(
            status_value="confirmed"
        )

        self.client.force_authenticate(
            user=self.admin_user
        )

        url = reverse(
            "api-appointment-confirm",
            args=[appointment.id],
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        appointment.refresh_from_db()

        self.assertEqual(
            appointment.status,
            "confirmed",
        )

    def test_admin_cannot_confirm_cancelled_appointment(
        self,
    ):
        appointment = self.create_appointment(
            status_value="cancelled"
        )

        self.client.force_authenticate(
            user=self.admin_user
        )

        url = reverse(
            "api-appointment-confirm",
            args=[appointment.id],
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        appointment.refresh_from_db()

        self.assertEqual(
            appointment.status,
            "cancelled",
        )

    def test_admin_can_complete_confirmed_appointment(self):
        appointment = self.create_appointment(
            status_value="confirmed"
        )

        self.client.force_authenticate(
            user=self.admin_user
        )

        url = reverse(
            "api-appointment-complete",
            args=[appointment.id],
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        appointment.refresh_from_db()

        self.assertEqual(
            appointment.status,
            "completed",
        )

    def test_admin_cannot_complete_pending_appointment(
        self,
    ):
        appointment = self.create_appointment(
            status_value="pending"
        )

        self.client.force_authenticate(
            user=self.admin_user
        )

        url = reverse(
            "api-appointment-complete",
            args=[appointment.id],
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        appointment.refresh_from_db()

        self.assertEqual(
            appointment.status,
            "pending",
        )

    def test_admin_cannot_complete_cancelled_appointment(
        self,
    ):
        appointment = self.create_appointment(
            status_value="cancelled"
        )

        self.client.force_authenticate(
            user=self.admin_user
        )

        url = reverse(
            "api-appointment-complete",
            args=[appointment.id],
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        appointment.refresh_from_db()

        self.assertEqual(
            appointment.status,
            "cancelled",
        )

    def test_non_staff_user_cannot_update_appointment(
        self,
    ):
        appointment = self.create_appointment(
            status_value="pending"
        )

        self.client.force_authenticate(
            user=self.user
        )

        url = reverse(
            "api-appointment-detail",
            args=[appointment.id],
        )

        response = self.client.patch(
            url,
            {
                "status": "confirmed",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        appointment.refresh_from_db()

        self.assertEqual(
            appointment.status,
            "pending",
        )


class AvailabilityAPITests(APITestCase):
    def setUp(self):
        self.service = Services.objects.create(
            name="Hair Cut",
            description="Professional haircut",
            price=500,
            duration_minutes=45,
            is_active=True,
        )

        self.staff = Staff.objects.create(
            name="Rahul",
            age=28,
            designation="Hair Stylist",
            phone="9876543210",
            email="rahul@example.com",
            is_active=True,
        )

        self.selected_date = (
            date.today()
            + timedelta(days=1)
        )

    def test_available_slots_are_returned(self):
        url = reverse(
            "api-availability"
        )

        response = self.client.get(
            url,
            {
                "staff": self.staff.id,
                "date": self.selected_date,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "10:00",
            response.data["available_slots"],
        )

    def test_booked_slot_is_removed(self):
        booking_user = User.objects.create_user(
            username="bookinguser",
            password="StrongPassword123",
        )

        Appointment.objects.create(
            customer=booking_user,
            service=self.service,
            staff=self.staff,
            appointment_date=self.selected_date,
            appointment_time=time(10, 0),
            status="confirmed",
        )

        url = reverse(
            "api-availability"
        )

        response = self.client.get(
            url,
            {
                "staff": self.staff.id,
                "date": self.selected_date,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertNotIn(
            "10:00",
            response.data["available_slots"],
        )

    def test_staff_parameter_is_required(self):
        url = reverse(
            "api-availability"
        )

        response = self.client.get(
            url,
            {
                "date": self.selected_date,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_date_parameter_is_required(self):
        url = reverse(
            "api-availability"
        )

        response = self.client.get(
            url,
            {
                "staff": self.staff.id,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


class AdminDashboardTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="staffuser",
            password="StrongPassword123",
            is_staff=True,
            is_active=True,
        )

        self.customer_user = User.objects.create_user(
            username="customeruser",
            password="StrongPassword123",
            is_staff=False,
            is_active=True,
        )

    def test_customer_cannot_access_admin_dashboard(self):
        self.client.login(
            username="customeruser",
            password="StrongPassword123",
        )

        response = self.client.get(
            reverse("admin-dashboard")
        )

        self.assertRedirects(
            response,
            "/login/?next=/admin-dashboard/",
        )

    def test_staff_user_can_access_admin_dashboard(self):
        self.client.login(
            username="staffuser",
            password="StrongPassword123",
        )

        response = self.client.get(
            reverse("admin-dashboard")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_inactive_staff_cannot_access_admin_dashboard(
        self,
    ):
        self.staff_user.is_active = False

        self.staff_user.save(
            update_fields=[
                "is_active",
            ]
        )

        self.client.login(
            username="staffuser",
            password="StrongPassword123",
        )

        response = self.client.get(
            reverse("admin-dashboard")
        )

        self.assertRedirects(
            response,
            "/login/?next=/admin-dashboard/",
        )


class RegisterAPITests(APITestCase):
    def test_new_registration_creates_customer_not_admin(
        self,
    ):
        response = self.client.post(
            reverse("api-register"),
            {
                "username": "newcustomer",
                "email": "customer@example.com",
                "password": "StrongPassword123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        user = User.objects.get(
            username="newcustomer"
        )

        self.assertFalse(
            user.is_staff
        )

        self.assertFalse(
            user.is_superuser
        )