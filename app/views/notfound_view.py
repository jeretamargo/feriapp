from django.views.generic import TemplateView

class Error404View(TemplateView):
    
    template_name = "404page.html"

    def render_to_response(self, context, **response_kwargs):
        response_kwargs["status"] = 404
        return super().render_to_response(context, **response_kwargs)


def custom_404(request, exception):
    return Error404View.as_view()(request, exception=exception)