from django.contrib import admin
from .models import Utilisateur,Entreprise
from django.contrib.auth.admin import  UserAdmin
from VehiculeApp.models import Vehicule
# Register your models here.
admin.site.site_title="TransConnect"
admin.site.site_header="DashBoard Admin TransConnect"
admin.site.index_title="Admin TransConnect"
@admin.register(Utilisateur)
class AdminUtilisateur(admin.ModelAdmin):
    list_display=('username','user_id','first_name','last_name','role')
    list_filter=('email',)
    list_editable=('first_name','last_name')
    search_fields=('email','telephone')
    ordering=('-created_at',)
    list_per_page=10
    date_hierarchy='created_at'
#admin.site.register(Utilisateur,AdminUtilisateur)
#class vehiculeInline(admin.StackedInline):
class vehiculeInline(admin.TabularInline):
    model=Vehicule
    extra=1
 #   fields=('',)
  
@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    inlines =[vehiculeInline]
    fieldsets = ( ('Information general', {
            'fields' : ('raison_sociale','matricule_fiscal')
        }),
        ('Entreprise Info', {
            'fields' :('type_entreprise','adresse','gerant')
        }), 
        ('dates', {
          'fields':(  'created_at','updated_at')
        })
    )
    readonly_fields =(  'created_at','updated_at')


