from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from django.http import JsonResponse
from django.contrib.auth import logout

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@staff_member_required
def intermediate_save_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        # Update only specific fields (e.g., doctor and lucrare)
        doctor_id = request.POST.get('doctor', None)
        lucrare_id = request.POST.get('lucrare', None)

        if doctor_id:
            # Update the doctor field (handle exceptions as needed)
            order.doctor_id = doctor_id
        if lucrare_id:
            # Update the lucrare field (handle exceptions as needed)
            order.lucrare_id = lucrare_id

        order.save()
        return redirect(reverse('admin:order_management_order_change', args=(order.pk,)))

    # Redirect back if not a POST request or if the order is not found
    return redirect(reverse('admin:index'))

def load_clinics(request):
    # Your code to load clinics
    return JsonResponse(data)
    
def load_options(request):
    # Logic to load options goes here
    # Example: return JsonResponse({'options': options_data})
    pass
    
def logout_view(request):
    logout(request)
    return redirect('login')