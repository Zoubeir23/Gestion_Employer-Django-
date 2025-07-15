from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.

class Service(models.Model):
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom du service")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def get_nombre_employes(self):
        return self.employer_set.count()

class Employer(models.Model):
    GENRE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES, verbose_name="Genre")
    email = models.EmailField(unique=True, verbose_name="Email")
    telephone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Téléphone")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Service")
    date_embauche = models.DateField(verbose_name="Date d'embauche")
    salaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salaire")
    poste = models.CharField(max_length=100, verbose_name="Poste")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    class Meta:
        verbose_name = "Employé"
        verbose_name_plural = "Employés"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def get_nombre_conges(self):
        return self.conge_set.count()

class Conge(models.Model):
    TYPE_CHOICES = [
        ('ANNUEL', 'Congé annuel'),
        ('MALADIE', 'Congé maladie'),
        ('MATERNITE', 'Congé maternité'),
        ('PATERNITE', 'Congé paternité'),
        ('AUTRE', 'Autre'),
    ]

    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('APPROUVE', 'Approuvé'),
        ('REJETE', 'Rejeté'),
    ]

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, verbose_name="Employé")
    type_conge = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type de congé")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(verbose_name="Date de fin")
    raison = models.TextField(blank=True, null=True, verbose_name="Raison")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE', verbose_name="Statut")
    date_demande = models.DateTimeField(auto_now_add=True, verbose_name="Date de la demande")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    approuve_par = models.ForeignKey(Employer, on_delete=models.SET_NULL, null=True, blank=True, related_name='conges_approuves', verbose_name="Approuvé par")
    commentaire_approbation = models.TextField(blank=True, null=True, verbose_name="Commentaire d'approbation")

    class Meta:
        verbose_name = "Congé"
        verbose_name_plural = "Congés"
        ordering = ['-date_demande']

    def __str__(self):
        return f"Congé de {self.employer} du {self.date_debut} au {self.date_fin}"

    def get_duree(self):
        return (self.date_fin - self.date_debut).days + 1
    
    @property
    def duree_jours(self):
        """Retourne la durée en jours"""
        return self.get_duree()
    
    @property
    def est_en_cours(self):
        """Vérifie si le congé est actuellement en cours"""
        today = timezone.now().date()
        return self.date_debut <= today <= self.date_fin and self.statut == 'APPROUVE'
    
    @property
    def jours_restants(self):
        """Calcule le nombre de jours restants avant le début du congé"""
        today = timezone.now().date()
        if self.date_debut > today:
            return (self.date_debut - today).days
        return 0
    
    @property
    def est_urgent(self):
        """Vérifie si la demande est urgente (en attente depuis plus de 7 jours)"""
        if self.statut == 'EN_ATTENTE':
            return (timezone.now().date() - self.date_demande.date()).days > 7
        return False

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.date_debut and self.date_fin:
            if self.date_debut > self.date_fin:
                raise ValidationError("La date de début doit être antérieure à la date de fin")
            
            # Vérifier les chevauchements pour le même employé
            if self.pk:  # Si c'est une modification
                chevauchements = Conge.objects.filter(
                    employer=self.employer,
                    statut='APPROUVE'
                ).exclude(pk=self.pk).filter(
                    date_debut__lte=self.date_fin,
                    date_fin__gte=self.date_debut
                )
            else:  # Si c'est une nouvelle demande
                chevauchements = Conge.objects.filter(
                    employer=self.employer,
                    statut='APPROUVE',
                    date_debut__lte=self.date_fin,
                    date_fin__gte=self.date_debut
                )
            
            if chevauchements.exists():
                raise ValidationError("Cette période chevauche avec un congé déjà approuvé")
