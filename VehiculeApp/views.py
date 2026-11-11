from django.shortcuts import render
from django.views.generic   import CreateView,ListView,UpdateView,DeleteView
from .models import Vehicule
from django.urls import reverse_lazy
from .forms import VehiculeForm
# Create your views here.
class VehiculeCreateView(CreateView):
    model= Vehicule
    template_name ='vehicules/form.html'
    #fields ='__all__'
    form_class = VehiculeForm
    success_url = reverse_lazy('vehicules:liste')
class VehiculeUpdateView(UpdateView):
    model= Vehicule
    template_name ='vehicules/form.html'
    #fields ='__all__'
    form_class = VehiculeForm
    success_url = reverse_lazy('vehicules:liste')
class ListVehiculeView(ListView):
    model= Vehicule
    template_name="vehicules/liste.html"
    context_object_name ='vehicules'
class DeleteVehiculeView(DeleteView):
    model=Vehicule
    template_name ="vehicules/confirm_delete.html"
    context_object_name ='vehicule'
    success_url = reverse_lazy('vehicules:liste')
