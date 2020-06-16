from __future__ import unicode_literals
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field
from authtools import forms as authtoolsforms
from django.contrib.auth import forms as authforms
from django.urls import reverse


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(label="Mémoriser ma session", required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["username"].widget.input_type = "email"  # ugly hack

        self.helper.layout = Layout(
            Field("username", placeholder="Adresse mail", autofocus=""),
            Field("password", placeholder="Mot de passe"),
            HTML(
                '<a href="{}">Mot de passe oublié?</a><br><br>'.format(
                    reverse("comptes:password-reset")
                )
            ),
            Field("remember_me"),
            Submit("sign_in", "Connexion", css_class="btn btn-lg btn-danger btn-block"),
        )


class SignupForm(authtoolsforms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["email"].widget.input_type = "email"  # ugly hack

        self.helper.layout = Layout(
            Field("email", placeholder="Entrer e-mail", autofocus=""),
            Field("name", placeholder="Nom d'utilisateur/pseudo"),
            Field("password1", placeholder="Minimum 8 caractères alphanumériques"),
            Field("password2", placeholder="Identique au précédent"),
            Submit("sign_up", "S'incrire", css_class="btn btn-lg btn-danger btn-block"),
        )


class PasswordChangeForm(authforms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field("old_password", placeholder="Ancien mot de passe", autofocus=""),
            Field("new_password1", placeholder="Nouveau mot de passe"),
            Field("new_password2", placeholder="Nouveau mot de passe (encore)"),
            Submit("pass_change", "Changer", css_class="btn-warning"),
        )


class PasswordResetForm(authtoolsforms.FriendlyPasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field("email", placeholder="Entrez votre adresse email", autofocus=""),
            Submit("pass_reset", "Soumettre", css_class="btn-warning"),
        )


class SetPasswordForm(authforms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field("new_password1", placeholder="Enter new password", autofocus=""),
            Field("new_password2", placeholder="Enter new password (again)"),
            Submit("pass_change", "Change Password", css_class="btn-warning"),
        )
