from __future__ import unicode_literals
from django.contrib import admin
from authtools.admin import NamedUserAdmin
from .models import *
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html

User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = Profile


class NewUserAdmin(NamedUserAdmin):
    inlines = [UserProfileInline]
    list_display = (
        "is_active",
        "email",
        "name",
        "permalink",
        "is_superuser",
        "is_staff",
    )

    # 'View on site' didn't work since the original User model needs to
    # have get_absolute_url defined. So showing on the list display
    # was a workaround.
    def permalink(self, obj):
        url = reverse("profiles:show", kwargs={"slug": obj.profile.slug})
        # Unicode hex b6 is the Pilcrow sign
        return format_html('<a href="{}">{}</a>'.format(url, "\xb6"))

class BeneficeAdmin(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ['montantBenefice']
    ordering = ['utilisateur']
    list_display = ('utilisateur', 'montantBenefice', 'dateBenefice', )

class BesoinsAdmin(admin.ModelAdmin):
    list_per_page = 10
    ordering = ['etatDuBesoin','dateDeDemande']
    search_fields = ['montantDuBesoin']
    readonly_fields = ('utilisateur', 'idAide', 'etatDuBesoin')
    list_display = ('utilisateur', 'idAide', 'dateDeDemande', 'montantDuBesoin', 'paye', 'restant', 'etatDuBesoin', )

class SouscriptionAdmin(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ['utilisateur']
    list_display = ["utilisateur","dateDeSousrcription","dateDexpiration","moyenDePaiment","statutCompte"]

class ApportAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if obj.fichierJoint:
            return format_html('<a href="{0}"><img src="{1}" style="width:60px; height:40px"/></a>'.format(obj.fichierJoint.url, obj.fichierJoint.url))

    image_tag.short_description = 'Image'
    list_per_page = 10
    
    ordering = ['activTransact','-dateDeSoumission']
    search_fields = ["dateDeSoumission"]
    list_display_links = ["dateDeSoumission"]
    list_display = [
        "dateDeSoumission", 
        "_emetteur",
        "montantApporte", 
        "_recepteur",
        "activTransact",
        "etatDapport",
        "etatDeReception",
        "dateDeValidation",
        "image_tag"
    ]
    def _recepteur(self, obj):
        if obj.activTransact:
            url = reverse("profiles:show", kwargs={"slug": obj.recepteur.slug})
            return format_html('<a href="{}">{}</a>'.format(url, obj.recepteur.user.name))
    
    def _emetteur(self, obj):
        if not obj.emetteur == None:
            url = reverse("profiles:show", kwargs={"slug": obj.emetteur.slug})
            return format_html('<a href="{}">{}</a>'.format(url, obj.emetteur.user.name))
    
    

admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)
admin.site.register(Souscriptions, SouscriptionAdmin)
admin.site.register(ApporterAide, ApportAdmin)
admin.site.register(BesoinsEmis, BesoinsAdmin)
admin.site.register(Benefices, BeneficeAdmin)