from rest_framework import serializers
from .models import Order, Option
from user_management.serializers import DoctorProfileSerializer, ClinicProfileSerializer
from product_management.serializers import ProductSerializer, OptionSerializer

class OrderSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer(read_only=True)
    clinica = ClinicProfileSerializer(read_only=True)
    lucrare = ProductSerializer(read_only=True)
    optiuni_names = serializers.SerializerMethodField()
    data_intrare = serializers.SerializerMethodField()  
    termen = serializers.SerializerMethodField()      
  

    class Meta:
        model = Order
        fields = ['id', 'nume_pacient', 'data_intrare', 'termen', 'urgent', 'urgent_due_date', 'comments', 'status', 'doctor', 'clinica', 'lucrare', 'optiuni', 'optiuni_names']

    def get_optiuni_names(self, obj):
        # Concatenate the names of all options
        return ', '.join([option.name for option in obj.lucrare.options.all()]) if obj.lucrare and obj.lucrare.options.exists() else ''

    def get_data_intrare(self, obj):
        return obj.data_intrare.strftime('%d-%m-%Y') if obj.data_intrare else None

    def get_termen(self, obj):
        return obj.termen.strftime('%d-%m-%Y') if obj.termen else None


