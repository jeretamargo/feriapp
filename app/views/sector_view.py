from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from app.models import Sector
from app.forms.sector_form import SectorForm


# List View 
class SectorListView(LoginRequiredMixin, ListView):
    model = Sector
    template_name = 'sector/lista_sector.html'
    context_object_name = 'sectores'
    #paginate_by = 10


# Detail View 
class SectorDetailView(LoginRequiredMixin, DetailView):
    model = Sector
    template_name = 'sector/actualizar_sector.html'
    context_object_name = 'sector'


# Create View 
class SectorCreateView(LoginRequiredMixin, CreateView):
    model = Sector
    template_name = 'sector/nuevo_sector.html'
    #fields = '__all__'
    success_url = reverse_lazy('sector-list')
    form_class = SectorForm


# Update View 
class SectorUpdateView(LoginRequiredMixin, UpdateView):
    model = Sector
    template_name = 'sector/actualizar_sector.html'
    #fields = '__all__'
    fomr_class = SectorForm
    success_url = reverse_lazy('sector-list')


# Delete View  
class SectorDeleteView(LoginRequiredMixin, DeleteView):
    model = Sector
    template_name = 'sector/borrar_sector.html'
    success_url = reverse_lazy('sector-list')
