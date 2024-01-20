from django import forms
from django.forms.models import inlineformset_factory
from .models import ClinicProfile, ShippingAddress

class ClinicProfileForm(forms.ModelForm):
    class Meta:
        model = ClinicProfile
        fields = '__all__'

ShippingAddressFormSet = inlineformset_factory(
    ClinicProfile, ShippingAddress, fields='__all__', extra=1, can_delete=True
)
