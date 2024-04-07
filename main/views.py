from django.views.generic import TemplateView
from .models import Principal
class Home(TemplateView):
    template_name = "home_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aquí se añaden los posts al contexto
        context['imagenes'] = Principal.objects.all()
        return context