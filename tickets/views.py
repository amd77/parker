# -*- coding: utf-8 -*-

from django.views.generic import View, FormView
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse_lazy
from empresa.views import OperarioMixin
from .models import Entrada, Salida
from .forms import TicketForm
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


class TicketFormView(OperarioMixin, FormView):
    template_name = "tickets/form.html"
    form_class = TicketForm
    success_url = reverse_lazy('ticket_form')

    def form_valid(self, form):
        context = {}
        creado, salida = Salida.crea_por_entrada(form.entrada, self.operario)
        context['entrada'] = form.entrada
        context['salida'] = salida
        context['creado'] = creado
        return self.render_to_response(self.get_context_data(**context))
