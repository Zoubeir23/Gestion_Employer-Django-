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

    class Meta:
        verbose_name = "Congé"
        verbose_name_plural = "Congés"
        ordering = ['-date_demande']

    def __str__(self):
        return f"Congé de {self.employer} du {self.date_debut} au {self.date_fin}"

    def get_duree(self):
        return (self.date_fin - self.date_debut).days + 1

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.date_debut and self.date_fin:
            if self.date_debut > self.date_fin:
                raise ValidationError("La date de début doit être antérieure à la date de fin")
            if self.date_debut < timezone.now().date():
                raise ValidationError("La date de début ne peut pas être dans le passé")
