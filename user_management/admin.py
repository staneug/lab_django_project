from django.contrib import admin
from .models import ClinicProfile
from .forms import ClinicProfileForm, ShippingAddressFormSet
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, TechnicianProfile, DoctorProfile, ClinicProfile, ShippingAddress

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'user_type')  # Specify the fields you want   
# Inline Admin for Profile Models
class TechnicianProfileInline(admin.StackedInline):
    model = TechnicianProfile
    can_delete = False

class DoctorProfileInline(admin.StackedInline):
    model = DoctorProfile
    can_delete = False

class ClinicProfileInline(admin.StackedInline):
    model = ClinicProfile
    can_delete = False

class ShippingAddressInline(admin.StackedInline):  # or admin.TabularInline
    model = ShippingAddress
    extra = 0  # Number of extra forms to display
    


# CustomUser Admin
class CustomUserAdmin(UserAdmin):
    inlines = [TechnicianProfileInline, DoctorProfileInline, ClinicProfileInline]
    model = CustomUser
    # Add additional fields here if you want to include them in the admin panel
    list_display = ['username', 'email', 'user_type']
    list_filter = ['user_type']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('user_type',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'user_type'),  # Fields to be displayed
        }),
    )
    

    def get_inline_instances(self, request, obj=None):
        inlines = super().get_inline_instances(request, obj)
        if not obj:  # This is the case when adding a new user
            return []  # Return no inline forms for new user creation

        # Modified part to include ShippingAddressInline for Clinic user
        if obj.user_type == 'clinic':
            return [inline for inline in inlines if isinstance(inline, (ClinicProfileInline, ShippingAddressInline))]
        elif obj.user_type == 'technician':
            return [inline for inline in inlines if isinstance(inline, TechnicianProfileInline)]
        elif obj.user_type == 'doctor':
            return [inline for inline in inlines if isinstance(inline, DoctorProfileInline)]
        return []

    # ... rest of your CustomUserAdmin configuration ...


    # You can also customize the form used for creating and editing users
    # by defining add_fieldsets attribute

# TechnicianProfile Admin
class TechnicianProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'expertise_level', 'phone_number']
    search_fields = ['user__username']

# DoctorProfile Admin
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'phone_number', 'display_clinics']
    search_fields = ['user__username']
    def display_clinics(self, obj):
        return ", ".join([clinic.company_full_name for clinic in obj.clinics.all()])
    display_clinics.short_description = 'Clinics'

# ClinicProfile Admin
class ClinicProfileAdmin(admin.ModelAdmin):
    inlines = [ShippingAddressInline]
    
    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # yield the inline formset
            yield inline.get_formset(request, obj), inline
                
    list_display = ['user', 'company_full_name', 'vat_id', 'reg_com', 'contact_person', 'contact_email']
    search_fields = ['user__username', 'company_full_name']

# ShippingAddress Admin
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['clinic', 'address']
    search_fields = ['clinic__company_full_name']

# Registering models with the admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(TechnicianProfile, TechnicianProfileAdmin)
admin.site.register(DoctorProfile, DoctorProfileAdmin)
admin.site.register(ClinicProfile, ClinicProfileAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)



