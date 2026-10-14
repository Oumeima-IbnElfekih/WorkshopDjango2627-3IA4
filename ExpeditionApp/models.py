from django.db import models
from EntrepriseApp.models import Entreprise
from django.utils import timezone
from django.core.exceptions import ValidationError
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
    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'chargeur':
            raise ValidationError({
                'entreprise': "Une expédition ne peut être créée que par une entreprise de type chargeur."
            })
    def save(self, *args,**kwargs):
        self.full_clean()
        self.reference=self._generate_ref()
        return super().save(*args,**kwargs)
    @classmethod
    def _generate_ref(cls):
        annee=timezone.now().strftime('%y')#2026 avec Y et 26 y
        prefixe= f"EXP-{annee}-"
        last_elem=(cls.objects
                   .filter(reference__startswith=prefixe)
                   .order_by('-reference').first())
        compteur = last_elem.reference[-5:] +1 if last_elem else 1
        if compteur > 99999:
            raise ValueError(f"limite de 99999 pour annee {annee}")
        return f"{prefixe}{compteur:05d}"