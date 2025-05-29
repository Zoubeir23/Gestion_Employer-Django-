from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Employer, Service, Conge

# Create your views here.

# Vues pour les Services
class ServiceListView(ListView):
    model = Service
    template_name = 'gestion/service_list.html'
    context_object_name = 'services'

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'gestion/service_detail.html'
    context_object_name = 'service'

class ServiceCreateView(CreateView):
    model = Service
    template_name = 'gestion/service_form.html'
    fields = ['nom']
    success_url = reverse_lazy('service_list')

    def form_valid(self, form):
        messages.success(self.request, 'Service créé avec succès.')
        return super().form_valid(form)

class ServiceUpdateView(UpdateView):
    model = Service
    template_name = 'gestion/service_form.html'
    fields = ['nom']
    success_url = reverse_lazy('service_list')

    def form_valid(self, form):
        messages.success(self.request, 'Service mis à jour avec succès.')
        return super().form_valid(form)

class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'gestion/service_confirm_delete.html'
    success_url = reverse_lazy('service_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Service supprimé avec succès.')
        return super().delete(request, *args, **kwargs)

# Vues pour les Employés
class EmployerListView(ListView):
    model = Employer
    template_name = 'gestion/employer_list.html'
    context_object_name = 'employers'

class EmployerDetailView(DetailView):
    model = Employer
    template_name = 'gestion/employer_detail.html'
    context_object_name = 'employer'

class EmployerCreateView(CreateView):
    model = Employer
    template_name = 'gestion/employer_form.html'
    fields = ['nom', 'service', 'date_embauche']
    success_url = reverse_lazy('employer_list')

    def form_valid(self, form):
        messages.success(self.request, 'Employé créé avec succès.')
        return super().form_valid(form)

class EmployerUpdateView(UpdateView):
    model = Employer
    template_name = 'gestion/employer_form.html'
    fields = ['nom', 'service', 'date_embauche']
    success_url = reverse_lazy('employer_list')

    def form_valid(self, form):
        messages.success(self.request, 'Employé mis à jour avec succès.')
        return super().form_valid(form)

class EmployerDeleteView(DeleteView):
    model = Employer
    template_name = 'gestion/employer_confirm_delete.html'
    success_url = reverse_lazy('employer_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Employé supprimé avec succès.')
        return super().delete(request, *args, **kwargs)

# Vues pour les Congés
class CongeListView(ListView):
    model = Conge
    template_name = 'gestion/conge_list.html'
    context_object_name = 'conges'

class CongeDetailView(DetailView):
    model = Conge
    template_name = 'gestion/conge_detail.html'
    context_object_name = 'conge'

class CongeCreateView(CreateView):
    model = Conge
    template_name = 'gestion/conge_form.html'
    fields = ['employer', 'date_debut', 'date_fin', 'raison']
    success_url = reverse_lazy('conge_list')

    def form_valid(self, form):
        messages.success(self.request, 'Congé créé avec succès.')
        return super().form_valid(form)

class CongeUpdateView(UpdateView):
    model = Conge
    template_name = 'gestion/conge_form.html'
    fields = ['employer', 'date_debut', 'date_fin', 'raison']
    success_url = reverse_lazy('conge_list')

    def form_valid(self, form):
        messages.success(self.request, 'Congé mis à jour avec succès.')
        return super().form_valid(form)

class CongeDeleteView(DeleteView):
    model = Conge
    template_name = 'gestion/conge_confirm_delete.html'
    success_url = reverse_lazy('conge_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Congé supprimé avec succès.')
        return super().delete(request, *args, **kwargs)

# Vue pour la page d'accueil
def home(request):
    return render(request, 'gestion/home.html', {
        'total_employers': Employer.objects.count(),
        'total_services': Service.objects.count(),
        'total_conges': Conge.objects.count(),
    })
