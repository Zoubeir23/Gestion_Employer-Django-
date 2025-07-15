from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, ProtectedError
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
import csv
import json
from datetime import datetime, timedelta
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

    def get_queryset(self):
        return Service.objects.annotate(
            nombre_employes=Count('employer')
        ).order_by('nom')

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
    template_name = 'gestion/service/form.html'
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
    template_name = 'gestion/service/form.html'
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
        queryset = super().get_queryset().select_related('service')
        
        # Recherche textuelle
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(nom__icontains=search_query) |
                Q(prenom__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(poste__icontains=search_query) |
                Q(service__nom__icontains=search_query)
            )
        
        # Filtre par service
        service_filter = self.request.GET.get('service')
        if service_filter:
            queryset = queryset.filter(service_id=service_filter)
        
        # Filtre par poste
        poste_filter = self.request.GET.get('poste')
        if poste_filter:
            queryset = queryset.filter(poste__icontains=poste_filter)
        
        # Filtre par date d'embauche
        date_debut = self.request.GET.get('date_debut')
        date_fin = self.request.GET.get('date_fin')
        if date_debut:
            queryset = queryset.filter(date_embauche__gte=date_debut)
        if date_fin:
            queryset = queryset.filter(date_embauche__lte=date_fin)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['postes_uniques'] = Employer.objects.values_list('poste', flat=True).distinct()
        
        # Conserver les paramètres de recherche
        context['current_search'] = self.request.GET.get('search', '')
        context['current_service'] = self.request.GET.get('service', '')
        context['current_poste'] = self.request.GET.get('poste', '')
        context['current_date_debut'] = self.request.GET.get('date_debut', '')
        context['current_date_fin'] = self.request.GET.get('date_fin', '')
        
        return context

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
    template_name = 'gestion/employer/form.html'
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
    template_name = 'gestion/employer/form.html'
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
    template_name = 'gestion/conge/form.html'
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
    template_name = 'gestion/conge/form.html'
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

# Vues pour l'approbation des congés
@login_required
def approuver_conge(request, pk):
    conge = get_object_or_404(Conge, pk=pk)
    conge.statut = 'APPROUVE'
    conge.save()
    messages.success(request, 'Congé approuvé avec succès !')
    return redirect('conge-detail', pk=pk)

@login_required
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
        return Employer.objects.select_related('service').order_by('-id')[:5]

    def get_context_data(self, **kwargs):
        from django.db.models import Count
        from datetime import datetime, timedelta
        
        context = super().get_context_data(**kwargs)
        
        # Statistiques de base
        context['total_employers'] = Employer.objects.count()
        context['total_services'] = Service.objects.count()
        context['total_conges'] = Conge.objects.count()
        context['conges_en_attente'] = Conge.objects.filter(statut='EN_ATTENTE').count()
        context['conges_approuves'] = Conge.objects.filter(statut='APPROUVE').count()
        context['conges_rejetes'] = Conge.objects.filter(statut='REJETE').count()
        
        # Données pour graphiques (sérialisées en JSON)
        import json
        
        # Employés par service
        services_data = Service.objects.annotate(
            nb_employes=Count('employer')
        ).values('nom', 'nb_employes')
        context['services_chart_data'] = json.dumps(list(services_data))
        
        # Congés par statut
        conges_stats = {
            'en_attente': context['conges_en_attente'],
            'approuves': context['conges_approuves'],
            'rejetes': context['conges_rejetes']
        }
        context['conges_chart_data'] = json.dumps(conges_stats)
        
        # Évolution des embauches (6 derniers mois)
        today = datetime.now().date()
        embauches_data = []
        for i in range(6):
            month_start = today.replace(day=1) - timedelta(days=i*30)
            month_end = month_start.replace(day=28) + timedelta(days=4)
            month_end = month_end - timedelta(days=month_end.day)
            
            count = Employer.objects.filter(
                date_embauche__gte=month_start,
                date_embauche__lte=month_end
            ).count()
            
            embauches_data.append({
                'mois': month_start.strftime('%B %Y'),
                'count': count
            })
        
        context['embauches_chart_data'] = json.dumps(list(reversed(embauches_data)))
        
        # Alertes et notifications
        context['alertes'] = []
        
        # Congés en attente depuis plus de 7 jours
        conges_anciens = Conge.objects.filter(
            statut='EN_ATTENTE',
            date_demande__lt=datetime.now().date() - timedelta(days=7)
        ).count()
        
        if conges_anciens > 0:
            context['alertes'].append({
                'type': 'warning',
                'message': f'{conges_anciens} congé(s) en attente depuis plus de 7 jours',
                'icon': 'fas fa-clock'
            })
        
        # Anniversaires d'embauche ce mois
        current_month = today.month
        anniversaires = Employer.objects.filter(
            date_embauche__month=current_month
        ).count()
        
        if anniversaires > 0:
            context['alertes'].append({
                'type': 'info',
                'message': f'{anniversaires} anniversaire(s) d\'embauche ce mois',
                'icon': 'fas fa-birthday-cake'
            })
        
        return context

class CongeApprobationView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Conge
    form_class = CongeApprobationForm
    template_name = 'gestion/conge/approbation/form.html'
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

# Vues d'export et rapports
@login_required
def export_employers_csv(request):
    """Export des employés en CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employes.csv"'
    response.write('\ufeff')  # BOM pour Excel
    
    writer = csv.writer(response)
    writer.writerow(['Nom', 'Prénom', 'Email', 'Poste', 'Service', 'Date d\'embauche', 'Téléphone'])
    
    employers = Employer.objects.select_related('service').all()
    for employer in employers:
        writer.writerow([
            employer.nom,
            employer.prenom,
            employer.email,
            employer.poste,
            employer.service.nom if employer.service else '',
            employer.date_embauche.strftime('%d/%m/%Y') if employer.date_embauche else '',
            employer.telephone or ''
        ])
    
    return response

@login_required
def export_conges_csv(request):
    """Export des congés en CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="conges.csv"'
    response.write('\ufeff')  # BOM pour Excel
    
    writer = csv.writer(response)
    writer.writerow(['Employé', 'Type', 'Date début', 'Date fin', 'Statut', 'Date demande', 'Raison'])
    
    conges = Conge.objects.select_related('employer').all()
    for conge in conges:
        writer.writerow([
            f"{conge.employer.prenom} {conge.employer.nom}",
            conge.get_type_conge_display(),
            conge.date_debut.strftime('%d/%m/%Y'),
            conge.date_fin.strftime('%d/%m/%Y'),
            conge.get_statut_display(),
            conge.date_demande.strftime('%d/%m/%Y') if conge.date_demande else '',
            conge.raison or ''
        ])
    
    return response

@login_required
def rapport_mensuel_conges(request):
    """Rapport mensuel des congés"""
    from django.db.models import Count
    from datetime import datetime, timedelta
    
    # Récupérer le mois et l'année depuis les paramètres GET
    today = datetime.now()
    mois = int(request.GET.get('mois', today.month))
    annee = int(request.GET.get('annee', today.year))
    
    # Calculer les dates de début et fin du mois
    debut_mois = datetime(annee, mois, 1).date()
    if mois == 12:
        fin_mois = datetime(annee + 1, 1, 1).date() - timedelta(days=1)
    else:
        fin_mois = datetime(annee, mois + 1, 1).date() - timedelta(days=1)
    
    # Statistiques des congés pour le mois
    conges_mois = Conge.objects.filter(
        date_debut__gte=debut_mois,
        date_debut__lte=fin_mois
    )
    
    stats = {
        'total': conges_mois.count(),
        'approuves': conges_mois.filter(statut='APPROUVE').count(),
        'en_attente': conges_mois.filter(statut='EN_ATTENTE').count(),
        'rejetes': conges_mois.filter(statut='REJETE').count(),
    }
    
    # Congés par service
    conges_par_service = conges_mois.values('employer__service__nom').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Congés par type
    conges_par_type = conges_mois.values('type_conge').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'mois': mois,
        'annee': annee,
        'mois_nom': debut_mois.strftime('%B %Y'),
        'stats': stats,
        'conges_par_service': conges_par_service,
        'conges_par_type': conges_par_type,
        'conges_detail': conges_mois.select_related('employer', 'employer__service')
    }
    
    return render(request, 'gestion/rapports/conges_mensuel.html', context)

@login_required
def api_dashboard_data(request):
    """API pour les données du dashboard (pour actualisation en temps réel)"""
    data = {
        'total_employers': Employer.objects.count(),
        'total_services': Service.objects.count(),
        'total_conges': Conge.objects.count(),
        'conges_en_attente': Conge.objects.filter(statut='EN_ATTENTE').count(),
        'conges_approuves': Conge.objects.filter(statut='APPROUVE').count(),
        'conges_rejetes': Conge.objects.filter(statut='REJETE').count(),
    }
    return JsonResponse(data)

@login_required
def recherche_globale(request):
    """Recherche globale dans toute l'application"""
    query = request.GET.get('q', '').strip()
    results = {
        'employers': [],
        'services': [],
        'conges': []
    }
    
    if query and len(query) >= 2:
        # Recherche dans les employés
        employers = Employer.objects.filter(
            Q(nom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(email__icontains=query) |
            Q(poste__icontains=query)
        ).select_related('service')[:10]
        
        results['employers'] = [{
            'id': emp.id,
            'nom': f"{emp.prenom} {emp.nom}",
            'poste': emp.poste,
            'service': emp.service.nom if emp.service else '',
            'url': reverse('employer-detail', args=[emp.id])
        } for emp in employers]
        
        # Recherche dans les services
        services = Service.objects.filter(
            Q(nom__icontains=query) |
            Q(description__icontains=query)
        )[:10]
        
        results['services'] = [{
            'id': service.id,
            'nom': service.nom,
            'description': service.description or '',
            'url': reverse('service-detail', args=[service.id])
        } for service in services]
        
        # Recherche dans les congés
        conges = Conge.objects.filter(
            Q(employer__nom__icontains=query) |
            Q(employer__prenom__icontains=query) |
            Q(raison__icontains=query)
        ).select_related('employer')[:10]
        
        results['conges'] = [{
            'id': conge.id,
            'employer': f"{conge.employer.prenom} {conge.employer.nom}",
            'type': conge.get_type_conge_display(),
            'date_debut': conge.date_debut.strftime('%d/%m/%Y'),
            'statut': conge.get_statut_display(),
            'url': reverse('conge-detail', args=[conge.id])
        } for conge in conges]
    
    return JsonResponse(results)
