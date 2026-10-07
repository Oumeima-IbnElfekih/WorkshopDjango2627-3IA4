from django.db import models
from EntrepriseApp.models import Entreprise
# Create your models here.
class Expedition(models.Model):
    reference=models.CharField(max_length=20,editable=False)
    date_souhaitee=models.DateField()
    ville_depart=models.CharField(max_length=100)
    ville_arrivee=models.CharField(max_length=100)
    poids_kg=models.DecimalField(decimal_places=3,max_digits=10)
    statut=models.CharField(max_length=100,choices=[
        ('publiee', 'Publiée'),
        ('en_cours', 'En cours'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
        ('attribuee', 'Attribuée')
    ], default='publiee')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    entreprise=models.ForeignKey(Entreprise,
                                 on_delete=models.CASCADE,
                                 related_name='expeditions')