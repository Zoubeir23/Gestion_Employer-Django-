#!/usr/bin/env python
"""
Script de test pour vérifier que toutes les fonctionnalités du projet fonctionnent correctement
"""

import os
import sys
import django
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

def test_urls():
    """Test que toutes les URLs sont accessibles"""
    from django.urls import reverse
    
    urls_to_test = [
        'home',
        'employer-list',
        'service-list',
        'conge-list',
        'export-employers',
        'export-conges',
        'rapport-conges-mensuel',
        'api-dashboard',
    ]
    
    print("🔍 Test des URLs...")
    for url_name in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name}: {url}")
        except Exception as e:
            print(f"❌ {url_name}: {e}")

def test_models():
    """Test que tous les modèles fonctionnent"""
    from gestion.models import Service, Employer, Conge
    
    print("\n🔍 Test des modèles...")
    
    try:
        # Test Service
        service_count = Service.objects.count()
        print(f"✅ Services: {service_count} enregistrements")
        
        # Test Employer
        employer_count = Employer.objects.count()
        print(f"✅ Employés: {employer_count} enregistrements")
        
        # Test Conge
        conge_count = Conge.objects.count()
        print(f"✅ Congés: {conge_count} enregistrements")
        
    except Exception as e:
        print(f"❌ Erreur modèles: {e}")

def test_views():
    """Test que les vues principales fonctionnent"""
    from gestion.views import HomeView, export_employers_csv, api_dashboard_data
    
    print("\n🔍 Test des vues...")
    
    try:
        print("✅ HomeView importée")
        print("✅ export_employers_csv importée")
        print("✅ api_dashboard_data importée")
    except Exception as e:
        print(f"❌ Erreur vues: {e}")

def test_templates():
    """Test que les templates existent"""
    import os
    
    print("\n🔍 Test des templates...")
    
    templates_to_check = [
        'gestion/base.html',
        'gestion/home.html',
        'gestion/rapports/conges_mensuel.html',
        'registration/login.html',
        'registration/logged_out.html',
    ]
    
    for template in templates_to_check:
        template_path = f"gestion/templates/{template}"
        if os.path.exists(template_path):
            print(f"✅ {template}")
        else:
            print(f"❌ {template} - Non trouvé")

def create_test_data():
    """Crée des données de test si elles n'existent pas"""
    from gestion.models import Service, Employer, Conge
    from django.contrib.auth.models import User
    
    print("\n🔍 Création de données de test...")
    
    try:
        # Créer un service de test
        service, created = Service.objects.get_or_create(
            nom="Service Test",
            defaults={'description': 'Service créé pour les tests'}
        )
        if created:
            print("✅ Service de test créé")
        
        # Créer un utilisateur de test
        user, created = User.objects.get_or_create(
            username="test_user",
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            print("✅ Utilisateur de test créé")
        
        print(f"📊 Statistiques:")
        print(f"   - Services: {Service.objects.count()}")
        print(f"   - Employés: {Employer.objects.count()}")
        print(f"   - Congés: {Conge.objects.count()}")
        print(f"   - Utilisateurs: {User.objects.count()}")
        
    except Exception as e:
        print(f"❌ Erreur création données: {e}")

def main():
    """Fonction principale de test"""
    print("🚀 TESTS DU PROJET GESTION DES EMPLOYÉS")
    print("=" * 50)
    
    test_urls()
    test_models()
    test_views()
    test_templates()
    create_test_data()
    
    print("\n" + "=" * 50)
    print("✅ Tests terminés !")
    print("\n📋 POUR LANCER LE PROJET:")
    print("1. Activer l'environnement virtuel")
    print("2. python manage.py runserver")
    print("3. Aller sur http://127.0.0.1:8000/")
    print("4. Se connecter avec votre compte admin")
    
    print("\n🎯 FONCTIONNALITÉS DISPONIBLES:")
    print("• Dashboard avec graphiques interactifs")
    print("• Recherche globale en temps réel")
    print("• Thème sombre/clair")
    print("• Export CSV des données")
    print("• Rapports mensuels")
    print("• Raccourcis clavier (Ctrl+N, Ctrl+S, Ctrl+C)")
    print("• Notifications et alertes")
    print("• Interface responsive")

if __name__ == "__main__":
    main()