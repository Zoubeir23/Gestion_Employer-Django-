from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.utils import timezone
from .models import Employer, Service, Conge
from .forms import EmployerForm, ServiceForm, CongeForm

# Create your views here.

# Vues pour les Services
class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'gestion/service_list.html'
    context_object_name = 'services'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.annotate(
            nombre_employes=Count('employer')
        )
        return context

class ServiceDetailView(LoginRequiredMixin, DetailView):
    model = Service
    template_name = 'gestion/service_detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employers'] = self.object.employer_set.all()
        return context

class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'gestion/service_form.html'
    success_url = reverse_lazy('service-list')

    def form_valid(self, form):
        messages.success(self.request, 'Service créé avec succès !')
        return super().form_valid(form)

class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'gestion/service_form.html'
    success_url = reverse_lazy('service-list')

    def form_valid(self, form):
        messages.success(self.request, 'Service mis à jour avec succès !')
        return super().form_valid(form)

class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'gestion/service_confirm_delete.html'
    success_url = reverse_lazy('service-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Service supprimé avec succès !')
        return super().delete(request, *args, **kwargs)

# Vues pour les Employés
class EmployerListView(LoginRequiredMixin, ListView):
    model = Employer
    template_name = 'gestion/employer_list.html'
    context_object_name = 'employers'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(nom__icontains=search_query) |
                Q(prenom__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        return queryset

class EmployerDetailView(LoginRequiredMixin, DetailView):
    model = Employer
    template_name = 'gestion/employer_detail.html'
    context_object_name = 'employer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conges'] = self.object.conge_set.all()
        return context

class EmployerCreateView(LoginRequiredMixin, CreateView):
    model = Employer
    form_class = EmployerForm
    template_name = 'gestion/employer_form.html'
    success_url = reverse_lazy('employer-list')

    def form_valid(self, form):
        messages.success(self.request, 'Employé créé avec succès !')
        return super().form_valid(form)

class EmployerUpdateView(LoginRequiredMixin, UpdateView):
    model = Employer
    form_class = EmployerForm
    template_name = 'gestion/employer_form.html'
    success_url = reverse_lazy('employer-list')

    def form_valid(self, form):
        messages.success(self.request, 'Employé mis à jour avec succès !')
        return super().form_valid(form)

class EmployerDeleteView(LoginRequiredMixin, DeleteView):
    model = Employer
    template_name = 'gestion/employer_confirm_delete.html'
    success_url = reverse_lazy('employer-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Employé supprimé avec succès !')
        return super().delete(request, *args, **kwargs)

# Vues pour les Congés
class CongeListView(LoginRequiredMixin, ListView):
    model = Conge
    template_name = 'gestion/conge_list.html'
    context_object_name = 'conges'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        statut = self.request.GET.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
        return queryset

class CongeDetailView(LoginRequiredMixin, DetailView):
    model = Conge
    template_name = 'gestion/conge_detail.html'
    context_object_name = 'conge'

class CongeCreateView(LoginRequiredMixin, CreateView):
    model = Conge
    form_class = CongeForm
    template_name = 'gestion/conge_form.html'
    success_url = reverse_lazy('conge-list')

    def form_valid(self, form):
        form.instance.employer = self.request.user.employer
        form.instance.statut = 'EN_ATTENTE'
        messages.success(self.request, 'Demande de congé créée avec succès !')
        return super().form_valid(form)

class CongeUpdateView(LoginRequiredMixin, UpdateView):
    model = Conge
    form_class = CongeForm
    template_name = 'gestion/conge_form.html'
    success_url = reverse_lazy('conge-list')

    def form_valid(self, form):
        messages.success(self.request, 'Demande de congé mise à jour avec succès !')
        return super().form_valid(form)

class CongeDeleteView(LoginRequiredMixin, DeleteView):
    model = Conge
    template_name = 'gestion/conge_confirm_delete.html'
    success_url = reverse_lazy('conge-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Demande de congé supprimée avec succès !')
        return super().delete(request, *args, **kwargs)

# Vue pour la page d'accueil
def approuver_conge(request, pk):
    conge = get_object_or_404(Conge, pk=pk)
    conge.statut = 'APPROUVE'
    conge.save()
    messages.success(request, 'Congé approuvé avec succès !')
    return redirect('conge-detail', pk=pk)

def rejeter_conge(request, pk):
    conge = get_object_or_404(Conge, pk=pk)
    conge.statut = 'REJETE'
    conge.save()
    messages.success(request, 'Congé rejeté avec succès !')
    return redirect('conge-detail', pk=pk)

class HomeView(LoginRequiredMixin, ListView):
    template_name = 'gestion/home.html'
    context_object_name = 'employers'

    def get_queryset(self):
        return Employer.objects.all()[:5]  # Affiche les 5 derniers employés

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_employers'] = Employer.objects.count()
        context['total_services'] = Service.objects.count()
        context['total_conges'] = Conge.objects.count()
        context['conges_en_attente'] = Conge.objects.filter(statut='EN_ATTENTE').count()
        return context
