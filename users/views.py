""" Vistas de la app de usuarios. """

# Django
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

# Modelos
from .models import User, UserLogs

# Utilidades
import requests
import json

class InitView(TemplateView):
    """ Vista inicial. """
    template_name = "index.html"

class SignUpView(CreateView):
    """ Vista para crear usuario."""
    model = User
    template_name = 'signup.html'
    fields = '__all__'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """ Función que se ejecuta cuando el formulario es válido. """

        password1 = self.request.POST.get('password')
        password2 = self.request.POST.get('password2')
        if password1 and password2 and password1 != password2:
            form.add_error('password', 'Las contraseñas no coinciden.')
            datos = form.cleaned_data
            print(datos)
            return self.form_invalid(form)
        
        correo = self.request.POST.get('correo')
        numeroId = self.request.POST.get('numeroId')
        nombre1 = self.request.POST.get('nombre1')
        apellido1 = self.request.POST.get('apellido1')
        celular = self.request.POST.get('celular')
        datos = form.cleaned_data
        nombre2 = self.request.POST.get('nombre2')
        apellido2 = self.request.POST.get('apellido2')
        fechaNac = self.request.POST.get('fechaNac')

        print(nombre2)
        print(apellido2)
        print(fechaNac)

        print(datos)

        user = User.objects.create_user(numeroId=numeroId, nombre1=nombre1, apellido1=apellido1, correo=correo, password=password1, celular=celular)
        
        if nombre2 and nombre2 != '':
            user.nombre2 = nombre2
        
        if apellido2 and apellido2 != '':
            user.apellido2 = apellido2
        
        if fechaNac and fechaNac != '':
            user.fechaNac = fechaNac
        
        user.save()

        return redirect("index")

    def form_invalid(self, form):
        datos = form.cleaned_data
        print(form.errors)
        return super(SignUpView, self).form_invalid(form)

class LoginView(View):
    """ Vista de inicio de sesión. """

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'login.html', context)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('lista_encuestas')
        else:
            messages.add_message(request, messages.ERROR, 'Correo electrónico o contraseña no válidos.')
            return redirect('login')

class LogoutView(LoginRequiredMixin ,View):
    """ Vista para salir de sesión. """
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


class UpdateUserView(LoginRequiredMixin, UpdateView):
    """ Vista para actualizar los datos del usuario. """
    login_url = 'login'
    template_name = 'update_user.html'
    model =  User
    fields = ['nombre1', 'nombre2', 'apellido1', 'apellido2', 'fechaNac', 'genero', 'correo', 'direccion', 'telefono', 'celular']
    success_url = reverse_lazy('lista_encuestas')

    def get_object(self, *args, **kwargs):
        obj = super(UpdateUserView, self).get_object(*args, **kwargs)
        if obj.id != self.request.user.id:
            raise Http404("No tiene permisos para cambiar este usuario.")
        return obj

    def get_context_data(self, **kwargs):
        context = super(UpdateUserView, self).get_context_data(**kwargs)
        user = self.request.user
        context['fechaNac'] = user.fechaNac.strftime('%Y-%m-%d')
        return context

    def form_valid(self, form):        

        user =self.request.user
        data = form.cleaned_data

        cambios = form.changed_data
        userlogs = UserLogs()

        metadata={}
        for cambio in cambios:
            if cambio == 'nombre1':
                metadata['nombre1_ant'] = user.nombre1
                metadata['nombre1_nue'] = data[cambio]
                userlogs.nombre1 = True
                
            if cambio == 'nombre2':
                metadata['nombre2_ant'] = user.nombre2
                metadata['nombre2_nue'] = data[cambio]
                userlogs.nombre2 = True

            if cambio == 'apellido1':
                metadata['apellido1_ant'] = user.apellido1
                metadata['apellido1_nue'] = data[cambio]
                userlogs.apellido1 = True

            if cambio == 'apellido2':
                metadata['apellido2_ant'] = user.apellido2
                metadata['apellido2_nue'] = data[cambio]
                userlogs.apellido2 = True

            if cambio == 'fechaNac':
                metadata['fechaNac_ant'] = user.fechaNac
                metadata['fechaNac_nue'] = data[cambio]
                userlogs.fechaNac = True

            if cambio == 'genero':
                metadata['genero_ant'] = user.genero
                metadata['genero_nue'] = data[cambio]
                userlogs.genero = True

            if cambio == 'correo':
                metadata['correo_ant'] = user.nombre1
                metadata['correo_nue'] = data[cambio]
                userlogs.correo = True

            if cambio == 'direccion':
                metadata['direccion_ant'] = user.direccion
                metadata['direccion_nue'] = data[cambio]
                userlogs.direccion = True

            if cambio == 'telefono':
                metadata['telefono_ant'] = user.telefono
                metadata['telefono_nue'] = data[cambio]
                userlogs.telefono = True

            if cambio == 'celular':
                metadata['celular_ant'] = user.celular
                metadata['celular_nue'] = data[cambio]
                userlogs.celular = True

        userlogs.metadata = metadata
        userlogs.user = user
        userlogs.save()

        return super().form_valid(form)
        
class ForgotPasswordView(View):
    """ Vista para enviar correo electrónico para el cambio de contraseña. """
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'forgot_pass.html', context)

    def post(self, request, *args, **kwargs):
        correo = self.request.POST.get('correo')
        if User.objects.filter(correo=correo).exists():
            user = User.objects.get(correo__exact=correo)
            
            current_site = get_current_site(request)
            mail_subject = 'Resetear contraseña'
            body = render_to_string('reset_password.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = correo
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            send_email.send()

            messages.success(request, 'Un email fue enviado a tu bandeja del correo eletrónico para cambiar tu contraseña.')
            return redirect('login')

        else:
            messages.error(request, 'La cuenta de usuario ingresada no existe.')
            return redirect('forgot_password')

class ResetPasswordValidateView(View):
    """ Vista que valida el enlace que se envió al correo electrónico para cambio de contraseña. """
    def get(self, request, *args, **kwargs):
        token = self.kwargs['token']
        uidb64 = self.kwargs['uidb64']
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            request.session['uid'] = uid
            print(request.session.get('uid'))
            messages.success(request, 'Por favor cambia tu contraseña.')
            return redirect('reset_password')
        
        else: 
            messages.error(request, 'El enlace ha expirado.')
            return redirect('login')
        
class ResetPasswordView(View):
    """ Visa para cambiar la contraseña de usuario. """
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'resetpassword.html', context)

    def post(self, request, *args, **kwargs):

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password1)
            user.save()
            messages.success(request, 'La contraseña ha sido moficada correctamente.')
            return redirect('login')

        else: 
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('reset_password')