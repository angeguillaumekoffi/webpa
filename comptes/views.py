from __future__ import unicode_literals

from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib import messages
from authtools import views as authviews
from braces import views as bracesviews
from django.conf import settings
from . import forms

User = get_user_model()


class LoginView(bracesviews.AnonymousRequiredMixin, authviews.LoginView):
    template_name = "comptes/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        redirect = super().form_valid(form)
        remember_me = form.cleaned_data.get("remember_me")
        if remember_me is True:
            ONE_MONTH = 30 * 24 * 60 * 60
            expiry = getattr(settings, "KEEP_LOGGED_DURATION", ONE_MONTH)
            self.request.session.set_expiry(expiry)
        return redirect


class LogoutView(authviews.LogoutView):
    url = reverse_lazy("home")


class SignUpView(
    bracesviews.AnonymousRequiredMixin,
    bracesviews.FormValidMessageMixin,
    generic.CreateView,
):
    form_class = forms.SignupForm
    model = User
    template_name = "comptes/signup.html"
    success_url = reverse_lazy("profiles:infosPerso")
    form_valid_message = "Vous avez fini la première étape. Veuillez completer vos informations personnelles pour terminer l'inscription"

    def form_valid(self, form):
        r = super().form_valid(form)
        username = form.cleaned_data["email"]
        password = form.cleaned_data["password1"]
        user = auth.authenticate(email=username, password=password)
        auth.login(self.request, user)
        return r


class PasswordChangeView(authviews.PasswordChangeView):
    form_class = forms.PasswordChangeForm
    template_name = "comptes/password-change.html"
    success_url = reverse_lazy("comptes:logout")

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "Votre mot de passe a été changé, "
            "Vous êtes déconnecté. Veuillez vous reconnecter svp",
        )

        return super().form_valid(form)


class PasswordResetView(authviews.PasswordResetView):
    form_class = forms.PasswordResetForm
    template_name = "comptes/password-reset.html"
    success_url = reverse_lazy("comptes:password-reset-done")
    subject_template_name = "comptes/emails/password-reset-subject.txt"
    email_template_name = "comptes/emails/password-reset-email.html"


class PasswordResetDoneView(authviews.PasswordResetDoneView):
    template_name = "comptes/password-reset-done.html"


class PasswordResetConfirmView(authviews.PasswordResetConfirmAndLoginView):
    template_name = "comptes/password-reset-confirm.html"
    form_class = forms.SetPasswordForm
