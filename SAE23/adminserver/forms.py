from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from . import models

class type_de_serveursForm(ModelForm):
    class Meta:
        model = models.type_de_serveurs
        fields = ('type', 'description')
        labels = {
            'type' : _('Type de serveur:'),
            'description' : _('Description:') ,
        }

class serveursForm(ModelForm):
    class Meta:
        model = models.serveurs
        fields = ('nom','type_de_serveur','processeurs','memoire','stockage')
        labels = {
            'nom' : _('Nom du serveur:'),
            'type_de_serveur' : _('Type du serveur:'),
            'processeurs' : _('Nombre de processeurs:'),
            'memoire' : _('Memoire du serveur (MegaOctets):'),
            'stockage' : _('Espace de stockage du serveur (GigaOctets):'),
        }

class utilisateursForm(ModelForm):
    class Meta:
        model = models.utilisateurs
        fields = ('nom','prenom','email')
        labels = {
            'nom' : _("Nom de l'utilisateur:"),
            'prenom' : _("Prenom de l'utilisateur:"),
            'email' : _("Email de l'utilisateur:"),
        }

class servicesForm(ModelForm):
    class Meta:
        model = models.services
        fields = ('nom_service','date_de_lancement','espace_memoire_utilise','memoire_vive_necessaire','serveur_de_lancement')
        labels = {
            'nom_service' : _('Nom du service:'),
            'date_de_lancement' : _('Date de lancement du service:'),
            'espace_memoire_utilise' : _('Espace memoire utilisee:'),
            'memoire_vive_necessaire' : _('Memoire vive necessaire:'),
            'serveur_de_lancement' : _('Serveur de lancement:'),
        }
        localized_fields = ('date_de_lancement',)

class applicationsForm(ModelForm):
    class Meta:
        model = models.applications
        fields = ('nom_application','logo','serveurs','utilisateurs','memoire_vive_necessaire','services_utilises')
        labels = {
            'nom_application' : _("Nom de l'application:"),
            'logo' : _('Logo:'),
            'serveurs' : _('Serveurs:'),
            'utilisateurs' : _("Utilisateurs de l'application:"),
            'memoire_vive_necessaire' : _('Memoire vive necessaire'),
            'services_utilises' : _('Services utilises'),
        }