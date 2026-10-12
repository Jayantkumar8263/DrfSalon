from rest_framework.authtoken.models import Token
from django.db.migrations import serializer
from django.shortcuts import render # render returns an HttpResponse object with the rendered text of the template. It takes the request object, the name of the template, and a context dictionary as arguments.
from salon.models import Services
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import Appointment, Services, Staff
from .serializers import AppointmentSerializer, ServicesSerializer, StaffSerializer
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from datetime import datetime, time, timedelta
from rest_framework.exceptions import ValidationError
from datetime import datetime, time, timedelta
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from django.contrib.admin.views.decorators import (
    staff_member_required,
)
from rest_framework.authentication import (
    TokenAuthentication,
)
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

# Create your views here.

def home(request):
    services = Services.objects.filter(is_active=True)[:6]

    staff_members = Staff.objects.filter(is_active=True)[:4]

    context = {
        "services": services,
        "staff_members": staff_members,
    }# here render is used for combining templates and context data, context data vo data hai jo services variable me hai, and home.html is the template file which is used to display the data in the browser.
    return render(request, "Home/home.html", context)


def services_page(request):
    services = Services.objects.filter(is_active=True)
    return render(request,"Home/service.html",{"services": services})
@api_view(["GET", "POST"]) # it is a decorator that is used to specify the HTTP methods that are allowed for a view function. In this case, the view function service_list_api is allowed to handle GET and POST requests.
def service_list_api(request):
    if request.method == "GET":
        services = Services.objects.filter(is_active=True) # This fetches data from the database.
        serializer = ServicesSerializer(services, many=True)# services = database se aaya hua data, is line me data ko validate karta hai, checks required fields, checks field types and rules if valid, serializer.save() database me save karta hai, serializer veriable me.
        return Response(serializer.data) # Ye line us converted data ko API response me bhej raha hai.

    serializer = ServicesSerializer(data=request.data)# ye line request.data ko serializer me pass kar raha hai, jisse ki serializer ko pata chale ki data kya hai jo usko serialize karna hai, Reads incoming JSON from the request body

    if serializer.is_valid():
        service = serializer.save() # this line will save the data in the database

        return Response(
            ServicesSerializer(service).data,
            status=status.HTTP_201_CREATED
        )# this line will indicate that the request was successful and a new resource was created as a result with the status code of 201

    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ServiceViewSet(ModelViewSet):# ViewSet ek collection hota hai jisme related API actions (GET, POST, PUT, DELETE) ek hi jagah define hote hain, ModelViewSet is a class that provides the implementation for CRUD operations for a model. It provides the implementation for list, create, retrieve, update, and destroy actions.
    queryset = Services.objects.filter(is_active=True)# 
    serializer_class = ServicesSerializer# here ServicesSerializer# is line se 
    filter_backends = [OrderingFilter]
    ordering_fields = ['name', 'price']
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        return [IsAdminUser()]
    
class StaffViewSet(ModelViewSet):# is line me ek class create kiya hai jiska naam staffviewset hai.
    queryset = Staff.objects.filter(is_active=True)# this line checks the staff members that are active in the database and returns them as a queryset.
    serializer_class = StaffSerializer
    permission_classes = [AllowAny]# in this line we are converting staff members data into JSON format and returning it as a response to the client. It allows any user to access the staff members data without any authentication or authorization.

# class AppointmentViewSet(ModelViewSet):
#     .
#     serializer_class = AppointmentSerializer
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         return Appointment.objects.filter(customer=self.request.user)
    
    
class AppointmentViewSet(ModelViewSet):
    serializer_class = AppointmentSerializer

    filter_backends = [
        OrderingFilter,
    ]

    ordering_fields = [
        "appointment_date",
        "appointment_time",
        "status",
        "created_at",
    ]

    ordering = [
        "-appointment_date",
        "-appointment_time",
    ]

    def get_permissions(self):
        customer_actions = [
            "list",
            "retrieve",
            "create",
            "cancel",
        ]

        if self.action in customer_actions:
            return [
                IsAuthenticated()
            ]

        return [
            IsAdminUser()
        ]

    def get_queryset(self):
        user = self.request.user

        queryset = Appointment.objects.select_related(
            "customer",
            "service",
            "staff",
        )

        if user.is_staff:
            return queryset

        return queryset.filter(
            customer=user
        )

    @action(
        detail=True,
        methods=["post"],
    )
    def cancel(self, request, pk=None):
        appointment = self.get_object()

        if appointment.status in [
            "completed",
            "cancelled",
        ]:
            return Response(
                {
                    "detail": (
                        "This appointment cannot "
                        "be cancelled."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        appointment.status = "cancelled"

        appointment.save(
            update_fields=["status"]
        )

        serializer = self.get_serializer(
            appointment
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[
            IsAdminUser,
        ],
    )
    def confirm(self, request, pk=None):
        appointment = self.get_object()

        if appointment.status != "pending":
            return Response(
                {
                    "detail": (
                        "Only pending appointments "
                        "can be confirmed."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        appointment.status = "confirmed"

        appointment.save(
            update_fields=["status"]
        )

        serializer = self.get_serializer(
            appointment
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[
            IsAdminUser,
        ],
    )
    def complete(self, request, pk=None):
        appointment = self.get_object()

        if appointment.status != "confirmed":
            return Response(
                {
                    "detail": (
                        "Only confirmed appointments "
                        "can be completed."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        appointment.status = "completed"

        appointment.save(
            update_fields=["status"]
        )

        serializer = self.get_serializer(
            appointment
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    
class AvailabilityAPIView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def get(self, request):
        staff_id = request.query_params.get(
            "staff"
        )

        selected_date_text = request.query_params.get(
            "date"
        )

        if not staff_id:
            raise ValidationError(
                {
                    "staff": (
                        "Staff ID is required."
                    )
                }
            )

        if not selected_date_text:
            raise ValidationError(
                {
                    "date": (
                        "Date is required."
                    )
                }
            )

        try:
            selected_date = datetime.strptime(
                selected_date_text,
                "%Y-%m-%d",
            ).date()

        except ValueError:
            raise ValidationError(
                {
                    "date": (
                        "Use YYYY-MM-DD format."
                    )
                }
            )

        booked_times = set(
            Appointment.objects.filter(
                staff_id=staff_id,
                appointment_date=selected_date,
                status__in=[
                    "pending",
                    "confirmed",
                ],
            ).values_list(
                "appointment_time",
                flat=True,
            )
        )

        available_slots = []

        current_time = time(
            hour=10,
            minute=0,
        )

        closing_time = time(
            hour=20,
            minute=0,
        )

        while current_time < closing_time:
            if current_time not in booked_times:
                available_slots.append(
                    current_time.strftime("%H:%M")
                )

            current_datetime = datetime.combine(
                selected_date,
                current_time,
            )

            current_datetime += timedelta(
                minutes=30
            )

            current_time = current_datetime.time()

        return Response(
            {
                "staff": int(staff_id),
                "date": selected_date,
                "available_slots": available_slots,
            }
        )    
class RegisterAPIView(APIView):
    authentication_classes = [
        TokenAuthentication,
    ]

    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        username = request.data.get(
            "username"
        )

        email = request.data.get(
            "email"
        )

        password = request.data.get(
            "password"
        )

        if not username:
            return Response(
                {
                    "username": (
                        "Username is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not email:
            return Response(
                {
                    "email": (
                        "Email is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not password:
            return Response(
                {
                    "password": (
                        "Password is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(
            username=username
        ).exists():
            return Response(
                {
                    "username": (
                        "Username already exists."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(
            email=email
        ).exists():
            return Response(
                {
                    "email": (
                        "Email already exists."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=False,
            is_superuser=False,
        )

        token, created = Token.objects.get_or_create(
            user=user
        )

        return Response(
            {
                "detail": (
                    "Account created successfully."
                ),
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_staff": user.is_staff,
                },
            },
            status=status.HTTP_201_CREATED,
        )
    
def login(request):
    return render(request, "Home/login.html")
    

def register_page(request):
    return render(request, "Home/register.html")

def booking_page(request):
    services = Services.objects.filter(is_active=True)
    staff_members = Staff.objects.filter(is_active=True)

    context = {
        "services": services,
        "staff_members": staff_members,
    }

    return render(request, "Home/booking.html", context)

def dashboard_page(request):
    return render(
        request,
        "Home/dashboard.html",
    )

# Admin Dashboard 
@staff_member_required(login_url="/login/")  # This decorator ensures that only staff members can access the admin dashboard. If a non-staff user tries to access it, they will be redirected to the login page.
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")


def customer_profile(request):
    return render(request,"Home/profile.html")