from django.db import models

# Create your models here.

class Service(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Employer(models.Model):
    nom = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_embauche = models.DateField()

    def __str__(self):
        return self.nom

class Conge(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    raison = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Congé pour {self.employer.nom} du {self.date_debut} au {self.date_fin}"
