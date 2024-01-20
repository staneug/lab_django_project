from django.db import models
from django.utils import timezone
import datetime
from user_management.models import DoctorProfile, ClinicProfile
from product_management.models import Product, Option

class Order(models.Model):
    nume_pacient = models.CharField(max_length=255, verbose_name="Nume Pacient")
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, verbose_name="Doctor")
    clinica = models.ForeignKey(ClinicProfile, on_delete=models.CASCADE, verbose_name="Clinica")
    lucrare = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Lucrare")
    optiuni = models.ManyToManyField(Option, verbose_name="Optiuni")
    data_intrare = models.DateTimeField(default=timezone.now, verbose_name="Data Intrare")
    termen = models.DateField(verbose_name="Termen")
    urgent = models.BooleanField(default=False, verbose_name="Urgent")
    urgent_due_date = models.DateField(blank=True, null=True, verbose_name="Urgent Due Date")
    comments = models.TextField(blank=True, null=True, verbose_name="Comentarii")
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        # Add more status choices as needed
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name="Status")

    def save(self, *args, **kwargs):
        # Logic for calculating 'termen' considering 'urgent' and 'urgent_due_date'
        if not self.id:  # Check if it's a new order
            if self.urgent and self.urgent_due_date:
                self.termen = self.urgent_due_date
            else:
                self.termen = self.calculate_termen()
        super(Order, self).save(*args, **kwargs)

    def calculate_termen(self):
        # Placeholder for termen calculation logic
        # Adjust this method to calculate the due date based on 'lucrare' and exclude weekends
        standard_exec_time = self.lucrare.standard_exec_time  # Assuming this is in days
        termen = timezone.now().date()
        while standard_exec_time > 0:
            termen += datetime.timedelta(days=1)
            # Skip weekends
            if termen.weekday() < 5:  # 0 is Monday, 4 is Friday
                standard_exec_time -= 1
        return termen

    def __str__(self):
        return f"Order {self.id} - {self.nume_pacient}"
