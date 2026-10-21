from django.contrib import admin
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