# Create your views here.
from django.utils import timezone
from django.views.generic import View, TemplateView, ListView, RedirectView
from .models import Registro
from django.core.urlresolvers import reverse

class RedirectDia(RedirectView):
    permanent = False
    def get_redirect_url(self):
        now = timezone.now()
        return reverse("dia_ymd", args=[now.year, now.month, now.day])

class VistaDia(ListView):
    model = Registro
    template_name = "registro/portada.html"

    def get_queryset(self):
        self.year = int(self.kwargs["year"], 10)
        self.month = int(self.kwargs["month"], 10)
        self.day = int(self.kwargs.get("day", "0"), 10)
        return Registro.coches_dia(self.year, self.month, self.day)

    def get_context_data(self, **kwargs):
        context = super(VistaDia, self).get_context_data(**kwargs)
        dentro = context['coches_dentro'] = Registro.coches_dentro(self.year, self.month, self.day).count()
        total = context['coches_total'] = Registro.coches_dia(self.year, self.month, self.day).count()
        context['coches_fuera'] = total - dentro
        context['total_recaudado'] = Registro.total_recaudado(self.year, self.month, self.day)
        return context

class VistaMes(ListView):
    model = Registro
    template_name = "registro/portada.html"

    def get_queryset(self):
        self.year = int(self.kwargs["year"], 10)
        self.month = int(self.kwargs["month"], 10)
        return Registro.coches_dia(self.year, self.month, self.day)

    def get_context_data(self, **kwargs):
        context = super(VistaDia, self).get_context_data(**kwargs)
        dentro = context['coches_dentro'] = Registro.coches_dentro(self.year, self.month)
        total = context['coches_total'] = Registro.coches_mes(self.year, self.month).count()
        context['coches_fuera'] = total - dentro
        context['total_recaudado'] = Registro.total_recaudado(self.year, self.month)
        return context

