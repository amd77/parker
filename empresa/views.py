# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .models import Empresa
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class OperarioMixin(object):
    def get_context_data(self, **kwargs):
        context = super(OperarioMixin, self).get_context_data(**kwargs)
        context['operario'] = self.operario
        context['empresa'] = self.empresa
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.operario = self.request.user.operario
        self.empresa = self.operario.empresa
        return super(OperarioMixin, self).dispatch(*args, **kwargs)



class Panel(OperarioMixin, TemplateView):
    template_name = "empresa/panel.html"
