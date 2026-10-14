from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator,RegexValidator
from django.core.exceptions import ValidationError
def validate_email(value):
    if not value:
        raise ValidationError("l'email est obligatoire")
    if not value.endswith('@gmail.com'):
        raise ValidationError("format de l'email est invalide (@gmail.com required)")
matricule_validator=RegexValidator(
    regex="^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$"
                                   ,message="invalide")
# Create your models here.
class Utilisateur(AbstractUser):
    user_id=models.CharField(max_length=10,
                             primary_key=True,
                               editable=False)
    email=models.EmailField(unique=True,validators=[validate_email])
    telephone=models.CharField(max_length=15,
                               blank=True,
                               null=True)
    role=models.CharField(max_length=20,choices=[
                                ('chargeur','Chargeur'),
                            ('transporteur','Transporteur')  ,
                               ('admin','Administrateur')    ])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
            self.full_clean()
            super().save(*args, **kwargs)

class Entreprise(models.Model):
    raison_sociale=models.CharField(max_length=100)
    matricule_fiscal=models.CharField(max_length=17,unique=True,
                                      validators=[matricule_validator])
    type_entreprise=models.CharField(max_length=100,choices= [
        ('chargeur','Chargeur'),
         ('transporteur','Transporteur'),
    ],default='chargeur')
    adresse=models.TextField(validators=[MinLengthValidator(20,"Un minimum de 20 caractères pour accepter l’adresse ")])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    gerant=models.OneToOneField(Utilisateur,on_delete=models.CASCADE,related_name='entreprise')
    def __str__(self):
        return self.raison_sociale

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)