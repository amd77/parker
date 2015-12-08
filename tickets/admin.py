from django.contrib import admin
from .models import Entrada, Salida


class SalidaInline(admin.TabularInline):
    model = Salida


class EntradaAdmin(admin.ModelAdmin):
    date_hierarchy = 'fecha_solicitud'
    list_display = ('codigo', 'expendedor', 'fecha_solicitud', 'fecha_apertura', 'salida')
    list_filter = ('expendedor', 'salida__operario')
    readonly_fields = ('fecha_post', )
    inlines = (SalidaInline, )
    actions = ['borra_salidas', ]

    def borra_salidas(self, request, queryset):
        for obj in queryset:
            try:
                obj.salida.delete()
            except Salida.DoesNotExist:
                pass

admin.site.register(Entrada, EntradaAdmin)
