from __future__ import unicode_literals
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from . import forms
from . import models

User = get_user_model()

def verif_delai():
    actu = datetime.now()
    #Control des confirmations d'envoi
    try:
        apports = models.ApporterAide.objects.filter(etatDapport=False, dateLimiteEnvoi__lte=actu)
        for elmt in apports:
            usr =  User.objects.get(id=elmt.emetteur.user.id)
            usr.is_active = False
            usr.save(update_fields=['is_active'])
            elmt.delete()
    except:
        pass
    #Control des confirmations de reeception
    try:
        apports = models.ApporterAide.objects.filter(etatDeReception=False, etatDapport=True, dateLimiteReception__lte=actu)
        for elmt in apports:
            usr =  User.objects.get(id=elmt.recepteur.user.id)
            usr.is_active = False
            usr.save(update_fields=['is_active'])
    except:
        pass
    #Control abonnements
    try:
        souscripts = models.Souscriptions.objects.filter(dateDexpiration__lte=actu)
        for ssc in souscripts:
            ssc.statutCompte = False
            ssc.save(update_fields=['statutCompte'])
    except:
        pass

class ShowProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/show_profile.html"
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        verif_delai()
        slug = self.kwargs.get("slug")
        if slug:
            profile = get_object_or_404(models.Profile, slug=slug)
            user = profile.user
        else:
            user = self.request.user

        if user == self.request.user:
            kwargs["editable"] = True
        try:    
            abonnement = models.Souscriptions.objects.get(utilisateur=user.profile)
        except models.Souscriptions.DoesNotExist:
            abonnement = None
            messages.warning(request, 
            "Bienvenue {}, vous devez vous abonner à valeur de 47€ pour un mois afin de pouvoir apporter et recevoir de l'aide !"
            "  Merci de vous abonner.".format(user.name),
            )
        Histo = models.ApporterAide.objects.filter(Q(emetteur=user.profile) | Q(recepteur=user.profile)).order_by("-dateDeSoumission")[:10]
        Apaye = models.ApporterAide.objects.filter(emetteur=user.profile, activTransact=True, etatDapport=False).order_by("-dateDeSoumission")[:3]
        paye = models.ApporterAide.objects.filter(emetteur=user.profile, etatDapport=True).order_by("-dateDeValidation")[:3]
        Arecevoir = models.ApporterAide.objects.filter(recepteur=user.profile, etatDeReception=False).order_by("-dateDeSoumission")[:3]
        recu = models.ApporterAide.objects.filter(recepteur=user.profile, etatDeReception=True).order_by("-dateDeSoumission")[:3]
        recent = models.ApporterAide.objects.filter(emetteur=user.profile, etatDapport=False).order_by("-dateDeSoumission")[:4]
        kwargs["show_user"] = user
        kwargs["Abonnement"] = abonnement
        kwargs["Apaye"] = Apaye
        kwargs["paye"] = paye
        kwargs["Arecevoir"] = Arecevoir
        kwargs["recu"] = recu
        kwargs["Histo"] = Histo
        kwargs["recent"] = recent

        if not abonnement.statutCompte:
            messages.warning(request, 
            "Bienvenue {}, vous devez vous abonner à valeur de 47€ pour un mois afin de pouvoir apporter et recevoir de l'aide !"
            "  Merci de vous abonner.".format(user.name),
            )
        return super().get(request, *args, **kwargs)


class EditProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/edit_profile.html"
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        verif_delai()
        user = self.request.user
        if "user_form" not in kwargs:
            kwargs["user_form"] = forms.UserForm(instance=user)
        if "profile_form" not in kwargs:
            kwargs["profile_form"] = forms.ProfileForm(instance=user.profile)
        
        try:
            abonnement = models.Souscriptions.objects.get(utilisateur=self.request.user.profile)
        except models.Souscriptions.DoesNotExist:
            abonnement = None

        kwargs["show_user"] = user
        kwargs["Abonnement"] = abonnement
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_form = forms.UserForm(request.POST, instance=user)
        profile_form = forms.ProfileForm(
            request.POST, request.FILES, instance=user.profile
        )
        if not (user_form.is_valid() and profile_form.is_valid()):
            messages.warning(
                request,
                "Erreur de soumission ! Veuillez verifier les renseignements.",
            )
            user_form = forms.UserForm(instance=user)
            profile_form = forms.ProfileForm(instance=user.profile)
            return super().get(request, user_form=user_form, profile_form=profile_form)
        # Both forms are fine. Time to save!
        user_form.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        messages.success(request, "Profil modifié!")
        return redirect("profiles:show_self")

class VueInfosPerso(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/infosperso.html"
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        verif_delai()
        user = self.request.user
        if "user_form" not in kwargs:
            kwargs["user_form"] = forms.UserForm(instance=user)
        if "profile_form" not in kwargs:
            kwargs["profile_form"] = forms.InfoPersoForm(instance=user.profile)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_form = forms.UserForm(request.POST, instance=user)
        profile_form = forms.InfoPersoForm(
            request.POST, request.FILES, instance=user.profile
        )
        if not (user_form.is_valid() and profile_form.is_valid()):
            messages.warning(
                request,
                "Echec de validadation ! Revoyez les details s'il vous plait.",
            )
            user_form = forms.UserForm(instance=user)
            profile_form = forms.InfoPersoForm(instance=user.profile)
            return super().get(request, user_form=user_form, profile_form=profile_form)
        # Both forms are fine. Time to save!
        user_form.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()

        messages.success(request, "Félicitation {}! vous avez validé toutes les étapes de l'inscription. Vous devez payer votre abonnement mensuel de 47€ pour pouvoir apporter et recevoir de l'aide  !".format(profile.user.name))
        return redirect("comptes:login")
#
#Apporter de l'aide
class VueAider(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/aider.html"
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        verif_delai()
        user = self.request.user
        if "Aide_form" not in kwargs:
            kwargs["Aide_form"] = forms.AiderForm(instance=user.profile.user)
        
        try:
            abonnement = models.Souscriptions.objects.get(utilisateur=user.profile)
        except models.Souscriptions.DoesNotExist:
            abonnement = None

        kwargs["show_user"] = user
        kwargs["Abonnement"] = abonnement
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        Aide_form = forms.AiderForm(request.POST)
        if not (Aide_form.is_valid()):
            messages.warning(
                request,
                "Erreur de soumission ! Veuillez verifier les renseignements.",
            )
            return redirect("profiles:aider")
        # Both forms are fine. Time to save!
        aide = Aide_form.save(commit=False)
        aide.emetteur = user.profile
        aide.save()
        messages.success(request, "Votre intention a bien été prise en compte! Veuillez patienter le temps que vous soyez fusionné avec un ou plusieurs membres de la communauté.")
        return redirect("profiles:show_self")


#Liste d'envoi
class VueListeEnvoi(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/listenvoi.html"
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        verif_delai()
        user = self.request.user
        try:
            abonnement = models.Souscriptions.objects.get(utilisateur=user.profile)
        except models.Souscriptions.DoesNotExist:
            abonnement = None

        liste = models.ApporterAide.objects.filter(emetteur=user.profile, activTransact=True, etatDapport=False).values("id","dateDeSoumission","montantApporte","recepteur", "dateLimiteEnvoi","etatDapport","etatDeReception").order_by('-dateDeSoumission')       
        kwargs["show_user"] = user
        kwargs["Abonnement"] = abonnement
        kwargs["liste_actions"] = liste
        return super().get(request, *args, **kwargs)

#Confirmation d'envoi
class VueConfirmerEnvoi(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/confirmenvoi.html"
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        verif_delai()
        user = self.request.user
        if "Envoi_form" not in kwargs:
            kwargs["Envoi_form"] = forms.ConfirmeEnvoiForm(instance=user.profile.user)
        try:
            abonnement = models.Souscriptions.objects.get(utilisateur=user.profile)
        except models.Souscriptions.DoesNotExist:
            abonnement = None

        liste = models.ApporterAide.objects.filter(emetteur=user.profile, etatDapport=False, activTransact=True, id=kwargs["Id"]).values("id","dateDeSoumission","montantApporte","recepteur","etatDapport","etatDeReception").order_by('-dateDeSoumission')       
        
        kwargs["show_user"] = user
        kwargs["Abonnement"] = abonnement
        kwargs["liste_actions"] = liste
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        user = self.request.user
        Envoi_form = forms.ConfirmeEnvoiForm(request.POST, request.FILES)
        if not (Envoi_form.is_valid()):
            messages.warning(
                request,
                "Erreur de soumission ! Veuillez verifier les renseignements.",
            )
            Envoi_form = forms.ConfirmeEnvoiForm(instance=user.profile)
            return super().get(request,Envoi_form=Envoi_form)
        
        Envoi = Envoi_form.save(commit=False)
        occurance= models.ApporterAide.objects.get(id=kwargs["Id"])
        Envoi.id= occurance.id
        Envoi.emetteur= occurance.emetteur
        Envoi.dateDeSoumission= occurance.dateDeSoumission
        Envoi.montantApporte = occurance.montantApporte
        Envoi.recepteur= occurance.recepteur
        Envoi.activTransact= occurance.activTransact
        Envoi.etatDapport= True
        Envoi.dateDeValidation= datetime.now()
        Envoi.dateLimiteEnvoi = occurance.dateLimiteEnvoi
        Envoi.dateLimiteReception = Envoi.dateDeValidation + timedelta(days=1)
        Envoi.etatDeReception= occurance.etatDeReception
        Envoi.save()

        messages.success(request, "Confirmation éffectuée ! Veuillez contacter le bénéficiare pour qu'il confirme la reception.")
        return redirect("profiles:ListeEnvoi")

#Liste de reception
class VueListeReception(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/listreception.html"
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        verif_delai()
        user = self.request.user
        if "Recu_form" not in kwargs:
            kwargs["Recu_form"] = forms.ConfirmeReceptionForm(instance=user.profile.user)
        if "Besoin_form" not in kwargs:
            kwargs["Besoin_form"] = forms.BesoinForm()
        try:
            abonnement = models.Souscriptions.objects.get(utilisateur=user.profile)
        except models.Souscriptions.DoesNotExist:
            abonnement = None

        liste = models.ApporterAide.objects.filter(recepteur=user.profile, etatDeReception=False, activTransact=True).values("id","dateDeValidation","emetteur","montantApporte", "dateLimiteReception","etatDapport","etatDeReception").order_by('-dateDeValidation')

        kwargs["show_user"] = user
        kwargs["Abonnement"] = abonnement
        kwargs["liste_actions"] = liste
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        occurance= get_object_or_404(models.ApporterAide, id=kwargs["Id"])
        Recu_form = forms.ConfirmeReceptionForm(request.POST)
        Besoin_form = forms.BesoinForm(request.POST, instance=occurance.emetteur)
        if not (Recu_form.is_valid() and Besoin_form.is_valid()):
            messages.warning(
                request,
                "Erreur de soumission ! Veuillez verifier les renseignements.",
            )
            Recu_form = forms.ConfirmeReceptionForm(instance=user.profile)
            Besoin_form = forms.BesoinForm(request.POST, instance=occurance.emetteur)
            return super().get(request,Recu_form=Recu_form, Besoin_form=Besoin_form)

        #"""______________________Mises à jour concernant l'emetteur________________ """
        try:
            #Ajout de l'envoyeur dans les besoins
            besoin = models.BesoinsEmis()
            besoin.utilisateur = occurance.emetteur
            besoin.idAide = occurance.id
            besoin.dateDeDemande = datetime.now()
            besoin.montantDuBesoin = 2*(occurance.montantApporte)
            besoin.restant = 2*(occurance.montantApporte)
            besoin.paye = 0
            besoin.save()
            benefice = models.Benefices()
            benefice.utilisateur = occurance.emetteur
            benefice.montantBenefice = 2*(occurance.montantApporte)
            benefice.save()
            #Marquer comme en attente d'aide avec son montant
            emis = Besoin_form.save(commit=False)
            emis.besoin = True
            try:
                benef = models.Benefices.objects.filter(utilisateur=occurance.emetteur).order_by('dateBenefice')[0]
                emis.montant = benef.montantBenefice
            except:
                emis.montant = 2*(occurance.montantApporte)
            emis.save()
        except models.Profile.DoesNotExist:
            messages.warning(request, "Erreur d'enregistrement ! Cet utilisateur a déja un besoin insatisfait")
            return redirect("profiles:show_self")
        #"""______________________fin des mise à jour_________________________________"""

        #Besoin satisfait
        try:
            besoinSat = models.BesoinsEmis.objects.filter(utilisateur=user.profile, etatDuBesoin=False).order_by('dateDeDemande')[0]
            prof = models.Profile.objects.get(user=occurance.recepteur.user)
            besoinSat.paye += occurance.montantApporte
            besoinSat.restant -= occurance.montantApporte
            if besoinSat.restant == 0:
                besoinSat.etatDuBesoin = True
                try:
                    models.Benefices.objects.filter(utilisateur=besoinSat.utilisateur, montantBenefice=besoinSat.montantDuBesoin).order_by('dateBenefice')[0].delete()
                    benef = models.Benefices.objects.filter(utilisateur=besoinSat.utilisateur).order_by('dateBenefice')[0]
                    prof.besoin = True
                    prof.montant = benef.montantBenefice
                except:
                    prof.besoin = False
                    prof.montant = 0
            elif besoinSat.restant < 0:
                messages.warning(request, "Erreur d'enregistrement ! Veuillez contacter l'administrateur.")
                return redirect("profiles:show_self")

            besoinSat.save(update_fields=['etatDuBesoin', 'paye', 'restant'])
            #desactive besoin chez le recepteur
            prof.save(update_fields=['besoin', 'montant'])
            Recu = Recu_form.save(commit=False)
            #Enregistrement de la confirmation
            Recu.id= occurance.id
            Recu.emetteur= occurance.emetteur
            Recu.dateDeSoumission= occurance.dateDeSoumission
            Recu.montantApporte= occurance.montantApporte
            Recu.recepteur= occurance.recepteur
            Recu.activTransact= occurance.activTransact
            Recu.etatDapport= occurance.etatDapport
            Recu.dateDeValidation= occurance.dateDeValidation
            Recu.fichierJoint= occurance.fichierJoint
            Recu.etatDeReception= True
            Recu.save()
        except models.BesoinsEmis.DoesNotExist:
            messages.warning(request, "Erreur d'enregistrement !  Veuillez contacter l'administrateur.")
            return redirect("profiles:show_self")
        
        messages.success(request, "Reception confirmée ! Apportez de l'aide pour  en bénéficier davantage.")
        return redirect("profiles:ListeReception")

#Vue des receptions
class VueHistoriqueRecu(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/listrecu.html"
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        verif_delai()
        user = self.request.user
        if "Recu_form" not in kwargs:
            kwargs["Recu_form"] = forms.ConfirmeReceptionForm(instance=user.profile.user)
        try:
            abonnement = models.Souscriptions.objects.get(utilisateur=user.profile)
        except models.Souscriptions.DoesNotExist:
            abonnement = None

        liste = models.ApporterAide.objects.filter(recepteur=user.profile, etatDapport=True, etatDeReception=True).values("id","dateDeValidation","emetteur","montantApporte","etatDapport","etatDeReception").order_by('-dateDeValidation')

        kwargs["show_user"] = user
        kwargs["Abonnement"] = abonnement
        kwargs["liste_actions"] = liste
        return super().get(request, *args, **kwargs)

#Vue des aides apportes
class VueHistoriqueEnvoi(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/listenvoye.html"
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        verif_delai()
        user = self.request.user
        if "Recu_form" not in kwargs:
            kwargs["Recu_form"] = forms.ConfirmeReceptionForm(instance=user.profile.user)
        
        try:    
            abonnement = models.Souscriptions.objects.get(utilisateur=user.profile)
        except models.Souscriptions.DoesNotExist:
            abonnement = None
        liste = models.ApporterAide.objects.filter(emetteur=user.profile, etatDapport=True).values("id","dateDeValidation","recepteur","montantApporte","etatDapport","etatDeReception").order_by('-dateDeValidation')

        kwargs["show_user"] = user
        kwargs["Abonnement"] = abonnement
        kwargs["liste_actions"] = liste
        return super().get(request, *args, **kwargs)

class VuePaypal(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/paypal.html"
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        verif_delai()
        user = self.request.user

        if user == self.request.user:
            kwargs["editable"] = True
        try:    
            abonnement = models.Souscriptions.objects.get(utilisateur=user.profile)
        except models.Souscriptions.DoesNotExist:
            abonnement = None

        kwargs["show_user"] = user
        kwargs["Abonnement"] = abonnement

        return super().get(request, *args, **kwargs)