# -*- coding: utf-8 -*-

from django.views.generic import View, FormView
from django.views.generic.dates import TodayArchiveView, DayArchiveView, MonthArchiveView, YearArchiveView

from django.http import HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse_lazy
from empresa.views import OperarioMixin
from .models import Entrada, Salida
from .forms import TicketForm
from inventario.models import Expendedor


class CreatePost(View):
    def post(self, request, *args, **kwargs):
        mac = request.POST.get('mac')
        codigo = request.POST.get('codigo')
        fecha_solicitud = request.POST.get('fecha_solicitud')
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
        qs = qs.filter(salida__isnull=True)
        return qs.order_by('fecha_post')


class SalidaArchiveMixin(object):
    month_format = "%m"
    model = Entrada
    date_field = "fecha_post"

    def get_queryset(self):
        qs = super(SalidaArchiveMixin, self).get_queryset()
        qs = qs.filter(expendedor__parking=self.parking)
        qs = qs.filter(salida__isnull=False)
        return qs.order_by('salida__fecha')


class EntradaTodayList(OperarioMixin, EntradaArchiveMixin, TodayArchiveView):
    pass


class EntradaDayList(OperarioMixin, EntradaArchiveMixin, DayArchiveView):
    pass


class SalidaTodayList(OperarioMixin, SalidaArchiveMixin, TodayArchiveView):
    pass


class SalidaDayList(OperarioMixin, SalidaArchiveMixin, DayArchiveView):
    pass


class SalidaMonthList(OperarioMixin, SalidaArchiveMixin, MonthArchiveView):
    pass


class SalidaYearList(OperarioMixin, SalidaArchiveMixin, YearArchiveView):
    pass
