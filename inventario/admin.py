from django.contrib import admin
from .models import Tarifa, Expendedor, Barrera, Parking, NodoRemoto, ComandoRemoto


class BarreraInline(admin.StackedInline):
    model = Barrera
    extra = 0


class ExpendedorInline(admin.TabularInline):
    model = Expendedor
    extra = 0


class TarifaInline(admin.TabularInline):
    model = Tarifa
    extra = 0


class ComandoInline(admin.TabularInline):
    model = ComandoRemoto
    extra = 0


class RemotoAdmin(admin.ModelAdmin):
    model = NodoRemoto
    extra = 0
    inlines = (ComandoInline,)


class ParkingAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'plazas', 'empresa')
    inlines = (BarreraInline, ExpendedorInline, TarifaInline)

admin.site.register(Parking, ParkingAdmin)
admin.site.register(NodoRemoto, RemotoAdmin)
