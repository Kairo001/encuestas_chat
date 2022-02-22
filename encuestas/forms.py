""" Formularios para la app de encuestas. """

# Django
from encuestas.models import Encuesta, CampoEncuesta
from django import forms

# Utilidades
import re
import json


class EncuestaForm(forms.ModelForm):
    """ Form para Encuesta. """
    
    class Meta:
        model = Encuesta
        fields = ('nombre', 'descripcion')

class CampoEncuestaForm(forms.ModelForm):
    """ Form para el campo de una encuesta. """

    lista_valores = forms.MultipleChoiceField(required=False)
    valor_item = forms.CharField(required=False)

    class Meta:
        model = CampoEncuesta
        fields = ('encuesta', 'nombre_campo', 'tipo', 'values_select', 'is_required')
        widgets = {
            'encuesta': forms.HiddenInput(),
            'values_select': forms.HiddenInput(),
        }
    
    def clean_nombre_campo(self):
        formulario = self.cleaned_data.get('encuesta')
        nombre_campo = self.cleaned_data.get('nombre_campo')
        nombre_campo = re.sub(r"\s+", "_", nombre_campo)
        if formulario.campos.filter(nombre_campo=nombre_campo).exists():
            raise forms.ValidationError('No se puede crear un campo ya existente.')
        
        return self.cleaned_data.get('nombre_campo')

    def clean_values_select(self):
        tipo = self.cleaned_data.get('tipo')
        if not tipo == CampoEncuesta.TIPO_LISTA:
            return None
        values_select = self.cleaned_data.get('values_select')
        if values_select == '':
            raise forms.ValidationError('La lista no puede estar vacía.')

        try: 
            lista_values_select = json.loads(values_select)
        except ValueError:
            raise forms.ValidationError('Formato inválido')

        if type(lista_values_select) is not list:
            raise forms.ValidationError('Formato inválido')

        if len(lista_values_select) == 0:
            raise forms.ValidationError('La lista no puede estar vacía')

        return values_select
    
class EncuestaFinalForm(forms.Form):
    """ Form para generar el formulario resultante de la creación de la encuesta. """

    def __init__(self, campos, *args, **kwargs):
        super(EncuestaFinalForm, self).__init__(*args, **kwargs)

        for campo in campos:
            if campo.tipo is CampoEncuesta.TIPO_TEXTO:
                self.fields[campo.nombre_campo] = forms.CharField(
                    label=campo.nombre_campo, widget=forms.TextInput(
                        attrs={'class' : 'form-control', 'id': campo.id}
                    ),
                    required=campo.is_required
                )
            elif campo.tipo is CampoEncuesta.TIPO_FECHA:
                self.fields[campo.nombre_campo] = forms.CharField(
                    label=campo.nombre_campo, widget=forms.TextInput(
                        attrs={'class' : 'class-fecha form-control', 'id': campo.id}
                    ),
                    required=campo.is_required
                )
            elif campo.tipo is CampoEncuesta.TIPO_LISTA:
                choices = [(option, option)
                           for option in json.loads(campo.values_select)]
                self.fields[campo.nombre_campo] = forms.ChoiceField(
                    choices=choices,
                    label=campo.nombre_campo, widget=forms.Select(
                        attrs={'class' : 'form-control', 'id': campo.id}
                    ),
                    required=campo.is_required
                )
            elif campo.tipo is CampoEncuesta.TIPO_TEXTO_AREA:
                self.fields[campo.nombre_campo] = forms.CharField(
                    label=campo.nombre_campo, widget=forms.Textarea(
                        attrs={'class': 'form-control', 'rows': "3", 'id': campo.id}
                    ),
                    required=campo.is_required
                )