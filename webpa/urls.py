from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.urls import include, path
import profiles.urls
import comptes.urls
import Infos.urls
from . import views

# Personalized admin site settings like title and header
admin.site.site_title = "Administrateur"
admin.site.site_header = "Administration"

urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("about/", views.AboutPage.as_view(), name="about"),
    path("utilisateur/", include(profiles.urls)),
    path("informations/", include(Infos.urls)),
    path("admin/", admin.site.urls),
    path("", include(comptes.urls)),
] 
#+ staticfiles_urlpatterns()

# User-uploaded files like profile pics need to be served in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Include django debug toolbar if DEBUG is on
#if settings.DEBUG:
#    import debug_toolbar
#
#    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]