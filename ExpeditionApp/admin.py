from django.contrib import admin,messages
from .models import Expedition
from django.utils import timezone
from offreApp.models import Offre
from django.utils.html import format_html
# Register your models here.
# Couleur du badge par statut (gris par défaut si un nouveau statut est ajouté et oublié ici).
STATUT_COLORS = {
    'publiee': '#0d6efd',
    'en_cours': '#fd7e14',
    'attribuee': '#6f42c1',
    'livree': '#198754',
    'annulee': '#dc3545',
}
class OffreInline(admin.TabularInline):
    # Lecture seule : une offre se crée/évolue via les règles métier d'OffresApp,
    # pas en la modifiant à la main depuis la fiche de l'expédition.
    model = Offre
    fields = ('transporteur', 'vehicule', 'prix', 'delai_jours', 'statut', 'date_proposition')
    readonly_fields = fields
    extra = 0
    can_delete = False
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False


class OffreInlineStacked(admin.StackedInline):
    # exactement le même comportement qu'OffreInline (lecture seule, pas d'ajout), seule la mise en forme change (StackedInline = un bloc vertical par offre, au lieu d'une ligne de tableau). 
    model = Offre
    fields = ('transporteur', 'vehicule', 'prix', 'delai_jours', 'statut', 'date_proposition')
    readonly_fields = fields
    extra = 0
    can_delete = False
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False
# Register your models here.
class EnretardFilter(admin.SimpleListFilter):
    title= 'en retard'
    parameter_name= 'en_retard'
    def lookups(self,req,model):
        return [('oui','OUI'),('non','NON')]
    def queryset(self, request, queryset):
        today= timezone.now().date()
        if self.value()=='oui':
            return queryset.filter(statut='publiee', date_souhaitee__lt=today)
        if self.value()=='non':
            return queryset.exclude(statut='publiee', date_souhaitee__lt=today)
        return queryset
@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display=('reference','statut')
    list_filter=('date_souhaitee',EnretardFilter)
    actions=['make_it_livree']
    @admin.action(description=" Clôturer les expéditions sélectionnées")
    def make_it_livree(self,req,queryset):
        liste= queryset.filter(statut='en_cours')
        liste_ignored_el=queryset.exclude(statut='en_cours').count()
        errors=[]
        nbr_sucess=0
        for exp in liste:
            exp.statut='livree'
            try:
                exp.save()
                nbr_sucess+=1
            except:
                errors.append(f"{exp.reference} : this expedition had an error")
        if nbr_sucess:
            self.message_user(
                req,
                f"{nbr_sucess} expeditions cloturées",
                messages.SUCCESS
            )
        if liste_ignored_el:
             self.message_user(
                            req,
                            f"{liste_ignored_el} expeditions ignorées",
                            messages.WARNING
                        )
        for e in errors:
            self.message_user( req, e,messages.ERROR)

    readonly_fields = ('reference', 'created_at', 'updated_at')
    search_fields = ('reference', 'ville_depart', 'ville_arrivee', 'entreprise__raison_sociale')
    fieldsets = (
        ('Expédition', {
            'fields': ('reference', 'entreprise', )
        }),
        ('Itinéraire et poids', {
            'fields': ('ville_depart', 'ville_arrivee', 'poids_kg', 'date_souhaitee')
        }),
        ('Statut et horodatage', {
            'fields': ('statut', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    @admin.display(description='Statut', ordering='statut')
    def statut_badge(self, obj):
        color = STATUT_COLORS.get(obj.statut, '#6c757d')
        return format_html(
            '<span style="background-color:{}; color:#fff; padding:2px 10px; '
            'border-radius:10px; font-size:12px; font-weight:600;">{}</span>',
            color, obj.get_statut_display(),
        )