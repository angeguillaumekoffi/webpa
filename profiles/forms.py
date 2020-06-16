from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(Field("name", type='hidden'))

    class Meta:
        model = User
        fields = ["name"]


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field("picture"),
            Field("bio"),
            Field("pays"),
            Field("contact"),
            
            Submit("update", "Update", css_class="btn-success"),
        )

    class Meta:
        model = models.Profile
        fields = ["picture", "nomComplet", "bio", "pays", "contact"]

class ImgForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field("picture"),
            Submit("update", "Valider", css_class="btn-warning"),
        )
    class Meta:
        model = models.Profile
        fields = ["picture"]

class InfoPersoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        #self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.fields['nomComplet'].required = True
        self.fields['pays'].required = True
        self.fields['contact'].required = True
        self.helper.layout = Layout(
            Field("picture"),
            Field("nomComplet"),
            Field("bio"),
            Field("pays"),
            Field("contact"),
            
            Submit("update", "Terminer", css_class="btn-success"),
        )

    class Meta:
        model = models.Profile
        fields = ["picture", "nomComplet", "bio", "pays", "contact"]

class AiderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = "formulaire"
        self.helper.form_method = 'post'
        self.fields['montantApporte'].required = True
        self.helper.layout = Layout(
            Field("montantApporte"),
            Button("update", "Envoyer", css_class="btn-success", onclick='Confirmer("Voulez vous vraiment apporter une aide ?")'),
        )
    class Meta:
        model = models.ApporterAide
        fields = ["montantApporte"]

class BesoinForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = "formulaire"
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field("besoin", type='hidden'),
            Field("montant", type='hidden'),
        )
    class Meta:
        model = models.Profile
        fields = ["besoin", "montant"]
    
class ConfirmeReceptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = "formulaire"
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field("etatDeReception", type="hidden"),
            #Button("bouton", "Confirmer", css_class="btn-danger btn-sm", onclick='ConfirmerSpec("{{ ligne.id }}")'),
        )
    class Meta:
        model = models.ApporterAide
        fields = ["etatDeReception"]

class ConfirmeEnvoiForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = "formulaire"
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field("fichierJoint"),
            
            Button("update", "Confirmer", css_class="btn-success", onclick='Confirmer("Confirmez vous avoir transféré cette somme ?")'),
        )

    class Meta:
        model = models.ApporterAide
        fields = ["fichierJoint"]