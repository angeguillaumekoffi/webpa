from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
import uuid
from django.db import models
from django.conf import settings
from datetime import datetime, timedelta

paysTuple = [
    ("South Africa", "South Africa"),
    ("Algérie", "Algérie"),
    ("Allemagne", "Allemagne"),
    ("Australia", "Australia"),
    ("Angola", "Angola"),
    ("Belgique", "Belgique"),
    ("Benin", "Benin"),
    ("Botswana", "Botswana"),
    ("Brazilia", "Brazilia"),
    ("Burkina Faso", "Burkina Faso"),
    ("Canada", "Canada"),
    ("Cameroun", "Cameroun"),
    ("RD Congo", "RD Congo"),
    ("Côte d'Ivoire", "Côte d'Ivoire"),
    ("Damemark", "Damemark"),
    ("Finland", "Finland"),
    ("France", "France"),
    ("Gabon", "Gabon"),
    ("Gambie", "Gambie"),
    ("Ghana", "Ghana"),
    ("Guinéé", "Guinéé"),
    ("Israel", "Israel"),
    ("Mali", "Mali"),
    ("Maroc", "Maroc"),
    ("Nigeria", "Nigeria"),
    ("Niger", "Niger"),
    ("Togo", "Togo"),
    ("Tunisia", "Tunisia"),
    ("USA", "USA"),
]

PaiementTuple = [
    ("Mobile money", "Mobile money"),
    ("Paypal", "Paypal"),
]

MontantAide = [
    (25000, "25.000 XOF"),
    (50000, "50.000 XOF"),
    (100000, "100.000 XOF"),
    (200000, "200.000 XOF"),
    (250000, "250.000 XOF"),
    (400000, "400.000 XOF"),
    (500000, "500.000 XOF"),
]

dateActuelle = datetime.now()
dateDexp = dateActuelle + timedelta(days=30)


def enregistrePhoto(instance, filename):
    return 'profils/utilisateur_{0}/{1}'.format(instance.user.name, filename)

def pieceJointe(instance, filename):
    return 'fichiers-joints/utilisateur_{0}/{1}'.format(instance.emetteur.user.name, filename)

class BaseProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    slug = models.UUIDField(default=uuid.uuid4, blank=True, editable=False)
    # Add more user profile fields here. Make sure they are nullable
    # or with default values
    picture = models.ImageField("Photo de profil", upload_to=enregistrePhoto, null=True, blank=True)
    bio = models.CharField("Bio", max_length=200, blank=True, null=True)
    email_verified = models.BooleanField("Email verifié", default=False)
    pays = models.CharField(max_length=25, default="South Africa", choices=paysTuple, verbose_name="Pays", blank=True, null=False)
    contact = models.CharField(verbose_name="Téléphone", unique=True, max_length=12,   blank=True, null=True)
    nomComplet = models.CharField(blank=True, null=True, unique=True, max_length=100, default="", verbose_name='Nom et Prenoms')
    besoin = models.BooleanField("Besoin", default=False)
    montant = models.IntegerField(verbose_name="Montant du besoin",blank=True, null=True)
    
    class Meta:
        abstract = True


@python_2_unicode_compatible
class Profile(BaseProfile):
    def __str__(self):
        return "{} ({} XOF)".format(self.user.name, self.montant)

class Benefices(models.Model):
    utilisateur = models.ForeignKey(Profile, verbose_name="Utilisateur", on_delete=models.CASCADE, blank=True)
    montantBenefice = models.IntegerField(verbose_name="Montant du bénéfice",blank=True, null=True)
    dateBenefice = models.DateTimeField(verbose_name="date", auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return "{0} ({1})".format(self.utilisateur.user.name, self.dateBenefice)

    class Meta:
        db_table = 'benefices'
        managed = True
        verbose_name = 'benefices'
        verbose_name_plural = 'benefices'

class Souscriptions(models.Model):
    utilisateur = models.ForeignKey(Profile, verbose_name="Utilisateur", on_delete=models.CASCADE, blank=True)
    dateDeSousrcription = models.DateTimeField(verbose_name="souscrit le", auto_now=True, auto_now_add=False)
    dateDexpiration = models.DateTimeField(verbose_name="Expire le", default=dateDexp, auto_now=False, auto_now_add=False)
    moyenDePaiment = models.CharField(verbose_name="Moyen de paiement", default="Paypal", choices=PaiementTuple, max_length=20, blank=True, null=False)
    statutCompte = models.BooleanField("Compte actif", default=False)
    
    def __str__(self):
        return "Souscripteur : {0} | Date de paiement : {1} | Expire le : {2}".format(self.utilisateur, self.dateDeSousrcription, self.dateDexpiration)

    class Meta:
        db_table = 'souscriptions'
        managed = True
        verbose_name = 'Souscriptions'
        verbose_name_plural = 'Souscriptions'

class BesoinsEmis(models.Model):
    utilisateur = models.ForeignKey(Profile, verbose_name="Utilisateur", on_delete=models.CASCADE, blank=True)
    idAide = models.SlugField(verbose_name="Ref aide", unique=True, blank=True, null=True)
    dateDeDemande = models.DateTimeField(verbose_name="Date d'emission", auto_now=True, auto_now_add=False)
    montantDuBesoin = models.IntegerField(verbose_name="Montant du besoin",blank=True, null=True)
    paye = models.IntegerField(verbose_name="Payé",blank=True, null=True)
    restant = models.IntegerField(verbose_name="Restant",blank=True, null=True)
    etatDuBesoin = models.BooleanField(verbose_name="Satisfait", default=False)

    def __str__(self):
        return "{}".format(self.utilisateur.user.name)

    class Meta:
        db_table = 'besoins_emis'
        managed = True
        verbose_name = 'Besoin émis'
        verbose_name_plural = 'Besoins émis'

class ApporterAide(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emetteur = models.ForeignKey(Profile, verbose_name="Emetteur", on_delete=models.CASCADE, blank=True, null=True)
    dateDeSoumission = models.DateTimeField(verbose_name="Date de soumission", auto_now=True, auto_now_add=False)
    montantApporte = models.IntegerField(verbose_name="Montant Apporté", choices=MontantAide, blank=True, null=True)
    recepteur = models.ForeignKey(Profile, limit_choices_to={'besoin':True}, related_name="Récepteur", verbose_name="Récepteur", on_delete=models.CASCADE, blank=True, null=True)
    #Etat de la transaction
    activTransact = models.BooleanField(verbose_name="Valide", default=False)
    etatDapport = models.BooleanField(verbose_name="Depot effectué", default=False)
    etatDeReception = models.BooleanField(verbose_name="Reception confirmée", default=False)
    #champs suplementaires pour la validation du paiement
    dateLimiteEnvoi = models.DateTimeField(verbose_name="Date butoire envoi", auto_now=False, auto_now_add=False, null=True, blank=True)
    dateLimiteReception = models.DateTimeField(verbose_name="Date butoire reception", auto_now=False, auto_now_add=False, null=True, blank=True)
    dateDeValidation = models.DateTimeField(verbose_name="Depot effectué le", auto_now=False, auto_now_add=False, null=True, blank=True)
    fichierJoint = models.ImageField("Fichier joint", upload_to=pieceJointe, null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.emetteur, self.recepteur)

    class Meta:
        db_table = 'apport_aide'
        managed = True
        verbose_name = "Apport d'aide"
        verbose_name_plural = "Apports d'aide"
