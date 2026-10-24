from django.contrib import admin
from .models import Utilisateur,Entreprise
from django.contrib.auth.admin import  UserAdmin
from VehiculeApp.models import Vehicule
# Register your models here.
admin.site.site_title="TransConnect"
admin.site.site_header="DashBoard Admin TransConnect"
admin.site.index_title="Admin TransConnect"
@admin.register(Utilisateur)
class AdminUtilisateur(UserAdmin):
    list_display=('username','user_id','first_name','last_name','role')
    list_filter=('email',)
    list_editable=('first_name','last_name')
    search_fields=('email','telephone')
    ordering=('-created_at',)
    list_per_page=10
    date_hierarchy='created_at'
    readonly_fields = ('user_id', 'date_joined', 'last_login', 'created_at', 'updated_at')
    fieldsets = (
        ('Identité', {
            'fields': ('user_id', 'username', 'email', 'telephone')
        }),
        ('Rôle et permissions', {
            'fields': ('role', 'password', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Horodatage', {
            'fields': ('date_joined', 'last_login', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
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
    list_display = ('raison_sociale', 'matricule_fiscal', 'type_entreprise', 'gerant', 'created_at')
    list_filter = ('type_entreprise', 'created_at')
    search_fields = ('raison_sociale', 'matricule_fiscal', 'gerant__username', 'gerant__email')
    list_select_related = ('gerant',)
    list_editable = ('type_entreprise',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 25
    readonly_fields =(  'created_at','updated_at')


