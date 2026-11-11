from django.urls import path
from .views import *
app_name="vehicules"
urlpatterns = [
    path('create/',VehiculeCreateView.as_view(), name='create'),
    path('<int:pk>/update/',VehiculeUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/',DeleteVehiculeView.as_view(), name='delete'),
    path('',ListVehiculeView.as_view(), name='liste')
]