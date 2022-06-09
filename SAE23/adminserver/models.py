import django.utils.timezone
from django.db import models

# Create your models here.

class type_de_serveurs(models.Model):
    type = models.CharField(max_length=100)
    description = models.TextField(null=True)

    def __str__(self):
        return self.type

    def dico(self):
        return {"type": self.type,"description":self.description}

class serveurs(models.Model):
    nom = models.CharField(max_length=100,blank=False)
    type_de_serveur = models.ForeignKey(type_de_serveurs, on_delete=models.CASCADE, null="true")
    processeurs = models.IntegerField(blank=False)
    memoire = models.IntegerField(blank=False)
    stockage = models.IntegerField(blank=False)

    def __str__(self):
        return self.nom

    def dico(self):
        return {"nom": self.nom,"type_de_serveur":self.type_de_serveur,"processeurs":self.processeurs,"memoire":self.memoire,"stockage":self.stockage}

class utilisateurs(models.Model):
    nom = models.CharField(max_length=100,blank=False)
    prenom = models.CharField(max_length=100,blank=False)
    email = models.EmailField(blank=False, null=True)

    def __str__(self):
        return self.email

    def dico(self):
        return {"nom": self.nom,"prenom":self.prenom,"email":self.email}


class services(models.Model):
    nom_service = models.CharField(max_length=100,blank=False)
    date_de_lancement = models.DateField(max_length=100,blank=False,default=django.utils.timezone.now)
    espace_memoire_utilise = models.IntegerField(blank=False)
    memoire_vive_necessaire = models.IntegerField(blank=False)
    serveur_de_lancement = models.ForeignKey(serveurs, on_delete=models.CASCADE, null="true")

    def __str__(self):
        return self.nom_service

    def dico(self):
        return {"nom_service":self.nom_service,"date_de_lancement":self.date_de_lancement,"espace_memoire_utilise":self.espace_memoire_utilise,"memoire_vive_necessaire":self.memoire_vive_necessaire,"serveur_de_lancement":self.serveur_de_lancement}

class applications(models.Model):
    nom_application = models.CharField(max_length=100,blank=False)
    logo = models.ImageField(upload_to='images')
    serveurs = models.ManyToManyField(serveurs)
    utilisateurs = models.ForeignKey(utilisateurs, on_delete=models.CASCADE, null="true")
    espace_memoire_utilise = models.IntegerField(blank=False)
    memoire_vive_necessaire = models.IntegerField(blank=False)
    services_utilises = models.ManyToManyField(services)

    def __str__(self):
        return self.nom_application

    def dico(self):
        return {"nom_application":self.nom_application,"logo":self.logo,"serveurs":self.serveurs,"utilisateurs":self.utilisateurs}