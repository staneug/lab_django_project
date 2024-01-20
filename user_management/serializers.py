from rest_framework import serializers
from .models import CustomUser, TechnicianProfile, DoctorProfile, ClinicProfile, ShippingAddress

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

# Forward declaration of ClinicProfileSerializer
class ClinicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicProfile
        fields = '__all__'



class TechnicianProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = TechnicianProfile
        fields = '__all__'

class DoctorProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    clinics = ClinicProfileSerializer(many=True, read_only=True)

    class Meta:
        model = DoctorProfile
        fields = '__all__'

# Now define ClinicProfileSerializer properly
class ClinicProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = ClinicProfile
        fields = '__all__'

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'