from django.views import View
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from usuarios.models.notificacion_models import Notificacion

class MarcarNotificacionLeidaView(View):

    def post(self, request, pk):

        notificacion = get_object_or_404(
            Notificacion,
            pk=pk,
            usuario=request.user
        )

        notificacion.marcar_leida()

        return redirect(request.META.get("HTTP_REFERER", "/"))