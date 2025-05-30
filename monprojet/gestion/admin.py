from django.contrib import admin
from .models import Employer, Service, Conge

# Register your models here.
@admin.register(Conge)
class CongeAdmin(admin.ModelAdmin):
    list_display = ('employer', 'type_conge', 'date_debut', 'date_fin', 'statut', 'date_demande')
    list_filter = ('statut', 'type_conge', 'date_debut')
    search_fields = ('employer__nom', 'employer__prenom', 'raison')
    date_hierarchy = 'date_debut'
    ordering = ('-date_demande',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(statut='EN_ATTENTE')

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'service', 'poste')
    list_filter = ('service', 'poste')
    search_fields = ('nom', 'prenom', 'email')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')
    search_fields = ('nom', 'description')
