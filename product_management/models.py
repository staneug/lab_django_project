from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal, ROUND_HALF_UP

class UnitOfMeasurement(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class LaborDifficulty(models.Model):
    difficulty_level = models.CharField(max_length=100)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.difficulty_level

class Labor(models.Model):
    name = models.CharField(max_length=100)
    labor_difficulty = models.ForeignKey(LaborDifficulty, on_delete=models.CASCADE)
    execution_time = models.IntegerField(help_text=_("Duration in minutes"))

    def __str__(self):
        return f"{self.name} ({self.labor_difficulty.difficulty_level}) - {self.execution_time} minutes"

class RawMaterial(models.Model):
    name = models.CharField(max_length=100)
    unit_of_measurement = models.ForeignKey(UnitOfMeasurement, on_delete=models.CASCADE)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Option(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    minimum_exec_time = models.DecimalField(max_digits=5, decimal_places=2, help_text=_("Minimum execution time in days"))
    standard_exec_time = models.DecimalField(max_digits=5, decimal_places=2, help_text=_("Standard execution time in days"))
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text=_("Selling price"))
    
    raw_materials = models.ManyToManyField(RawMaterial, through='ProductRawMaterial')
    labors = models.ManyToManyField(Labor, through='ProductLabor')
    options = models.ManyToManyField(Option, through='ProductOption')

    def calculate_production_cost(self):
        materials_cost = sum(
            Decimal(prm.quantity) * prm.raw_material.price_per_unit for prm in self.productrawmaterial_set.all()
        )
        labor_cost = sum(
            (Decimal(pl.labor.execution_time) / Decimal('60')) * pl.labor.labor_difficulty.price_per_hour for pl in self.productlabor_set.all()
        )
        options_cost = sum(
            po.option.price for po in self.productoption_set.all()
        )
        total_cost = materials_cost + labor_cost + options_cost
        # Round to 2 decimal places
        return total_cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


    def calculate_production_time(self):
        # Sum the execution time of all labors related to the product
        total_minutes = sum(
            pl.labor.execution_time for pl in self.productlabor_set.all()
        )
        return total_minutes

    def calculate_yield(self):
        if self.price > 0:
            production_cost = self.calculate_production_cost()
            yield_value = ((self.price - production_cost) / self.price) * Decimal('100')
            return yield_value.quantize(Decimal('0.01'))  # Rounds the yield to 2 decimal places
        else:
            return Decimal('0')  # Yield is 0% if there is no selling price.

    def __str__(self):
        return self.name

class ProductRawMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.raw_material.name}"

class ProductLabor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    labor = models.ForeignKey(Labor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.labor.name}"

class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.option.name}"
