from django.shortcuts import render # render returns an HttpResponse object with the rendered text of the template. It takes the request object, the name of the template, and a context dictionary as arguments.
from salon.models import Services
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import Appointment, Services, Staff
from .serializers import AppointmentSerializer, ServicesSerializer, StaffSerializer

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
    return render(request,"service.html",{"services": services})
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
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        return [IsAdminUser()]
    
class StaffViewSet(ModelViewSet):# is line me ek class create kiya hai jiska naam staffviewset hai.
    queryset = Staff.objects.filter(is_active=True)# this line checks the staff members that are active in the database and returns them as a queryset.
    serializer_class = StaffSerializer
    permission_classes = [AllowAny]# in this line we are converting staff members data into JSON format and returning it as a response to the client. It allows any user to access the staff members data without any authentication or authorization.

class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()# is line me Appointment model ke saare objects ko fetch kar raha hai aur queryset variable me store kar raha hai.
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Appointment.objects.filter(customer=self.request.user)
    
class AppointmentViewSet(ModelViewSet):
    serializer_class = AppointmentSerializer

    permission_classes =  [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Appointment.objects.all()

        return Appointment.objects.filter(customer=user)