# Generated by Django 5.2.1 on 2025-05-30 11:45

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conge',
            options={'ordering': ['-date_demande'], 'verbose_name': 'Congé', 'verbose_name_plural': 'Congés'},
        ),
        migrations.AlterModelOptions(
            name='employer',
            options={'ordering': ['nom', 'prenom'], 'verbose_name': 'Employé', 'verbose_name_plural': 'Employés'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['nom'], 'verbose_name': 'Service', 'verbose_name_plural': 'Services'},
        ),
        migrations.AddField(
            model_name='conge',
            name='date_demande',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date de la demande'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conge',
            name='date_modification',
            field=models.DateTimeField(auto_now=True, verbose_name='Dernière modification'),
        ),
        migrations.AddField(
            model_name='conge',
            name='statut',
            field=models.CharField(choices=[('EN_ATTENTE', 'En attente'), ('APPROUVE', 'Approuvé'), ('REJETE', 'Rejeté')], default='EN_ATTENTE', max_length=20, verbose_name='Statut'),
        ),
        migrations.AddField(
            model_name='conge',
            name='type_conge',
            field=models.CharField(choices=[('ANNUEL', 'Congé annuel'), ('MALADIE', 'Congé maladie'), ('MATERNITE', 'Congé maternité'), ('PATERNITE', 'Congé paternité'), ('AUTRE', 'Autre')], default='ANNUEL', max_length=20, verbose_name='Type de congé'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employer',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date de création'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employer',
            name='date_modification',
            field=models.DateTimeField(auto_now=True, verbose_name='Dernière modification'),
        ),
        migrations.AddField(
            model_name='employer',
            name='email',
            field=models.EmailField(default='admin@gmail.com', max_length=254, unique=True, verbose_name='Email'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employer',
            name='genre',
            field=models.CharField(choices=[('M', 'Masculin'), ('F', 'Féminin')], default='M', max_length=1, verbose_name='Genre'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employer',
            name='poste',
            field=models.CharField(default='Inconnu', max_length=100, verbose_name='Poste'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employer',
            name='prenom',
            field=models.CharField(default='Inconnu', max_length=100, verbose_name='Prénom'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employer',
            name='salaire',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Salaire'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employer',
            name='telephone',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Téléphone'),
        ),
        migrations.AddField(
            model_name='service',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date de création'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='date_modification',
            field=models.DateTimeField(auto_now=True, verbose_name='Dernière modification'),
        ),
        migrations.AddField(
            model_name='service',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='conge',
            name='date_debut',
            field=models.DateField(verbose_name='Date de début'),
        ),
        migrations.AlterField(
            model_name='conge',
            name='date_fin',
            field=models.DateField(verbose_name='Date de fin'),
        ),
        migrations.AlterField(
            model_name='conge',
            name='employer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.employer', verbose_name='Employé'),
        ),
        migrations.AlterField(
            model_name='conge',
            name='raison',
            field=models.TextField(blank=True, null=True, verbose_name='Raison'),
        ),
        migrations.AlterField(
            model_name='employer',
            name='date_embauche',
            field=models.DateField(verbose_name="Date d'embauche"),
        ),
        migrations.AlterField(
            model_name='employer',
            name='nom',
            field=models.CharField(max_length=100, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='employer',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.service', verbose_name='Service'),
        ),
        migrations.AlterField(
            model_name='service',
            name='nom',
            field=models.CharField(max_length=100, unique=True, verbose_name='Nom du service'),
        ),
    ]
