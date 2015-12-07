from django.forms import ModelForm
from .models import Registro


class RegistroForm(ModelForm):
    class Meta:
        model = Registro
        fields = ['matricula', 'fecha_entrada', 'fecha_salida']
