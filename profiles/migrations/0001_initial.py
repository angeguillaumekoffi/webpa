# Generated by Django 2.2 on 2020-06-05 02:15

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import profiles.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authtools', '0003_auto_20160128_0912'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('slug', models.UUIDField(blank=True, default=uuid.uuid4, editable=False)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=profiles.models.enregistrePhoto, verbose_name='Photo de profil')),
                ('bio', models.CharField(blank=True, max_length=200, null=True, verbose_name='Bio')),
                ('email_verified', models.BooleanField(default=False, verbose_name='Email verifié')),
                ('pays', models.CharField(blank=True, choices=[('Afrique du sud', 'Afrique du sud'), ('Algérie', 'Algérie'), ('Allemagne', 'Allemagne'), ('Australie', 'Australie'), ('Angola', 'Angola'), ('Belgique', 'Belgique'), ('Botswana', 'Botswana'), ('Brazil', 'Brazil'), ('Burkina Faso', 'Burkina Faso'), ('Canada', 'Canada'), ('Cameroun', 'Cameroun'), ('Congo RDC', 'Congo RDC'), ("Côte d'Ivoire", "Côte d'Ivoire"), ('Damemark', 'Damemark'), ('Finland', 'Finland'), ('France', 'France'), ('Gabon', 'Gabon'), ('Gambie', 'Gambie'), ('Ghana', 'Ghana'), ('Guinéé', 'Guinéé'), ('Mali', 'Mali'), ('Inde', 'Inde'), ('Ireland', 'Ireland'), ('Israel', 'Israel')], default="Côte d'Ivoire", max_length=25, verbose_name='Pays')),
                ('contact', models.CharField(blank=True, max_length=12, null=True, verbose_name='Tel/Cel')),
                ('nomComplet', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Nom et Prenoms')),
                ('statutCompte', models.BooleanField(default=False, verbose_name='Compte actif')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Souscriptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateDeSousrcription', models.DateTimeField(auto_now=True, verbose_name='souscrit le')),
                ('dateDexpiration', models.DateTimeField(default=datetime.datetime(2020, 7, 5, 2, 15, 17, 932761), verbose_name='Expire le')),
                ('moyenDePaiment', models.CharField(blank=True, choices=[('Mobile money', 'Mobile money'), ('Paypal', 'Paypal')], default='Mobile money', max_length=20, verbose_name='Moyen de paiement')),
                ('statutCompte', models.BooleanField(default=True, verbose_name='Compte actif')),
                ('utilisateur', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.Profile', verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': 'Souscriptions',
                'verbose_name_plural': 'Souscriptions',
                'db_table': 'souscriptions',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BesoinsEmis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idAide', models.IntegerField(blank=True, null=True, unique=True, verbose_name='Ref aide')),
                ('dateDeDemande', models.DateTimeField(auto_now=True, verbose_name="Date d'emission")),
                ('montantDuBesoin', models.IntegerField(blank=True, null=True, verbose_name='Montant du besoin')),
                ('etatDuBesoin', models.BooleanField(default=False, verbose_name='Satisfait')),
                ('utilisateur', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.Profile', verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': 'Besoin émis',
                'verbose_name_plural': 'Besoins émis',
                'db_table': 'besoins_emis',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ApporterAide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateDeSoumission', models.DateTimeField(auto_now=True, verbose_name='Date de soumission')),
                ('montantApporte', models.IntegerField(blank=True, choices=[(25000, '25.000 XOF'), (50000, '50.000 XOF'), (100000, '10.0000 XOF'), (200000, '20.0000 XOF'), (250000, '250.000 XOF'), (400000, '400.000 XOF'), (500000, '500.000 XOF')], null=True, verbose_name='Montant Apporté')),
                ('activTransact', models.BooleanField(default=False, verbose_name='Valide')),
                ('etatDapport', models.BooleanField(default=False, verbose_name='Depot effectué')),
                ('etatDeReception', models.BooleanField(default=False, verbose_name='Reception confirmée')),
                ('dateDeValidation', models.DateTimeField(blank=True, null=True, verbose_name='Depot effectué le')),
                ('fichierJoint', models.ImageField(blank=True, null=True, upload_to=profiles.models.pieceJointe, verbose_name='Fichier joint')),
                ('emetteur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.Profile', verbose_name='Emetteur')),
                ('recepteur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Récepteur', to='profiles.Profile', verbose_name='Récepteur')),
            ],
            options={
                'verbose_name': "Apport d'aide",
                'verbose_name_plural': "Apports d'aide",
                'db_table': 'apport_aide',
                'managed': True,
            },
        ),
    ]
