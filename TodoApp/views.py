from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import Tarea

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


# Create your views here.

class IniciarSesion(LoginView):
    template_name = "TodoApp/login.html"
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy("tareas")
    

class PaginaRegistro(FormView):
    template_name = "TodoApp/registro.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("tareas")

    def form_valid(self, form):
        usuario = form.save()
        if usuario is not None:
            login(self.request, usuario)
        return super(PaginaRegistro, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect("tareas")
        return super(PaginaRegistro, self).get(*args, **kwargs)


class ListaTareas(LoginRequiredMixin, ListView):
    model = Tarea
    context_object_name = "tareas"
    template_name = 'TodoApp/lista_tareas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tareas'] = context['tareas'].filter(usuario=self.request.user)
        context['count'] = context['tareas'].filter(completado=False).count()

        buscador = self.request.GET.get('buscador')
        if buscador:
            context['tareas'] = context['tareas'].filter(
                titulo__istartswith=buscador)
            
        context['buscador'] = buscador
        return context
    

class DetallesTarea(LoginRequiredMixin, DetailView):
    model = Tarea
    context_object_name = "tarea"
    template_name = 'TodoApp/tarea.html'


class CrearTarea(LoginRequiredMixin, CreateView):
    model = Tarea
    fields = ["titulo", "descripcion", "completado"]
    success_url = reverse_lazy("tareas")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(CrearTarea, self).form_valid(form)


class EditarTarea(LoginRequiredMixin, UpdateView):
    model = Tarea
    fields = ["titulo", "descripcion", "completado"]
    success_url = reverse_lazy("tareas")


class EliminarTarea(LoginRequiredMixin, DeleteView):
    model = Tarea
    context_object_name = "tareas"
    template_name = 'TodoApp/elimnar_tarea.html'
    success_url = reverse_lazy("tareas")
