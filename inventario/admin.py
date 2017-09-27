from django.contrib import admin
from .models import Tarifa, Expendedor, Barrera, Parking


class BarreraInline(admin.StackedInline):
    model = Barrera
    extra = 0


class ExpendedorInline(admin.TabularInline):
    model = Expendedor
    extra = 0


class TarifaInline(admin.TabularInline):
    model = Tarifa
    extra = 0


class ParkingAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'plazas', 'empresa')
    inlines = (BarreraInline, ExpendedorInline, TarifaInline)

admin.site.register(Parking, ParkingAdmin)
