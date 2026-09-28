from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class Services(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): # this line is used to show how the object appears in admin and the Django shell
        return self.name
    
class Staff(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    designation = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(User,on_delete=models.CASCADE, related_name="appointments")
    service = models.ForeignKey(Services, on_delete=models.PROTECT,related_name="appointments")
    staff = models.ForeignKey(
    "Staff",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="appointments"
)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="pending")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} - {self.service.name}"