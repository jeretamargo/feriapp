

def notificaciones(request):
    if request.user.is_authenticated:
        return {
            "notificaciones": request.user.notificaciones.filter(leida=False),
            "num_notificaciones": request.user.notificaciones.filter(leida=False).count()
        }

    return {
        "notificaciones": [],
        "num_notificaciones":0

    }
