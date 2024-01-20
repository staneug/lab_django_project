from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from .models import (UnitOfMeasurement, LaborDifficulty, Labor, RawMaterial, Option, 
                     Product, ProductRawMaterial, ProductLabor, ProductOption)

class UnitOfMeasurementAdmin(admin.ModelAdmin):
    list_display = ['name']

class LaborDifficultyAdmin(admin.ModelAdmin):
    list_display = ['difficulty_level', 'price_per_hour']

class LaborAdmin(admin.ModelAdmin):
    list_display = ['name', 'labor_difficulty', 'execution_time']

class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit_of_measurement', 'price_per_unit']

class OptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

class ProductRawMaterialInline(admin.TabularInline):
    model = ProductRawMaterial
    extra = 1

class ProductLaborInline(admin.TabularInline):
    model = ProductLabor
    extra = 1

class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_min_exec_time', 'display_std_exec_time',
                     'display_prod_time', 'display_prod_cost', 'display_price', 'display_profit_margin')

    @admin.display(description=_('Min Exec Time'))
    def display_min_exec_time(self, obj):
        return f"{obj.minimum_exec_time} days"

    @admin.display(description=_('Std Exec Time'))
    def display_std_exec_time(self, obj):
        return f"{obj.standard_exec_time} days"
        
        
    @admin.display(description=_('Prod Time'))
    def display_prod_time(self, obj):
        total_minutes = obj.calculate_production_time()
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours}h {minutes}m" if hours else f"{minutes}m"

    @admin.display(description=_('Prod Cost'))
    def display_prod_cost(self, obj):
        return f"{obj.calculate_production_cost()} Lei"

    

    @admin.display(description=_('Price'))
    def display_price(self, obj):
        return f"{obj.price} Lei"

    @admin.display(description=_('Profit Margin'))
    def display_profit_margin(self, obj):
        margin_value = obj.calculate_yield()
        margin_percentage = f"{margin_value}%"
        # Color code based on the value of margin
        if margin_value < 20:
            color = 'red'
        elif 20 <= margin_value <= 50:
            color = 'green'
        else:
            color = 'blue'
        return mark_safe(f'<span style="color: {color};">{margin_percentage}</span>')

    inlines = [ProductRawMaterialInline, ProductLaborInline, ProductOptionInline]

admin.site.register(UnitOfMeasurement, UnitOfMeasurementAdmin)
admin.site.register(LaborDifficulty, LaborDifficultyAdmin)
admin.site.register(Labor, LaborAdmin)
admin.site.register(RawMaterial, RawMaterialAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Product, ProductAdmin)
