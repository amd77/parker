# -*- coding: utf-8 -*-

import datetime
from django.views.generic import View, FormView
from django.views.generic.dates import TodayArchiveView, DayArchiveView, MonthArchiveView, YearArchiveView
from django.utils import timezone

from django.http import HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse_lazy
from empresa.views import OperarioMixin
from django.db.models import Sum
from .models import Entrada, Salida
from .forms import TicketForm, CierreForm
from inventario.models import Expendedor


class CreatePost(View):
    def post(self, request, *args, **kwargs):
        mac = request.POST.get('mac')
        codigo = request.POST.get('codigo')
        fecha_solicitud = float(request.POST.get('fecha_solicitud'))
        fecha_solicitud = datetime.datetime.fromtimestamp(fecha_solicitud)
        try:
            exp = Expendedor.objects.get(mac=mac)
            obj = Entrada.objects.create(expendedor=exp, codigo=codigo,
                                         fecha_solicitud=fecha_solicitud)
            return HttpResponse("ok: {}".format(obj.pk))
        except Exception as e:
            return HttpResponseBadRequest("ko: {}".format(e))


class UpdatePost(View):
    def post(self, request, *args, **kwargs):
        codigo = request.POST.get('codigo')
        fecha_apertura = request.POST.get('fecha_apertura')
        fecha_cierre = request.POST.get('fecha_cierre')
        try:
            obj = Entrada.objects.get(codigo=codigo)
            if fecha_apertura:
                obj.fecha_apertura = fecha_apertura
            if fecha_cierre:
                obj.fecha_cierre = fecha_cierre
            obj.save()
            return HttpResponse("ok: {}".format(obj.pk))
        except Exception as e:
            return HttpResponseBadRequest("ko: {}".format(e))


class CierreView(OperarioMixin, FormView):
    template_name = "tickets/cierre.html"
    form_class = CierreForm
    # success_url = reverse_lazy('logout')
    success_url = reverse_lazy('ticket_cierre')

    def get_queryset(self):
        return self.operario.salida_set.de_hoy().sin_cerrar()

    def get_initial(self):
        qs = self.get_queryset()
        euros = qs.aggregate(out=Sum('euros'))['out'] or 0.0
        return {'euros': euros}

    def get_context_data(self, **kwargs):
        context = super(CierreView, self).get_context_data(**kwargs)
        qs = self.get_queryset()
        context['object_list'] = qs
        context['primer_ticket'] = qs.first()
        context['ultimo_ticket'] = qs.last()
        context['numero_tickets'] = qs.count()
        context['euros'] = qs.aggregate(out=Sum('euros'))['out'] or 0.0
        return context

    def form_valid(self, form):
        redirect = super(CierreView, self).form_valid(form)
        qs = self.get_queryset()
        euros = qs.aggregate(out=Sum('euros'))['out'] or 0.0
        if euros == form.cleaned_data['euros']:
            qs.update(fecha_caja=timezone.now())
        return redirect


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


class EntradaArchiveMixin(object):
    month_format = "%m"
    model = Entrada
    date_field = "fecha_post"

    def get_queryset(self):
        qs = super(EntradaArchiveMixin, self).get_queryset()
        qs = qs.filter(expendedor__parking=self.parking)
        # qs = qs.filter(salida__isnull=True)
        return qs.order_by('fecha_post')


class EntradaTodayList(OperarioMixin, EntradaArchiveMixin, TodayArchiveView):
    pass


class EntradaDayList(OperarioMixin, EntradaArchiveMixin, DayArchiveView):
    pass


class EntradaMonthList(OperarioMixin, EntradaArchiveMixin, MonthArchiveView):
    def get_context_data(self, **kwargs):
        context = super(EntradaMonthList, self).get_context_data(**kwargs)
        context['operarios'] = self.empresa.operario_set.filter(es_administrador=False)
        fechas = []

        for fecha_inicio in context['date_list']:
            fecha_fin = fecha_inicio + datetime.timedelta(days=1)
            qs = context['object_list'].filter(fecha_post__range=(fecha_inicio, fecha_fin))
            qs_caja = qs.filter(salida__fecha_caja__isnull=False)
            gente = [qs_caja.por_operario(operario) for operario in context['operarios']]
            d = {
                "fecha": fecha_inicio,
                "dentro": qs,
                "fuera": qs.filter(salida__isnull=False),
                "caja": qs.filter(salida__fecha_caja__isnull=False),
                "gente": gente,
            }
            fechas.append(d)
        context['fechas'] = fechas
        return context


class EntradaYearList(OperarioMixin, EntradaArchiveMixin, YearArchiveView):
    pass
