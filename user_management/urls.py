from django.urls import path, include
from django.contrib.auth.views import LoginView
from .views import (
    home,
    technician_dashboard, 
    doctor_dashboard, 
    clinic_dashboard, 
    dashboard_redirect,
    login_view  # Import the login view
)
from rest_framework.routers import DefaultRouter
from .views import (CustomUserViewSet, TechnicianProfileViewSet, 
                    ClinicProfileViewSet, ShippingAddressViewSet, DoctorProfileViewSet)

# Set up the router
router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'technicians', TechnicianProfileViewSet)
router.register(r'clinics', ClinicProfileViewSet)
router.register(r'shippingaddresses', ShippingAddressViewSet)
router.register(r'doctors', DoctorProfileViewSet)

urlpatterns = [
    # Add the login URL pattern
    path('api/login', login_view, name='api_login'),
    path('accounts/login/', 
         LoginView.as_view(template_name='accounts/login.html'), 
         name='login'),
    
    # Include the router URL patterns
    path('', include(router.urls)),

    # Existing dashboard URL patterns
    path('', home, name='home'),
    path('dashboard/technician/', technician_dashboard, name='technician_dashboard'),
    path('dashboard/doctor/', doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/clinic/', clinic_dashboard, name='clinic_dashboard'),
    path('dashboard-redirect/', dashboard_redirect, name='dashboard_redirect'),
    # ... other URL patterns ...
]
