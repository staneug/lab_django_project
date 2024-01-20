from django import forms
from .models import Order, ClinicProfile, Option

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'optiuni': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        # Update this logic as per your model relationships
        if self.instance.pk:
            if self.instance.doctor:
                self.fields['clinica'].queryset = self.instance.doctor.clinics.all()
            if self.instance.lucrare:
                self.fields['optiuni'].queryset = self.instance.lucrare.options.all()