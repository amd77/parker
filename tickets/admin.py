from django.contrib import admin
from .models import Entrada, Salida


class SalidaInline(admin.TabularInline):
    model = Salida


class EntradaAdmin(admin.ModelAdmin):
    date_hierarchy = 'fecha_solicitud'
    list_display = ('codigo', 'expendedor', 'fecha_solicitud', 'fecha_apertura', 'salida')
    list_filter = ('expendedor', )
    readonly_fields = ('fecha_post', )
    inlines = (SalidaInline, )

admin.site.register(Entrada, EntradaAdmin)
