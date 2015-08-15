from django.contrib import admin
from .models import Entrada, Salida


class SalidaInline(admin.TabularInline):
    model = Salida


class EntradaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'expendedor', 'fecha_solicitud', 'salida')
    list_filter = ('expendedor', )
    readonly_fields = ('fecha_post', )
    inlines = (SalidaInline, )

admin.site.register(Entrada, EntradaAdmin)
