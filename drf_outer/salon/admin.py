from django.contrib import admin
from .models import Services, Staff, Appointment


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price",
        "duration_minutes",
        "is_active",
    ]

    list_filter = [
        "is_active",
    ]

    search_fields = [
        "name",
        "description",
    ]


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "age",
        "designation",
        "phone",
        "email",
        "is_active",
    ]

    list_filter = [
        "is_active",
    ]

    search_fields = [
        "name",
        "designation",
        "email",
    ]


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        "customer",
        "service",
        "staff",
        "appointment_date",
        "appointment_time",
        "status",
    ]

    list_filter = [
        "status",
        "appointment_date",
    ]

    search_fields = [
        "customer__username",
        "service__name",
        "staff__name",
    ]