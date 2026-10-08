from datetime import time

from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework import serializers

from .models import (
    Appointment,
    Services,
    Staff,
)


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services

        fields = [
            "id",
            "name",
            "description",
            "price",
            "duration_minutes",
            "is_active",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff

        fields = [
            "id",
            "name",
            "age",
            "designation",
            "phone",
            "email",
            "is_active",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source="customer.username",
        read_only=True,
    )

    service_name = serializers.CharField(
        source="service.name",
        read_only=True,
    )

    staff_name = serializers.CharField(
        source="staff.name",
        read_only=True,
    )

    class Meta:
        model = Appointment

        fields = [
            "id",
            "customer",
            "customer_name",
            "service",
            "service_name",
            "staff",
            "staff_name",
            "appointment_date",
            "appointment_time",
            "status",
            "notes",
            "created_at",
        ]

        read_only_fields = [
            "customer",
            "customer_name",
            "service_name",
            "staff_name",
            "status",
            "created_at",
        ]

    def validate(self, data):
        staff = data.get("staff")
        appointment_date = data.get(
            "appointment_date"
        )
        appointment_time = data.get(
            "appointment_time"
        )

        if appointment_date is None:
            raise serializers.ValidationError(
                {
                    "appointment_date": (
                        "Appointment date is required."
                    )
                }
            )

        if appointment_time is None:
            raise serializers.ValidationError(
                {
                    "appointment_time": (
                        "Appointment time is required."
                    )
                }
            )

        today = timezone.localdate()

        if appointment_date < today:
            raise serializers.ValidationError(
                {
                    "appointment_date": (
                        "Appointment date cannot be "
                        "in the past."
                    )
                }
            )

        opening_time = time(
            hour=10,
            minute=0,
        )

        closing_time = time(
            hour=20,
            minute=0,
        )

        if not (
            opening_time
            <= appointment_time
            <= closing_time
        ):
            raise serializers.ValidationError(
                {
                    "appointment_time": (
                        "Appointments are available "
                        "between 10:00 and 20:00."
                    )
                }
            )

        if staff is None:
            return data

        already_booked = Appointment.objects.filter(
            staff=staff,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status__in=[
                "pending",
                "confirmed",
            ],
        ).exists()

        if already_booked:
            raise serializers.ValidationError(
                {
                    "appointment_time": (
                        "This staff member is already "
                        "booked for this date and time."
                    )
                }
            )

        return data

    def create(self, validated_data):
        request = self.context["request"]

        validated_data["customer"] = request.user

        return super().create(validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={
            "input_type": "password",
        },
    )

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "password",
        ]

        read_only_fields = [
            "id",
        ]

    def validate_username(self, value):
        username_exists = User.objects.filter(
            username=value
        ).exists()

        if username_exists:
            raise serializers.ValidationError(
                "This username is already taken."
            )

        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get(
                "email",
                "",
            ),
            password=validated_data["password"],
        )

        return user