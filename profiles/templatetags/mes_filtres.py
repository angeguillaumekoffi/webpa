from django import template
from profiles.models import Profile, BesoinsEmis, ApporterAide
from django.contrib.auth import get_user_model

User = get_user_model()
register = template.Library()

@register.simple_tag
def nom_utilisateur_simple(idt):
    apprt = User.objects.get(id=idt)
    try:
        return apprt.name
    except:
        return None

@register.simple_tag
def noms_nom(nom):
    try:
        user = User.objects.get(id=nom.user.id)
        apprt = Profile.objects.get(user=user)
        return apprt.user.name
    except:
        return None

@register.simple_tag
def contact(nom):
    try:
        apprt = Profile.objects.get(user=nom)
        return apprt.contact
    except:
        return None