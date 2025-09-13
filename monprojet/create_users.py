#!/usr/bin/env python
"""
Script pour créer des utilisateurs de test et afficher les comptes disponibles
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User

def create_test_users():
    """Créer des utilisateurs de test"""
    print("🔧 Création d'utilisateurs de test...")
    
    # Utilisateur de test standard
    test_user, created = User.objects.get_or_create(
        username="testuser",
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'is_staff': False,
            'is_superuser': False
        }
    )
    
    if created:
        test_user.set_password('test123')
        test_user.save()
        print("✅ Utilisateur 'testuser' créé avec mot de passe 'test123'")
    else:
        print("ℹ️ Utilisateur 'testuser' existe déjà")
    
    # Gestionnaire RH
    hr_user, created = User.objects.get_or_create(
        username="rh_manager",
        defaults={
            'email': 'rh@example.com',
            'first_name': 'Manager',
            'last_name': 'RH',
            'is_staff': True,
            'is_superuser': False
        }
    )
    
    if created:
        hr_user.set_password('rh123')
        hr_user.save()
        print("✅ Gestionnaire RH 'rh_manager' créé avec mot de passe 'rh123'")
    else:
        print("ℹ️ Gestionnaire RH 'rh_manager' existe déjà")

def display_users():
    """Afficher tous les utilisateurs disponibles"""
    print("\n👥 COMPTES DE CONNEXION DISPONIBLES:")
    print("=" * 50)
    
    users = User.objects.all().order_by('username')
    
    for user in users:
        status = "🔴 Superadmin" if user.is_superuser else "🟡 Staff" if user.is_staff else "🟢 Utilisateur"
        
        print(f"{status} {user.username}")
        print(f"    📧 Email: {user.email}")
        print(f"    👤 Nom: {user.first_name} {user.last_name}")
        print(f"    🔐 Actif: {'Oui' if user.is_active else 'Non'}")
        print()

def main():
    """Fonction principale"""
    try:
        create_test_users()
        display_users()
        
        print("🔗 INFORMATIONS DE CONNEXION:")
        print("=" * 50)
        print("🌐 URL: http://127.0.0.1:8000/")
        print("🔐 Page de connexion: http://127.0.0.1:8000/accounts/login/")
        print("\n📋 COMPTES RECOMMANDÉS:")
        print("• Admin complet: 'admin' (mot de passe défini lors de la création)")
        print("• Test standard: 'testuser' / 'test123'")
        print("• Gestionnaire RH: 'rh_manager' / 'rh123'")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()