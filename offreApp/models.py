from django.db import models

# Create your models here.
class Offre(models.Model):
    date_proposition=models.DateField(auto_now_add=True)
    delai_jours=models.PositiveIntegerField()
    prix=models.DecimalField(max_digits=10,decimal_places=2)
    statut=models.CharField(max_length=10, choices=[
        ('proposee','proposee'),
         ('acceptee','acceptee'),
          ('refusee','refusee'),
           ('retiree','retiree')
    ],default='proposee')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    expedition=models.ForeignKey('ExpeditionApp.Expedition',on_delete=models.CASCADE,related_name='offres')
    vehicule=models.ForeignKey('VehiculeApp.Vehicule',on_delete=models.CASCADE,related_name='offres')
    transporteur=models.ForeignKey('EntrepriseApp.Entreprise',on_delete=models.CASCADE,related_name='offres')
