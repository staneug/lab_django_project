from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('nume_pacient', 'doctor', 'clinica', 'lucrare', 'data_intrare', 'termen', 'status')
    list_filter = ('doctor', 'clinica', 'lucrare', 'status')
    search_fields = ('nume_pacient', 'doctor__user__username', 'clinica__company_full_name', 'lucrare__name')
    readonly_fields = ('data_intrare', 'termen')

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(doctor__user=request.user)

admin.site.register(Order, OrderAdmin)
