# -*- coding: utf-8 -*-

from django.http import Http404
from django.views.generic import TemplateView, RedirectView
from empresa.views import OperarioMixin
from .models import Barrera


class Tarifas(OperarioMixin, TemplateView):
    template_name = "inventario/tarifas.html"


class BarreraComando(OperarioMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        try:
            barrera = Barrera.objects.get(slug=self.kwargs['slug'])
        except Barrera.DoesNotExist:
            raise Http404("Barrera desconocida")
        comando = self.kwargs['comando']
        if comando == "abre":
            barrera.abre()
        elif comando == "abresiempre":
            barrera.abresiempre()
        elif comando == "cierra":
            barrera.cierra()
        else:
            raise Http404("Comando desconocido")
        # FIXME esto es cutre, lo mejor sería AJAX
        return "../.."
