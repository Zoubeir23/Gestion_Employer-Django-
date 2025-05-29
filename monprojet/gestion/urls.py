from django.urls import path
from . import views

urlpatterns = [
    # Page d'accueil
    path('', views.home, name='home'),

    # URLs pour les Services
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('services/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/update/', views.ServiceUpdateView.as_view(), name='service_update'),
    path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),

    # URLs pour les Employés
    path('employers/', views.EmployerListView.as_view(), name='employer_list'),
    path('employers/<int:pk>/', views.EmployerDetailView.as_view(), name='employer_detail'),
    path('employers/create/', views.EmployerCreateView.as_view(), name='employer_create'),
    path('employers/<int:pk>/update/', views.EmployerUpdateView.as_view(), name='employer_update'),
    path('employers/<int:pk>/delete/', views.EmployerDeleteView.as_view(), name='employer_delete'),

    # URLs pour les Congés
    path('conges/', views.CongeListView.as_view(), name='conge_list'),
    path('conges/<int:pk>/', views.CongeDetailView.as_view(), name='conge_detail'),
    path('conges/create/', views.CongeCreateView.as_view(), name='conge_create'),
    path('conges/<int:pk>/update/', views.CongeUpdateView.as_view(), name='conge_update'),
    path('conges/<int:pk>/delete/', views.CongeDeleteView.as_view(), name='conge_delete'),
] 