from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import CustomUser, TechnicianProfile, DoctorProfile, ClinicProfile, ShippingAddress
from .serializers import (CustomUserSerializer, TechnicianProfileSerializer, 
                          DoctorProfileSerializer, ClinicProfileSerializer, ShippingAddressSerializer)

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class TechnicianProfileViewSet(viewsets.ModelViewSet):
    queryset = TechnicianProfile.objects.all()
    serializer_class = TechnicianProfileSerializer

class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rating', 'clinics']

class ClinicProfileViewSet(viewsets.ModelViewSet):
    queryset = ClinicProfile.objects.all()
    serializer_class = ClinicProfileSerializer
    
class ShippingAddressViewSet(viewsets.ModelViewSet):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        # Authentication success
        # Implement token generation logic if using token-based authentication
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        # Authentication failed
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

def home(request):
    return render(request, 'home.html')


@login_required
def technician_dashboard(request):
    # Existing logic for technician dashboard
    return render(request, 'technician_dashboard.html')

@login_required
def doctor_dashboard(request):
    # Existing logic for doctor dashboard
    return render(request, 'doctor_dashboard.html')

@login_required
def clinic_dashboard(request):
    # Existing logic for clinic dashboard
    return render(request, 'clinic_dashboard.html')

@login_required
def dashboard_redirect(request):
    if request.user.user_type == 'technician':
        return redirect('technician_dashboard')
    elif request.user.user_type == 'doctor':
        return redirect('doctor_dashboard')
    elif request.user.user_type == 'clinic':
        return redirect('clinic_dashboard')
    elif request.user.user_type == 'admin':  
        return redirect('/admin/')  # Redirect to a custom admin dashboard
        # or use return redirect('/admin/') to use Django's built-in admin panel    
    else:
        return redirect('home')  # Replace 'home' with your default route
