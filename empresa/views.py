# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone


class OperarioMixin(object):
    def get_context_data(self, **kwargs):
        context = super(OperarioMixin, self).get_context_data(**kwargs)
        context['operario'] = self.operario
        context['empresa'] = self.empresa
        context['parking'] = self.parking
        context['now'] = timezone.now()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.operario = self.request.user.operario
        self.empresa = self.operario.empresa
        self.parking = self.empresa.parking
        return super(OperarioMixin, self).dispatch(*args, **kwargs)
