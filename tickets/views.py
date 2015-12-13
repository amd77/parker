# -*- coding: utf-8 -*-

import datetime
from django.views.generic import View, FormView
from django.views.generic.dates import TodayArchiveView, DayArchiveView, MonthArchiveView
from django.utils import timezone
from django.core.files.base import ContentFile

from django.http import HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse_lazy
from empresa.views import OperarioMixin
from django.db.models import Sum
from .models import Entrada, Salida
from .forms import TicketForm, CierreForm
from inventario.models import Expendedor
from empresa.models import Abonado, Operario


class CreatePost(View):
    def post(self, request, *args, **kwargs):
        mac = request.POST.get('mac')
        codigo = request.POST.get('codigo')
        try:
            fecha_solicitud = float(request.POST.get('fecha_solicitud'))
            fecha_solicitud = datetime.datetime.fromtimestamp(fecha_solicitud)
            exp = Expendedor.objects.get(mac=mac)
            obj = Entrada.objects.create(expendedor=exp, codigo=codigo,
                                         fecha_solicitud=fecha_solicitud)

            filename = "foto_{}.jpg".format(obj.pk)
            contenido = exp.saca_foto()
            if contenido:
                obj.foto.save(filename, ContentFile(contenido))
                return HttpResponse("ok: {}".format(obj.pk))
            else:
                return HttpResponse("ok: {} (sin foto)".format(obj.pk))

        except Exception as e:
            return HttpResponseBadRequest("ko: {}".format(e))


class UpdatePost(View):
    def post(self, request, *args, **kwargs):
        codigo = request.POST.get('codigo')
        try:
            fecha_apertura = float(request.POST.get('fecha_apertura'))
            fecha_apertura = datetime.datetime.fromtimestamp(fecha_apertura)
            obj = Entrada.objects.get(codigo=codigo)
            if fecha_apertura:
                obj.fecha_apertura = fecha_apertura
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
        if round(euros, 2) == round(form.cleaned_data['euros'], 2):
            qs.update(fecha_caja=timezone.now())
        return redirect


class TicketFormView(OperarioMixin, FormView):
    template_name = "tickets/form.html"
    form_class = TicketForm
    success_url = reverse_lazy('ticket_form')
    initial = {'cobrar': '1'}

    def get_form_kwargs(self):
        kwargs = super(TicketFormView, self).get_form_kwargs()
        if kwargs.get('data'):
            data = kwargs['data'] = kwargs['data'].copy()  # make form writable!
            if data['cobrar'] != '1':
                data['cobrar'] = '1'  # hacemos paso intermedio
            elif Abonado.objects.filter(codigo=data.get('cosa')):
                data['abonado'] = data['cosa']
                data['cosa'] = ''
            elif Entrada.objects.filter(codigo=data.get('cosa')):
                data['entrada'] = data['cosa']
                data['cosa'] = ''
        return kwargs

    def form_valid(self, form):
        context = {}
        abonado = form.cleaned_data.get('abonado')
        entrada = form.cleaned_data.get('entrada')
        cobrar = form.cleaned_data.get('cobrar')
        perdido = form.cleaned_data.get('perdido', False)
        if entrada and cobrar:
            creado, salida = Salida.crea_por_entrada(entrada, self.operario, abonado, perdido)
            context['entrada'] = entrada
            context['salida'] = salida
            context['creado'] = creado
        else:
            form.data['cobrar'] = '1'
            context['form'] = form
        return self.render_to_response(self.get_context_data(**context))


class ArchiveMixin(object):
    month_format = "%m"
    allow_empty = True
    que_es = "cambiame en el hijo"
    template_name = "tickets/archive_day.html"

    def get_context_data(self, **kwargs):
        context = super(ArchiveMixin, self).get_context_data(**kwargs)
        context['cuales'] = self.kwargs['cuales'] or 'todos'
        context['que_es'] = self.que_es
        context['url_dia'] = "estadisticas_{}_day".format(self.que_es)
        context['url_mes'] = "estadisticas_{}_month".format(self.que_es)
        return context


class EntradaArchiveMixin(ArchiveMixin):
    model = Entrada
    date_field = "fecha_post"
    que_es = "entrada"

    def get_queryset(self):
        qs = super(EntradaArchiveMixin, self).get_queryset()
        qs = qs.filter(expendedor__parking=self.parking)
        if self.kwargs['cuales'] == 'caja':
            qs = qs.filter(salida__fecha_caja__isnull=False)
        elif self.kwargs['cuales'] == 'fuera':
            qs = qs.filter(salida__isnull=False)
        elif self.kwargs['cuales'] == 'dentro':
            qs = qs.filter(salida__isnull=True)
        else:
            pass
        return qs.order_by(self.date_field)


class SalidaArchiveMixin(ArchiveMixin):
    model = Salida
    date_field = "fecha"
    que_es = "salida"

    def get_queryset(self):
        qs = super(SalidaArchiveMixin, self).get_queryset()
        qs = qs.filter(entrada__expendedor__parking=self.parking)
        if self.kwargs['cuales'] == 'caja':
            qs = qs.filter(fecha_caja__isnull=False)
        else:
            pass
        return qs.order_by(self.date_field)


class EntradaTodayList(OperarioMixin, EntradaArchiveMixin, TodayArchiveView):
    pass


class SalidaTodayList(OperarioMixin, SalidaArchiveMixin, TodayArchiveView):
    pass


class EntradaDayList(OperarioMixin, EntradaArchiveMixin, DayArchiveView):
    pass


class SalidaDayList(OperarioMixin, SalidaArchiveMixin, DayArchiveView):
    pass


class ResumenMensualMixin(object):
    template_name = "tickets/archive_month.html"

    def get_context_data(self, **kwargs):
        context = super(ResumenMensualMixin, self).get_context_data(**kwargs)
        if self.que_es == "salida":
            operarios = set(context['object_list'].values_list("operario", flat=True).distinct())
        elif self.que_es == "entrada":
            operarios = set(context['object_list'].values_list("salida__operario", flat=True).distinct())
        context['operarios'] = Operario.objects.filter(pk__in=operarios)
        fechas = []

        range_key = self.date_field + "__range"
        for fecha_inicio in context['date_list']:
            fecha_fin = fecha_inicio + datetime.timedelta(days=1)
            range = {range_key: (fecha_inicio, fecha_fin)}
            qs = context['object_list'].filter(**range)
            gente = [qs.por_operario(operario) for operario in context['operarios']]
            d = {
                "fecha": fecha_inicio,
                "gente": gente,
            }
            if self.que_es == "entrada":
                d["fuera"] = qs.filter(salida__isnull=False)
                d["dentro"] = qs.filter(salida__isnull=True)
            elif self.que_es == "salida":
                d["fuera"] = qs
            fechas.append(d)
        context['fechas'] = fechas
        return context


class EntradaMonthList(OperarioMixin, ResumenMensualMixin, EntradaArchiveMixin, MonthArchiveView):
    pass


class SalidaMonthList(OperarioMixin, ResumenMensualMixin, SalidaArchiveMixin, MonthArchiveView):
    pass


class FotoToday(OperarioMixin, EntradaArchiveMixin, TodayArchiveView):
    template_name = "tickets/fotos.html"
