from django import forms
from .models import Employer, Service, Conge
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.core.exceptions import ValidationError
from datetime import date

class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['nom', 'prenom', 'email', 'telephone', 'genre', 'date_embauche', 'poste', 'salaire', 'service']
        widgets = {
            'date_embauche': forms.DateInput(attrs={'type': 'date'}),
            'salaire': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('nom', css_class='form-group col-md-6 mb-0'),
                Column('prenom', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('telephone', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('genre', css_class='form-group col-md-4 mb-0'),
                Column('date_embauche', css_class='form-group col-md-4 mb-0'),
                Column('salaire', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('poste', css_class='form-group col-md-6 mb-0'),
                Column('service', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Enregistrer', css_class='btn btn-primary')
        )

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['nom', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'nom',
            'description',
            Submit('submit', 'Enregistrer', css_class='btn btn-primary')
        )

class CongeForm(forms.ModelForm):
    class Meta:
        model = Conge
        fields = ['employer', 'type_conge', 'date_debut', 'date_fin', 'raison']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'employer',
            'type_conge',
            Row(
                Column('date_debut', css_class='form-group col-md-6 mb-0'),
                Column('date_fin', css_class='form-group col-md-6 mb-0'),
            ),
            'raison',
            Submit('submit', 'Enregistrer', css_class='btn btn-primary')
        )

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        type_conge = cleaned_data.get('type_conge')
        employer = cleaned_data.get('employer')

        if date_debut and date_fin:
            # Vérifier que la date de début n'est pas dans le passé
            if date_debut < date.today():
                raise ValidationError("La date de début ne peut pas être dans le passé.")

            # Vérifier que la date de fin est après la date de début
            if date_fin < date_debut:
                raise ValidationError("La date de fin doit être postérieure à la date de début.")

            # Vérifier la durée maximale selon le type de congé
            duree = (date_fin - date_debut).days + 1
            if type_conge == 'ANNUEL' and duree > 30:
                raise ValidationError("La durée maximale des congés annuels est de 30 jours.")
            elif type_conge == 'MALADIE' and duree > 15:
                raise ValidationError("La durée maximale des congés maladie est de 15 jours.")
            elif type_conge == 'MATERNITE' and duree > 98:
                raise ValidationError("La durée maximale des congés maternité est de 98 jours.")
            elif type_conge == 'PATERNITE' and duree > 14:
                raise ValidationError("La durée maximale des congés paternité est de 14 jours.")

            # Vérifier les chevauchements de congés
            if employer:
                conges_existants = Conge.objects.filter(
                    employer=employer,
                    date_debut__lte=date_fin,
                    date_fin__gte=date_debut
                )
                if self.instance.pk:  # Si c'est une modification
                    conges_existants = conges_existants.exclude(pk=self.instance.pk)
                if conges_existants.exists():
                    raise ValidationError("L'employé a déjà un congé sur cette période.")

        return cleaned_data

class CongeApprobationForm(forms.ModelForm):
    class Meta:
        model = Conge
        fields = ['statut', 'commentaire_approbation']
        widgets = {
            'commentaire_approbation': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'statut',
            'commentaire_approbation',
            Submit('submit', 'Enregistrer', css_class='btn btn-primary')
        ) 