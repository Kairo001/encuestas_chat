""" Urls de la app de encuestas. """

# Django
from django.urls import path

# Vistas
from encuestas import views

urlpatterns = [
    path('encuesta_nueva/', views.EncuestaCreateView.as_view(), name='crear_encuesta'),
    path('encuesta/<pk_encuesta>/campos', views.CampoEncuestaCreateView.as_view(), name='campo_encuesta'),
    path('encuesta/<pk_encuesta>/campo/<pk>/', views.CampoEncuestaDeleteView.as_view(), name="encuesta_campo_delete"),
    path('encuesta/<pk_encuesta>/vista_previa', views.VistaPreviaFormView.as_view(), name="vista_previa" ),
    path('lista_encuestas/', views.ListaEncuestasListView.as_view(), name="lista_encuestas"),
    path('lista_encuestas/pre_terminar/', views.TerminarEncuestaView.as_view(), name='pre_terminar_encuesta'),
    path('lista_encuestas/terminar_encuesta/', views.EncuestaUpdateView.as_view(), name="terminar_encuesta"),
    path('lista_encuestas/activar_encuesta/', views.ActivarEncuestaView.as_view() , name="acitivar_encuesta"),
    path('eliminar_encuesta/<pk_encuesta>', views.EncuestaDeleteView.as_view(), name="eliminar_encuesta"),
    path('ver_encuesta/<pk_encuesta>', views.EncuestaVistaFormView.as_view(), name='ver_encuesta'),
    path('listaencuestas/', views.ListaEncuestasRealizarListView.as_view(), name="lista_encuestas_realizar"),
    path('realizar_encuesta/<pk_encuesta>/', views.RealizarEncuestaFormView.as_view(), name="realizar_encuesta"),
    path('resultados_encuesta/<pk_encuesta>/', views.GraficaTemplateView.as_view(), name='resultados_encuesta'),
    path('encuesta_agente/<pk_encuesta>/', views.EncuestaAgenteTemplateView.as_view(), name="encuesta_agente"),
]