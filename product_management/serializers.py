from rest_framework import serializers
from .models import Product
from .models import Option

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['name']  # Include other fields as needed

class ProductSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'options']  # Include other fields as needed
