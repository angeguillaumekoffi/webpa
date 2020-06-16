from django.urls import path
from . import views

app_name = "profiles"
urlpatterns = [
    path("moi/", views.ShowProfile.as_view(), name="show_self"),
    path("moi/modifier/", views.EditProfile.as_view(), name="edit_self"),
    path("moi/aider", views.VueAider.as_view(), name="aider"),
    path("moi/liste/envoi/", views.VueListeEnvoi.as_view(), name="ListeEnvoi"),
    path("moi/liste/envoi/confirmation/<slug:Id>/", views.VueConfirmerEnvoi.as_view(), name="ConfirmeEnvoi"),
    path("moi/liste/envoyes/", views.VueHistoriqueEnvoi.as_view(), name="HEnvoye"),
    path("moi/liste/reception/", views.VueListeReception.as_view(), name="ListeReception"),
    path("moi/liste/reception/confirmation/<slug:Id>/", views.VueListeReception.as_view(), name="ConfirmeReception"),
    path("moi/liste/montantrecu/", views.VueHistoriqueRecu.as_view(), name="MRecu"),
    path("moi/inscription/informations/", views.VueInfosPerso.as_view(), name="infosPerso"),
    path("myaccount/suscribe/paypal", views.VuePaypal.as_view(), name="paypal"),
    path("<slug:slug>/", views.ShowProfile.as_view(), name="show"),
]
