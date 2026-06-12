from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from app.mixins.AdminReq import AdminRequiredMixin
from app.forms.form_feria import FeriaForm
from app.models.feria_models import Feria
from app.models.categoria_models import Categoria
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.db.models import Avg
from app.models.resena_models import Resena


class ListaFeriasView(LoginRequiredMixin,ListView):
    """Lista todas las ferias activas."""

    model = Feria
    template_name = "ferias/lista_ferias.html"
    context_object_name = "ferias"
    

    def get_queryset(self):
        qs = Feria.objects.all()
        # aplicar filtros desde query params
        if self.request.GET:
            nombre = self.request.GET.get("nombre")
            categoria = self.request.GET.get("categoria")
            fecha_from = self.request.GET.get("fecha_inicio_from")
            fecha_to = self.request.GET.get("fecha_inicio_to")
            ubicacion = self.request.GET.get("ubicacion")
            activa = self.request.GET.get("activa")

            if nombre:
                qs = qs.filter(nombre__icontains=nombre)
            if categoria:
                qs = qs.filter(categoria=categoria)
            if fecha_from:
                qs = qs.filter(fecha_inicio__gte=fecha_from)
            if fecha_to:
                qs = qs.filter(fecha_inicio__lte=fecha_to)
            if ubicacion:
                qs = qs.filter(ubicacion__icontains=ubicacion)
            # Si el parámetro 'activa' vino explícitamente en la query y vale
            # "true" o "false", aplicarlo. Si no viene o viene vacío, no
            # aplicamos filtro (por defecto mostrar todas).
            if 'activa' in self.request.GET:
                if activa == "true":
                    qs = qs.filter(activa=True)
                elif activa == "false":
                    qs = qs.filter(activa=False)
        else:
            # form inválido: no aplicar filtro por defecto (mostrar todas)
            pass

        return qs.order_by("fecha_inicio")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pasar las categorias y ubicaciones para los dropdowns
        context["categorias"] = Categoria.objects.all()
        context["ubicaciones"] = Feria.objects.values_list('ubicacion', flat=True).distinct()
        # separar ferias en próximas y pasadas según fecha_fin
        today = date.today()
        qs = self.get_queryset()
        proximas_qs = qs.filter(fecha_fin__gte=today).order_by('fecha_inicio')
        pasadas_qs = qs.filter(fecha_fin__lt=today).order_by('-fecha_inicio')

        # paginar 6 por página en cada sección
        per_page = 6
        page_proximas = self.request.GET.get('page_proximas')
        page_pasadas = self.request.GET.get('page_pasadas')

        # Próximas
        if proximas_qs.exists():
            proximas_paginator = Paginator(proximas_qs, per_page)
            try:
                proximas_page = proximas_paginator.page(page_proximas)
            except PageNotAnInteger:
                proximas_page = proximas_paginator.page(1)
            except EmptyPage:
                proximas_page = proximas_paginator.page(proximas_paginator.num_pages)
        else:
            proximas_page = None

        # Pasadas
        if pasadas_qs.exists():
            pasadas_paginator = Paginator(pasadas_qs, per_page)
            try:
                pasadas_page = pasadas_paginator.page(page_pasadas)
            except PageNotAnInteger:
                pasadas_page = pasadas_paginator.page(1)
            except EmptyPage:
                pasadas_page = pasadas_paginator.page(pasadas_paginator.num_pages)
        else:
            pasadas_page = None

        context['proximas_page_obj'] = proximas_page
        context['pasadas_page_obj'] = pasadas_page

        # base_query: parámetros GET sin paginación, para preservar filtros en enlaces de página
        params = self.request.GET.copy()
        params.pop('page_proximas', None)
        params.pop('page_pasadas', None)
        context['base_query'] = params.urlencode()
        return context
    
    

class NuevaFeriaView(AdminRequiredMixin,LoginRequiredMixin,CreateView):
    """Vista para crear una nueva feria."""

    model = Feria
    template_name = "ferias/nueva_feria.html"
    form_class = FeriaForm
    #fields = ["nombre", "categoria", "fecha_inicio", "fecha_fin", "ubicacion", "capacidad_puestos"]
    success_url = reverse_lazy('ferias:lista_ferias')
    

    def form_valid(self, form):
        # Usar el método `Feria.new` para crear la instancia usando cleaned_data
        data = form.cleaned_data
        feria, errors = Feria.new(
            data.get("nombre"),
            data.get("categoria"),
            data.get("fecha_inicio"),
            data.get("fecha_fin"),
            data.get("ubicacion"),
            data.get("capacidad_puestos"),
        )
        if errors:
            for err in errors:
                messages.error(self.request, err)
            return self.form_invalid(form)

        self.object = feria
        response = HttpResponseRedirect(self.get_success_url())
        # if not self.request.user.has_perm("ferias.add_feria"):
        #     messages.error(self.request, "No tienes permisos para crear ferias.")
        #     return self.form_invalid(form)
        
        messages.success(
        self.request,
        f"La Feria '{self.object.nombre}' fue creada correctamente. "
        f"<a href='{reverse_lazy('ferias:detalle_feria', args=[self.object.pk])}' class='alert-link'>Ver detalle</a>")
        
        return response
    
    def form_invalid(self, form):
        # Enviar todos los errores del formulario como mensajes
        for field, errors in form.errors.items():
            for error in errors:
                if field == "__all__":
                    messages.error(self.request, f"Error general: {error}")
                else:
                    messages.error(self.request, f"Error en {field}: {error}")
        return super().form_invalid(form)

class DetalleFeriaView(LoginRequiredMixin, DetailView):
    """Vista para mostrar los detalles de una feria."""

    model = Feria
    template_name = "ferias/detalle_feria.html"
    context_object_name = "feria"

    def get_context_data(self, **kwargs):
        """Agrega la cantidad de puestos ocupados y disponibles a la plantilla."""
        context = super().get_context_data(**kwargs)
        context["puestos_ocupados"] = self.object.puestos_ocupados() # pyright: ignore[reportAttributeAccessIssue]
        context["puestos_disponibles"] = self.object.puestos_disponibles() # pyright: ignore[reportAttributeAccessIssue]
        # Obtener inscripciones y añadir promedio de reseñas (evitar N+1)
        inscripciones_qs = list(self.object.inscripcion_set.select_related('emprendedor').order_by('numero_puesto'))
        emprendedor_ids = [i.emprendedor_id for i in inscripciones_qs]
        avg_map = Resena.avg_for_emprendedores(emprendedor_ids)
        # Adjuntar atributo dinámico a cada inscripcion
        for ins in inscripciones_qs:
            ins.avg_puntuacion = avg_map.get(ins.emprendedor_id)
        context['inscripciones'] = inscripciones_qs
        return context
    
class DeleteFeriaView(AdminRequiredMixin,LoginRequiredMixin,DeleteView):
    """Vista para eliminar una feria."""

    model = Feria
    template_name = "ferias/borrar_feria.html"
    success_url = reverse_lazy('ferias:lista_ferias')
    
    def get_success_url(self):
        messages.warning(self.request, f"La feria '{self.object.nombre}' fue borrada exitosamente.")
        return super().get_success_url()

class UpdateFeriaView(AdminRequiredMixin,LoginRequiredMixin,UpdateView):
    """Vista para actualizar una feria."""

    model = Feria
    form_class = FeriaForm
    template_name = "ferias/actualizar_feria.html"
    #fields = ["nombre", "categoria", "fecha_inicio", "fecha_fin", "ubicacion", "capacidad_puestos"]
    success_url = reverse_lazy('ferias:lista_ferias')
    
    def form_valid(self, form):
        """Marca la feria como activa al actualizarla."""
        
        data = form.cleaned_data
        errors = self.object.update(
            data.get("nombre"),
            data.get("categoria"),
            data.get("fecha_inicio"),
            data.get("fecha_fin"),
            data.get("ubicacion"),
            data.get("capacidad_puestos"),
        )
        if errors:
            for err in errors:
                messages.error(self.request, err)
            return self.form_invalid(form)

        messages.info(
            self.request,
            f"La Feria '{self.object.nombre}' fue actualizada correctamente. "
            f"<a href='{reverse_lazy('ferias:detalle_feria', args=[self.object.pk])}' class='alert-link'>Ver detalle</a>")
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form):
        # Enviar todos los errores del formulario como mensajes
        for field, errors in form.errors.items():
            for error in errors:
                if field == "__all__":
                    messages.error(self.request, f"Error general: {error}")
                else:
                    messages.error(self.request, f"Error en {field}: {error}")
        return super().form_invalid(form)
    