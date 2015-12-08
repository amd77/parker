# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Entrada
from empresa.models import Abonado


class TicketForm(forms.Form):
    cosa = forms.CharField(max_length=13, required=False, label="")
    entrada = forms.CharField(max_length=13, required=False, widget=forms.HiddenInput)
    abonado = forms.CharField(max_length=13, required=False, widget=forms.HiddenInput)

    def clean_cosa(self):
        cosa = self.cleaned_data['cosa']
        if cosa:
            raise forms.ValidationError("Desconocido")

    def clean_entrada(self):
        codigo = self.cleaned_data['entrada']
        try:
            self.entrada_obj = Entrada.objects.get(codigo=codigo)
            return self.entrada_obj
        except Entrada.DoesNotExist:
            return None

    def clean_abonado(self):
        codigo = self.cleaned_data['abonado']
        try:
            self.abonado_obj = Abonado.objects.get(codigo=codigo)
            return self.abonado_obj
        except Abonado.DoesNotExist:
            return None


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
        total = d['billete_50'] * 50 + \
            d['billete_20'] * 20 + \
            d['billete_10'] * 10 + \
            d['billete_5'] * 5 + \
            d['moneda_2'] * 2 + \
            d['moneda_1'] * 1 + \
            d['moneda_50c'] * 0.50 + \
            d['moneda_20c'] * 0.20 + \
            d['moneda_10c'] * 0.10 + \
            d['moneda_5c'] * 0.05 + \
            d['moneda_2c'] * 0.02 + \
            d['moneda_1c'] * 0.01
        diferencia = d['euros'] - total
        if diferencia > 0.005:
            raise forms.ValidationError("La suma da {:.2f} y faltan {:.2f} €".format(total, diferencia))
        elif diferencia < -0.005:
            raise forms.ValidationError("La suma da {:.2f} y sobran {:.2f} €".format(total, -diferencia))
