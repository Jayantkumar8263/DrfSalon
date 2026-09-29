from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Services, Staff, Appointment

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:#class Meta sirf yeh batata hai ki Django aapke logic ko kaise handle kare — uska behavior, uska look, uski rules.
        model = Services
        fields = ['id', 'name', 'description', 'price', 'duration_minutes', 'is_active', 'created_at'] # here fields is used to convert the fields to be in the jason format
        read_only_fields = ['id', 'created_at']

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'name', 'age', 'designation', 'phone', 'email', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
        
class AppointmentSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    staff_name = serializers.CharField(source='staff.name', read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'customer', 'service', 'staff', 'appointment_date', 'appointment_time', 'status', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at', 'customer']
    
    def create(self, validated_data):
        request = self.context['request']
        validated_data["customer"] = request.user
        return super().create(validated_data)
    
    def validate(self, data):
        staff = data.get("staff")
        appointment_date = data.get("appointment_date")
        appointment_time = data.get("appointment_time")

        if staff is None:
            return data

        already_booked = Appointment.objects.filter(
            staff=staff,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
        status__in=["pending", "confirmed"],
    ).exists()

        if already_booked:
            raise serializers.ValidationError(
            {
                "appointment_time": (
                    "This staff member is already booked "
                    "for this date and time."
                )
            }
        )

        return data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length= 4, style={"input_type": "password"}) # Password request mein accept hoga, lekin response mein return nahi hoga, iska matlab hai ki password ko write_only banaya gaya hai, taki wo sirf input ke liye ho aur output mein na aaye.

    class Meta:
        model = User
        fields = ["id", "username", "email", "password",]

        read_only_fields = ["id"]

    def validate_username(self, value): # ye line username ko validate karne ke liye hai, agar username already exist karta hai to ye error raise karega.
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def create(self, validated_data): # ye function user ko create karne ke liye hai, ye validated_data ko use karke user create karega.    
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )

        return user
