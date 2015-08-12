# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from empresa.views import OperarioMixin


class Tarifas(OperarioMixin, TemplateView):
    template_name = "inventario/tarifas.html"
