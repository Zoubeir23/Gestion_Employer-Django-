from django import forms
from .models import Employer, Service, Conge

class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['nom', 'prenom', 'email', 'telephone', 'genre', 'date_embauche', 'poste', 'salaire', 'service']
        widgets = {
            'date_embauche': forms.DateInput(attrs={'type': 'date'}),
            'salaire': forms.NumberInput(attrs={'step': '0.01'}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['nom', 'description']

class CongeForm(forms.ModelForm):
    class Meta:
        model = Conge
        fields = ['type_conge', 'date_debut', 'date_fin', 'raison']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            'raison': forms.Textarea(attrs={'rows': 4}),
        } 