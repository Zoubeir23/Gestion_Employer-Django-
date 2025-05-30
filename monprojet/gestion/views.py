from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q, ProtectedError
from django.utils import timezone
from .models import Employer, Service, Conge
from .forms import EmployerForm, ServiceForm, CongeForm, CongeApprobationForm

# Create your views here.

# Vues pour les Services
class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'gestion/service/list.html'
    context_object_name = 'services'
    paginate_by = 10
    ordering = ['nom']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.annotate(
            nombre_employes=Count('employer')
        )
        return context

class ServiceDetailView(LoginRequiredMixin, DetailView):
    model = Service
    template_name = 'gestion/service/detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employers'] = self.object.employer_set.all()
        return context

class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'gestion/service/ajout/create.html'
    success_url = reverse_lazy('service-list')

    def form_valid(self, form):
        messages.success(self.request, 'Service créé avec succès !')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erreur lors de la création du service. Veuillez vérifier les informations.')
        return super().form_invalid(form)

class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'gestion/service/modification/update.html'
    success_url = reverse_lazy('service-list')

    def form_valid(self, form):
        messages.success(self.request, 'Service modifié avec succès !')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erreur lors de la modification du service. Veuillez vérifier les informations.')
        return super().form_invalid(form)

class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'gestion/service/suppression/confirm_delete.html'
    success_url = reverse_lazy('service-list')

    def delete(self, request, *args, **kwargs):
        try:
            messages.success(request, 'Service supprimé avec succès !')
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, 'Impossible de supprimer ce service car il est associé à des employés.')
            return redirect('service-list')

# Vues pour les Employés
class EmployerListView(LoginRequiredMixin, ListView):
    model = Employer
    template_name = 'gestion/employer/list.html'
    context_object_name = 'employers'
    paginate_by = 10
    ordering = ['nom', 'prenom']

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
    template_name = 'gestion/employer/detail.html'
    context_object_name = 'employer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conges = self.object.conge_set.all()
        context['conges'] = conges
        context['approved_count'] = conges.filter(statut='APPROUVE').count()
        context['pending_count'] = conges.filter(statut='EN_ATTENTE').count()
        return context

class EmployerCreateView(LoginRequiredMixin, CreateView):
    model = Employer
    form_class = EmployerForm
    template_name = 'gestion/employer/ajout/create.html'
    success_url = reverse_lazy('employer-list')

    def form_valid(self, form):
        messages.success(self.request, 'Employé créé avec succès !')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erreur lors de la création de l\'employé. Veuillez vérifier les informations.')
        return super().form_invalid(form)

class EmployerUpdateView(LoginRequiredMixin, UpdateView):
    model = Employer
    form_class = EmployerForm
    template_name = 'gestion/employer/modification/update.html'
    success_url = reverse_lazy('employer-list')

    def form_valid(self, form):
        messages.success(self.request, 'Employé modifié avec succès !')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erreur lors de la modification de l\'employé. Veuillez vérifier les informations.')
        return super().form_invalid(form)

class EmployerDeleteView(LoginRequiredMixin, DeleteView):
    model = Employer
    template_name = 'gestion/employer/suppression/confirm_delete.html'
    success_url = reverse_lazy('employer-list')

    def delete(self, request, *args, **kwargs):
        try:
            messages.success(request, 'Employé supprimé avec succès !')
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, 'Impossible de supprimer cet employé car il est associé à des congés.')
            return redirect('employer-list')

# Vues pour les Congés
class CongeListView(LoginRequiredMixin, ListView):
    model = Conge
    template_name = 'gestion/conge/list.html'
    context_object_name = 'conges'
    paginate_by = 10
    ordering = ['-date_debut']

    def get_queryset(self):
        queryset = super().get_queryset()
        statut = self.request.GET.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
        return queryset

class CongeDetailView(LoginRequiredMixin, DetailView):
    model = Conge
    template_name = 'gestion/conge/detail.html'
    context_object_name = 'conge'

class CongeCreateView(LoginRequiredMixin, CreateView):
    model = Conge
    form_class = CongeForm
    template_name = 'gestion/conge/ajout/create.html'
    success_url = reverse_lazy('conge-list')

    def form_valid(self, form):
        messages.success(self.request, 'Congé créé avec succès !')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erreur lors de la création du congé. Veuillez vérifier les informations.')
        return super().form_invalid(form)

class CongeUpdateView(LoginRequiredMixin, UpdateView):
    model = Conge
    form_class = CongeForm
    template_name = 'gestion/conge/modification/update.html'
    success_url = reverse_lazy('conge-list')

    def form_valid(self, form):
        messages.success(self.request, 'Congé modifié avec succès !')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erreur lors de la modification du congé. Veuillez vérifier les informations.')
        return super().form_invalid(form)

class CongeDeleteView(LoginRequiredMixin, DeleteView):
    model = Conge
    template_name = 'gestion/conge/suppression/confirm_delete.html'
    success_url = reverse_lazy('conge-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Congé supprimé avec succès !')
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
    context_object_name = 'derniers_employers'

    def get_queryset(self):
        return Employer.objects.order_by('-id')[:5]  # Affiche les 5 derniers employés ajoutés

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_employers'] = Employer.objects.count()
        context['total_services'] = Service.objects.count()
        context['total_conges'] = Conge.objects.count()
        context['conges_en_attente'] = Conge.objects.filter(statut='EN_ATTENTE').count()
        return context

class CongeApprobationView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Conge
    form_class = CongeApprobationForm
    template_name = 'gestion/conge/approbation/approbation.html'
    success_url = reverse_lazy('conge-list')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'avez pas les permissions nécessaires pour approuver ou rejeter les congés.")
        return redirect('conge-list')

    def form_valid(self, form):
        conge = form.save(commit=False)
        conge.save()
        messages.success(self.request, f'Le congé a été {conge.get_statut_display().lower()}.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erreur lors de l\'approbation du congé. Veuillez vérifier les informations.')
        return super().form_invalid(form)
