from django.contrib import admin,messages
from .models import Expedition
from django.utils import timezone
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

