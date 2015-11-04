# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from .models import Entrada


class TicketForm(forms.Form):
    codigo = forms.CharField(max_length=13)

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        try:
            self.entrada = Entrada.objects.get(codigo=codigo)
        except Entrada.DoesNotExist:
            raise forms.ValidationError("Código no se encuentra")
        return codigo


class CierreForm(forms.Form):
    confirmacion = forms.BooleanField()
