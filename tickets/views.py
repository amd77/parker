# -*- coding: utf-8 -*-

from django.views.generic import View
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Entrada
from inventario.models import Expendedor


class Create(View):
    def post(self, request, *args, **kwargs):
        keys = 'codigo fecha_solicitud fecha_apertura fecha_cierre'.split()
        data = {key: request.POST.get(key) for key in keys}
        try:
            exp = Expendedor.objects.get(mac=request.POST.get('mac'))
            obj = Entrada.objects.create(expendedor=exp, **data)
            return HttpResponse("ok: {}".format(obj.pk))
        except Exception as e:
            return HttpResponseBadRequest("ko: {}".format(e))
