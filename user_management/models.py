from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import RegexValidator

# Custom User Model
class CustomUser(AbstractUser):
    # User type choices
    ADMIN = 'admin'
    TECHNICIAN = 'technician'
    DOCTOR = 'doctor'
    CLINIC = 'clinic'
    USER_TYPE_CHOICES = [
        (ADMIN, 'Admin'),
        (TECHNICIAN, 'Technician'),
        (DOCTOR, 'Doctor'),
        (CLINIC, 'Clinic'),
    ]
     
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=ADMIN)
    
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="customuser",
    )

    def __str__(self):
        return self.username

# Technician Profile Model
class TechnicianProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='technician_profile')
    expertise_level = models.IntegerField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username} - Technician"


# Clinic Profile Model
class ClinicProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='clinic_profile')
    company_full_name = models.CharField(max_length=255)
    vat_id = models.CharField(max_length=50)
    reg_com = models.CharField(max_length=50, validators=[RegexValidator(regex='^J\\d+\\/\\d+\\/\\d+$', message='Reg. Com. must be in the format J00/0000/0000')])
    billing_address = models.TextField()
    contact_person = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField()

    def __str__(self):
        return self.company_full_name

# Shipping Address Model for Clinics
class ShippingAddress(models.Model):
    clinic = models.ForeignKey(ClinicProfile, on_delete=models.CASCADE, related_name='shipping_addresses')
    address = models.TextField()

    def __str__(self):
        return self.address
        
# Doctor Profile Model
class DoctorProfile(models.Model):
    RATING_CHOICES = (
        ('Premium', 'Premium'),
        ('Standard', 'Standard'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    rating = models.CharField(max_length=10, choices=RATING_CHOICES)
    phone_number = models.CharField(max_length=15)
    clinics = models.ManyToManyField(ClinicProfile, related_name='doctors')

    # Define the relationship to ClinicProfile here if needed

    def __str__(self):
        return f"{self.user.username} - Doctor"


# Additional models or methods can be added as needed
