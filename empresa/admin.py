from django.contrib import admin
from .models import Empresa, Operario, Abonado, Factura


class OperarioInline(admin.TabularInline):
    model = Operario
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False

class AbonadoInline(admin.TabularInline):
    model = Abonado
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cif', 'ultima_factura')
    inlines = [OperarioInline, AbonadoInline]

    def has_delete_permission(self, request, obj=None):
        return False

class FacturaAdmin(admin.ModelAdmin):
    list_filter = ('empresa', )
    list_display = ('numero', 'nombre', 'fecha', 'importe')

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Factura, FacturaAdmin)
