""" Vistas para la app de encuestas """

# Djang
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView, CreateView, DeleteView, FormView, View, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

# Formularios
from encuestas.forms import EncuestaForm, CampoEncuestaForm, EncuestaFinalForm

# Modelos
from encuestas.models import Encuesta, CampoEncuesta, RespuestaCampo

# Utilidades
import ast
import numpy as np
import json

class EncuestaCreateView(LoginRequiredMixin, CreateView):
    """ Vista para crear una encuesta. """
    login_url = 'login'
    model = Encuesta
    form_class = EncuestaForm
    template_name = 'encuestas/crear_encuesta.html'

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)

        return redirect('lista_encuestas_realizar')
        
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(EncuestaCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('campo_encuesta', kwargs={"pk_encuesta": self.object.pk})

class CampoEncuestaCreateView(LoginRequiredMixin, CreateView):
    """ Vista para crear un campo de la encuesta. """
    login_url = 'login'
    model = CampoEncuesta
    template_name = "encuestas/encuesta_campo.html"
    form_class = CampoEncuestaForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)

        return redirect('lista_encuestas_realizar')

    def get_initial(self):
        initial = super(CampoEncuestaCreateView, self).get_initial()
        encuesta = Encuesta.objects.get(pk=self.kwargs['pk_encuesta'])
        initial.update({'encuesta': encuesta.id})
        return initial

    def get_context_data(self, **kwargs):
        context = super(CampoEncuestaCreateView, self).get_context_data(**kwargs)
        encuesta = Encuesta.objects.get(pk=self.kwargs['pk_encuesta'])
        context['encuesta'] = encuesta
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        message = 'No se pudo llevar a cabo la creacion del campo.'
        messages.add_message(
            self.request,
            messages.ERROR,
            message,
        )
        return super(CampoEncuestaCreateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('campo_encuesta', kwargs={"pk_encuesta": self.kwargs['pk_encuesta']})

class CampoEncuestaDeleteView(LoginRequiredMixin, DeleteView):
    """ Vista para eliminar un campo de la encuesta. """
    login_url = 'login'
    model=CampoEncuesta
    template_name = "encuestas/campoencuesta_confirm_delete.html"

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)

        return redirect('lista_encuestas_realizar')

    def delete(self, request, *args, **kwargs):
        message = " Se eliminó con éxito el campo."

        messages.add_message(
            self.request,
            messages.SUCCESS,
            message,
        )
        return super(CampoEncuestaDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('campo_encuesta', kwargs={"pk_encuesta": self.kwargs['pk_encuesta']})

class VistaPreviaFormView(LoginRequiredMixin, FormView):
    """ Vita para visualizar la encuesta una vez finalizada. """
    login_url = 'login'
    form_class = EncuestaFinalForm
    template_name = "encuestas/vista_previa.html"
    
    def dispatch(self, request, *args, **kwargs):

        if not (request.user.is_manager):
            return redirect('lista_encuestas_realizar')

        encuesta = Encuesta.objects.get(pk=self.kwargs['pk_encuesta'])
        campos = encuesta.campos.all()

        if not campos.exists():
            message = "No se puede crear una encuesta vacía"
            messages.add_message(
                self.request,
                messages.ERROR,
                message,
            )
            return redirect(reverse('campo_encuesta', kwargs={"pk_encuesta": self.kwargs['pk_encuesta']}))
        return super(VistaPreviaFormView, self).dispatch(request, *args, **kwargs)
    
    def get_form(self):
        self.form_class = self.get_form_class()
        encuesta = Encuesta.objects.get(pk=self.kwargs['pk_encuesta'])
        campos = encuesta.campos.all()
        return self.form_class(campos=campos, **self.get_form_kwargs())    

    def get_context_data(self, **kwargs):
        context =  super(VistaPreviaFormView, self).get_context_data(**kwargs)
        context['pk_encuesta'] = self.kwargs['pk_encuesta']
        return context

class ListaEncuestasListView(LoginRequiredMixin, ListView):
    """ Vista para listar las encuestas. """
    login_url = 'login'
    model = Encuesta
    template_name = "encuestas/lista_encuestas.html"

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)

        return redirect('lista_encuestas_realizar')
    
    def get_queryset(self):
        return self.request.user.encuestas.all()

class EncuestaDeleteView(LoginRequiredMixin, DeleteView):
    """ Vista para eliminar una encuesta """
    login_url = 'login'
    model = Encuesta
    template_name = "encuestas/eliminar_encuesta.html"

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)

        return redirect('lista_encuestas_realizar')

    def get_object(self, queryset=None):
        return Encuesta.objects.get(pk=self.kwargs['pk_encuesta'])

    def get_success_url(self):
        return reverse('lista_encuestas')

class TerminarEncuestaView(LoginRequiredMixin, View):
    """ Vista para enviar al front si la encuesta que si quiere erminar tiene o no respuestas. """
    login_url = 'login'
    def get(self, request, *args, **kwargs):
        encuesta = Encuesta.objects.get(pk=request.GET['pk_encuesta'])
        
        respuestas = encuesta.respuestas.all()

        respuesta = {}

        if respuestas.exists():
            respuesta['terminar'] = True
        else:
            respuesta['terminar'] = False


        return JsonResponse(respuesta)

class EncuestaUpdateView(LoginRequiredMixin, View):
    """ Vista para actualizar el estado de la encuesta a Terminada """
    login_url = 'login'
    def dispatch(self, request, *args, **kwargs):

        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)

        return redirect('lista_encuestas_realizar')

    def post(self, request, *args, **kwargs):
        post_data = json.loads(request.body.decode("utf-8"))
        encuesta = Encuesta.objects.get(pk=post_data['pk_encuesta'])
        encuesta.estado_terminado = True
        encuesta.save()

        return JsonResponse({'respuesta':'success'})

class ActivarEncuestaView(LoginRequiredMixin, View):
    """ Vista para actualizar el estado de la encuesta a Terminada """
    login_url = 'login'
    def dispatch(self, request, *args, **kwargs):

        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)

        return redirect('lista_encuestas_realizar')

    def post(self, request, *args, **kwargs):

        post_data = json.loads(request.body.decode("utf-8"))
        
        try:
            encuesta = Encuesta.objects.get(pk=post_data['pk_encuesta'])
            encuesta.is_active = True
            encuesta.save()
            respuesta = {'actualizado' : True}
        except:
            respuesta = {'actualizado' : False}

        return JsonResponse(respuesta)

class EncuestaAgenteTemplateView(LoginRequiredMixin, TemplateView):
    """ Vista para que el agente gestione el proceso de realización de una encuesta. """
    login_url = 'login'
    template_name = "encuestas/encuesta_agente.html"

    def dispatch(self, request, *args, **kwargs):

        if Encuesta.objects.get(pk=self.kwargs['pk_encuesta']).estado_terminado == True:
            return redirect('lista_encuestas')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EncuestaAgenteTemplateView, self).get_context_data(**kwargs)
        encuesta = Encuesta.objects.get(pk=self.kwargs['pk_encuesta'])
        preguntas = encuesta.campos.all()
        context['encuesta'] = encuesta
        context['preguntas'] = preguntas
        return context
        

class EncuestaVistaFormView(LoginRequiredMixin, FormView):
    """ Vista para visualizar la encuesta en una vista previa. """
    login_url = 'login'
    form_class = EncuestaFinalForm
    template_name = 'encuestas/vista_encuesta.html'

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)

        return redirect('lista_encuestas_realizar')

    def get_form(self):
        self.form_class = self.get_form_class()
        encuesta = Encuesta.objects.get(pk=self.kwargs['pk_encuesta'])
        campos = encuesta.campos.all()
        return self.form_class(campos=campos, **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(EncuestaVistaFormView, self).get_context_data(**kwargs)
        context['pk_encuesta'] = self.kwargs['pk_encuesta']
        return context

class ListaEncuestasRealizarListView(LoginRequiredMixin, ListView):
    """ Vista para listar las encuestas. """
    login_url = 'login'
    model = Encuesta
    template_name = "encuestas/lista_encuestas_realizar.html"

    def get_context_data(self, **kwargs):
        context =  super(ListaEncuestasRealizarListView, self).get_context_data(**kwargs)

        for i in range(len(context['object_list'])):
            setattr(context['object_list'][i], 'ha_sido_diligenciada', RespuestaCampo.objects.filter(encuesta=context['object_list'][i], user=self.request.user).exists())

        print(context['object_list'][0].ha_sido_diligenciada)

        return context

class RealizarEncuestaFormView(LoginRequiredMixin, FormView):
    """ Vista para realizar la encuesta. """
    login_url = 'login'
    form_class = EncuestaFinalForm
    template_name = 'encuestas/realizar_encuesta.html'
    success_url = reverse_lazy('lista_encuestas_realizar')

    def dispatch(self, request, *args, **kwargs):

        if Encuesta.objects.get(pk=self.kwargs['pk_encuesta']).estado_terminado == True:
            return redirect('lista_encuestas_realizar')

        return super().dispatch(request, *args, **kwargs)

    def get_form(self):
        self.form_class = self.get_form_class()
        encuesta = Encuesta.objects.get(pk=self.kwargs['pk_encuesta'])
        campos = encuesta.campos.all()
        return self.form_class(campos=campos, **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(RealizarEncuestaFormView, self).get_context_data(**kwargs)
        encuesta = Encuesta.objects.get(pk=self.kwargs['pk_encuesta'])
        campos = encuesta.campos.all()
        preguntas = []
        for campo in campos:
            preguntas.append({
                "pregunta_id" : campo.id,
                "is_active" : campo.is_active
            })
        context['preguntas'] = preguntas
        context['encuesta'] = encuesta
        return context

class GuardarRespuestaView(LoginRequiredMixin, View):
    """ Vista para guardar las respuestas del usuario. """
    login_url = 'login'
    def post(self, request, *args, **kwargs):
        post_data = json.loads(request.body.decode("utf-8"))

        encuesta = Encuesta.objects.get(pk=post_data['pk_encuesta'])
        pregunta = CampoEncuesta.objects.get(pk=post_data['pk_pregunta'])
        respuesta_pregunta = post_data['respuesta']

        if pregunta.is_active == True:
            if RespuestaCampo.objects.filter(user=request.user, encuesta=encuesta, pregunta=pregunta).exists():
                print("El usuario ya respondio a esta pregunta.")
                respuesta = RespuestaCampo.objects.get(user=request.user, encuesta=encuesta, pregunta=pregunta)
                print(respuesta)
                respuesta.respuesta = respuesta_pregunta
                respuesta.save()
            else:
                print("El usuario no a respondido a esta pregunta.")
                RespuestaCampo.objects.create(
                    user=self.request.user,
                    encuesta=encuesta,
                    pregunta=pregunta,
                    respuesta=respuesta_pregunta
                )
            respuesta = True
        
        else:
            respuesta = False

        return JsonResponse({'respuesta':respuesta})

class GraficaTemplateView(LoginRequiredMixin, TemplateView):
    """ Vista para graficar los resultados de las encuestas gráficamente sii son preguntas tipo lista. """
    login_url = 'login'
    template_name = "encuestas/resultados_encuesta.html"

    def get_context_data(self, **kwargs):
        context = super(GraficaTemplateView, self).get_context_data(**kwargs)
        encuesta = Encuesta.objects.get(pk=self.kwargs['pk_encuesta'])
        preguntas = encuesta.campos.all()

        resultados = []
        numero_votantes = []
        for pregunta in preguntas:
            numero_votantes.append(pregunta.respuestas.all().count())

        numero_votantes = max(numero_votantes)
        for pregunta in preguntas:
            if pregunta.tipo == CampoEncuesta.TIPO_TEXTO or pregunta.tipo == CampoEncuesta.TIPO_TEXTO_AREA:
                continue
            
            if pregunta.tipo == CampoEncuesta.TIPO_LISTA:
                respuestas = pregunta.respuestas.all()

                respuestas_aux = []

                for respuesta in respuestas:
                    respuestas_aux.append(respuesta.respuesta) 

                items = ast.literal_eval(pregunta.values_select)

                contador_respuestas = []
                colores = []

                for item in items:
                    contador_respuestas.append(respuestas_aux.count(item))
                    color = np.random.choice(range(256), size=3)
                    colores.append('rgb({}, {}, {})'.format(color[0], color[1], color[2]))

                for i in range(len(contador_respuestas)):
                    porcentaje = round((contador_respuestas[i]/numero_votantes)*100, 2)
                    items[i] = items[i] + " " +str(porcentaje) + "%"

                items.append('Ausencia/No responde')

                votantes_ausentes = numero_votantes-sum(contador_respuestas)
                contador_respuestas.append(votantes_ausentes)
                color = np.random.choice(range(256), size=3)
                colores.append('rgb({}, {}, {})'.format(color[0], color[1], color[2]))
                porcentaje = round((votantes_ausentes/numero_votantes)*100, 2)
                items[items.index('Ausencia/No responde')] = items[items.index('Ausencia/No responde')] + " " + str(porcentaje) + "%"

                resultados.append({
                    'pregunta' : pregunta.nombre_campo,
                    'labels' : items,
                    'contador_respuestas' : contador_respuestas,
                    'colores' : colores,
                })
        
        context['resultados'] = resultados
        context['encuesta'] = encuesta
        return context