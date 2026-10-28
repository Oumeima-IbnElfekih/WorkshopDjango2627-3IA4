from django.urls import path
from .views import *
app_name = 'expeditions'
urlpatterns =[

    path("",ExpeditionListView.as_view(),name="liste"),
    path('<str:reference>/', ExpeditionDetailView.as_view(), name='detail'),
]