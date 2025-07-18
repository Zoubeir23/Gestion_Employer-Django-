from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    
    # URLs pour les employés
    path('employes/', views.EmployerListView.as_view(), name='employer-list'),
    path('employes/<int:pk>/', views.EmployerDetailView.as_view(), name='employer-detail'),
    path('employes/nouveau/', views.EmployerCreateView.as_view(), name='employer-create'),
    path('employes/<int:pk>/modifier/', views.EmployerUpdateView.as_view(), name='employer-update'),
    path('employes/<int:pk>/supprimer/', views.EmployerDeleteView.as_view(), name='employer-delete'),
    
    # URLs pour les services
    path('services/', views.ServiceListView.as_view(), name='service-list'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service-detail'),
    path('services/nouveau/', views.ServiceCreateView.as_view(), name='service-create'),
    path('services/<int:pk>/modifier/', views.ServiceUpdateView.as_view(), name='service-update'),
    path('services/<int:pk>/supprimer/', views.ServiceDeleteView.as_view(), name='service-delete'),
    
    # URLs pour les congés
    path('conges/', views.CongeListView.as_view(), name='conge-list'),
    path('conges/<int:pk>/', views.CongeDetailView.as_view(), name='conge-detail'),
    path('conges/nouveau/', views.CongeCreateView.as_view(), name='conge-create'),
    path('conges/<int:pk>/modifier/', views.CongeUpdateView.as_view(), name='conge-update'),
    path('conges/<int:pk>/supprimer/', views.CongeDeleteView.as_view(), name='conge-delete'),
    path('conges/<int:pk>/approbation/', views.CongeApprobationView.as_view(), name='conge-approbation'),
    path('conges/<int:pk>/approuver/', views.approuver_conge, name='conge-approuver'),
    path('conges/<int:pk>/rejeter/', views.rejeter_conge, name='conge-rejeter'),
    
    # URLs pour les exports et rapports
    path('export/employes/', views.export_employers_csv, name='export-employers'),
    path('export/conges/', views.export_conges_csv, name='export-conges'),
    path('rapports/conges-mensuel/', views.rapport_mensuel_conges, name='rapport-conges-mensuel'),
    
    # APIs
    path('api/dashboard/', views.api_dashboard_data, name='api-dashboard'),
    path('api/recherche/', views.recherche_globale, name='api-recherche'),
] 