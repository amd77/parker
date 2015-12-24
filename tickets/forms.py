# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Entrada, Salida
from empresa.models import Abonado


class TicketForm(forms.Form):
    cosa = forms.CharField(max_length=13, required=False, label="")
    entrada = forms.CharField(max_length=13, required=False, widget=forms.HiddenInput)
    abonado = forms.CharField(max_length=13, required=False, widget=forms.HiddenInput)
    cobrar = forms.BooleanField(required=False, widget=forms.HiddenInput)
    perdido = forms.BooleanField(required=False, widget=forms.HiddenInput)

    def clean_entrada(self):
        codigo = self.cleaned_data['entrada']
        try:
            entrada = Entrada.objects.get(codigo=codigo)
        except Entrada.DoesNotExist:
            return None
        try:
            if entrada.salida:
                self.add_error("cosa", "Ticket {} ya validado".format(codigo))
                return None
        except Salida.DoesNotExist:
            pass

        self.entrada_obj = entrada
        return entrada

    def clean_abonado(self):
        codigo = self.cleaned_data['abonado']
        try:
            abonado = Abonado.objects.get(codigo=codigo)
        except Abonado.DoesNotExist:
            return None

        self.abonado_obj = abonado
        return abonado


class CierreForm(forms.Form):
    billete_50 = forms.IntegerField(label="50€", initial=0)
    billete_20 = forms.IntegerField(label="20€", initial=0)
    billete_10 = forms.IntegerField(label="10€", initial=0)
    billete_5 = forms.IntegerField(label="5€", initial=0)
    moneda_2 = forms.IntegerField(label="2€", initial=0)
    moneda_1 = forms.IntegerField(label="1€", initial=0)
    moneda_50c = forms.IntegerField(label="50¢", initial=0)
    moneda_20c = forms.IntegerField(label="20¢", initial=0)
    moneda_10c = forms.IntegerField(label="10¢", initial=0)
    moneda_5c = forms.IntegerField(label="5¢", initial=0)
    moneda_2c = forms.IntegerField(label="2¢", initial=0)
    moneda_1c = forms.IntegerField(label="1¢", initial=0)
    euros = forms.FloatField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(CierreForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-4'
        self.helper.add_input(Submit('submit', 'Cerrar caja'))

    def clean(self):
        d = super(CierreForm, self).clean()
        total = \
            d.get('billete_50', 0) * 50 + \
            d.get('billete_20', 0) * 20 + \
            d.get('billete_10', 0) * 10 + \
            d.get('billete_5', 0) * 5 + \
            d.get('moneda_2', 0) * 2 + \
            d.get('moneda_1', 0) * 1 + \
            d.get('moneda_50c', 0) * 0.50 + \
            d.get('moneda_20c', 0) * 0.20 + \
            d.get('moneda_10c', 0) * 0.10 + \
            d.get('moneda_5c', 0) * 0.05 + \
            d.get('moneda_2c', 0) * 0.02 + \
            d.get('moneda_1c', 0) * 0.01
        diferencia = d['euros'] - total
        if diferencia > 0.005:
            raise forms.ValidationError("La suma da {:.2f} y faltan {:.2f} €".format(total, diferencia))
        elif diferencia < -0.005:
            raise forms.ValidationError("La suma da {:.2f} y sobran {:.2f} €".format(total, -diferencia))
