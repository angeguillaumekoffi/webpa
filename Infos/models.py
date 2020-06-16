from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Informations(models.Model):
    titre = models.CharField("Titre", max_length=256, blank=True, null=True)
    descri = RichTextField("Description", blank=True, null=True)
    class Meta:
        db_table= "Informations"
        managed = True
        verbose_name = "Information"
        verbose_name_plural = "Informations"
    def __str__(self):
        return "{}".format(self.titre)