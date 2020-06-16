from django.views import generic
from django.contrib import messages
from Infos.models import Informations


class HomePage(generic.TemplateView):
    template_name = "home.html"
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        infos = Informations.objects.all()

        kwargs["infos"] = infos
        messages.info(request, "Bienvenue dans la communauté. Un monde nouveau s'ouvre à vous dès aujourd'hui.")
        return super().get(request, *args, **kwargs)


class AboutPage(generic.TemplateView):
    template_name = "about.html"