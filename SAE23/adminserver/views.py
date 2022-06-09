from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import applicationsForm
from .forms import servicesForm
from .forms import utilisateursForm
from .forms import serveursForm
from .forms import type_de_serveursForm

from . import  models
# Create your views here.
def index(request):
    return render(request, 'index.html')

def ajout(request):
    return render(request, 'index_ajout.html')

#CRUD SERVEUR ==========================================================================================================================

def serveurs_index(request):
    URL = "serveur"
    serveurs = list(models.serveurs.objects.all())
    return render(request,"liste_index.html",{"objects" : serveurs,"title":"SERVEURS:","extra":"server_img","url":URL})

def ajout_serveur(request):
    title = "Ajouter un serveur"
    url = "serveur"
    if request.method == "POST":
        form = serveursForm(request.POST)
        if form.is_valid():
            serveur = form.save()
            return HttpResponseRedirect("/adminserver/serveurs")
        else:
            return render(request,"ajout.html",{"form" : form,"url":url,"title":title})
    else:
        form = serveursForm()
        return render(request,"ajout.html",{"form" : form,"url":url,"title":title})

def update_serveur(request, id):
    if request.method == "POST":
        form = serveursForm(request.POST)
        if form.is_valid():
            serveur = form.save(commit=False)
            serveur.id = id
            serveur.save()
            return HttpResponseRedirect("/adminserver/serveurs")
        else:
            return render(request, "update.html", {"form": form, "id": id})
    else:
        serveur = models.serveurs.objects.get(pk=id)
        form = serveursForm(serveur.dico())
        return render(request, "update.html", {"form": form,"id":id})

def delete_serveur(request, id):
    serveur = models.serveurs.objects.get(pk=id)
    serveur.delete()
    return HttpResponseRedirect("/adminserver/servers")

def affiche_serveur(request, id):
    serveur = models.serveurs.objects.get(pk=id)
    return render(request,"serveur/affiche.html",{"serveurs" : serveur})


#CRUD TYPE-SERVEUR ==========================================================================================================================
def typesServeurs_index(request):
    URL = "typeServeur"
    typesServeurs = list(models.type_de_serveurs.objects.all())
    return render(request,"liste_index.html",{"objects" : typesServeurs,"title":"TYPES DE SERVEURS:","extra":"","url":URL})

def ajout_typeserveur(request):
    title = "Ajouter un type de serveur"
    url = "typeServeur"
    if request.method == "POST":
        form = type_de_serveursForm(request.POST)
        if form.is_valid():
            type_serveur = form.save()
            return HttpResponseRedirect("/adminserver/")
        else:
            return render(request,"ajout.html",{"form" : form,"url":url,"title":title})
    else:
        form = type_de_serveursForm()
        return render(request,"ajout.html",{"form" : form,"url":url,"title":title})

def update_typeserveur(request, id):
    if request.method == "POST":
        form = type_de_serveursForm(request.POST)
        if form.is_valid():
            type_serveur = form.save(commit=False)
            type_serveur.id = id
            type_serveur.save()
            return HttpResponseRedirect("/adminserver/typesServeurs")
        else:
            return render(request, "update.html", {"form": form, "id": id})
    else:
        type_serveur = models.type_de_serveurs.objects.get(pk=id)
        form = serveursForm(type_serveur.dico())
        return render(request, "update.html", {"form": form,"id":id})

def delete_typeserveur(request, id):
    type_serveur = models.type_de_serveurs.objects.get(pk=id)
    type_serveur.delete()
    return HttpResponseRedirect("/adminserver/typesServeurs")

def affiche_typeserveur(request, id):
    typeServeur = models.type_de_serveurs.objects.get(pk=id)
    return render(request,"type_serveur/affiche.html",{"typeServeur" : typeServeur})

#CRUD SERVICE ==========================================================================================================================

def services_index(request):
    URL = "service"
    services = list(models.services.objects.all())
    return render(request,"liste_index.html",{"objects" : services,"title":"SERVICES:","extra":"","url":URL})

def ajout_service(request):
    title = "Ajouter un service"
    url = "service"
    if request.method == "POST":
        form = servicesForm(request.POST)
        if form.is_valid():
            service = form.save()
            return HttpResponseRedirect("/adminserver/")
        else:
            return render(request,"ajout.html",{"form" : form,"url":url,"title":title})
    else:
        form = servicesForm()
        return render(request,"ajout.html",{"form" : form,"url":url,"title":title})

def update_service(request, id):
    if request.method == "POST":
        form = servicesForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.id = id
            service.save()
            return HttpResponseRedirect("/adminserver/services")
        else:
            return render(request, "update.html", {"form": form, "id": id})
    else:
        service = models.services.objects.get(pk=id)
        form = servicesForm(service.dico())
        return render(request, "update.html", {"form": form,"id":id})

def delete_service(request, id):
    service = models.services.objects.get(pk=id)
    service.delete()
    return HttpResponseRedirect("/adminserver/services")

def affiche_service(request, id):
    service = models.services.objects.get(pk=id)
    return render(request,"services/affiche.html",{"service" : service})

#CRUD APPLICATION ==========================================================================================================================

def applications_index(request):
    URL = "application"
    applications = list(models.applications.objects.all())
    return render(request,"liste_index.html",{"objects" : applications,"title":"APPLICATIONS:","extra":"","url":URL})

def ajout_application(request):
    title = "Ajouter une application"
    url = "application"
    if request.method == "POST":
        form = applicationsForm(request.POST,request.FILES)
        if form.is_valid():
            application = form.save()
            return HttpResponseRedirect("/adminserver/")
        else:
            return render(request,"ajout.html",{"form" : form,"url":url,"title":title})
    else:
        form = applicationsForm()
        return render(request,"ajout.html",{"form" : form,"url":url,"title":title})

def update_application(request, id):
    if request.method == "POST":
        form = applicationsForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.id = id
            application.save()
            return HttpResponseRedirect("/adminserver/applications")
        else:
            return render(request, "update.html", {"form": form, "id": id})
    else:
        serveur = models.applications.objects.get(pk=id)
        form = applicationsForm(serveur.dico())
        return render(request, "update.html", {"form": form,"id":id})

def delete_application(request, id):
    application = models.applications.objects.get(pk=id)
    application.delete()
    return HttpResponseRedirect("/adminserver/applications")

def affiche_application(request, id):
    application = models.applications.objects.get(pk=id)
    return render(request,"application/affiche.html",{"application" : application})

#CRUD UTILISATEUR ==========================================================================================================================

def utilisateurs_index(request):
    URL = "utilisateur"
    utilisateurs = list(models.utilisateurs.objects.all())
    return render(request,"liste_index.html",{"objects" : utilisateurs,"title":"UTILISATEURS:","extra":"","url":URL})

def ajout_utilisateur(request):
    title = "Ajouter un utilisateur"
    url = "utilisateur"
    if request.method == "POST":
        form = utilisateursForm(request.POST)
        if form.is_valid():
            utilisateur = form.save()
            return HttpResponseRedirect("/adminserver/")
        else:
            return render(request,"ajout.html",{"form" : form,"url":url,"title":title})
    else:
        form = utilisateursForm()
        return render(request,"ajout.html",{"form" : form,"url":url,"title":title})

def update_utilisateur(request, id):
    if request.method == "POST":
        form = utilisateursForm(request.POST)
        if form.is_valid():
            utilisateur = form.save(commit=False)
            utilisateur.id = id
            utilisateur.save()
            return HttpResponseRedirect("/adminserver/utilisateurs")
        else:
            return render(request, "update.html", {"form": form, "id": id})
    else:
        serveur = models.utilisateurs.objects.get(pk=id)
        form = utilisateursForm(serveur.dico())
        return render(request, "update.html", {"form": form,"id":id})

def delete_utilisateur(request, id):
    utilisateur = models.utilisateurs.objects.get(pk=id)
    utilisateur.delete()
    return HttpResponseRedirect("/adminserver/utilisateurs")

def affiche_utilisateur(request, id):
    utilisateur = models.utilisateurs.objects.get(pk=id)
    return render(request,"serveur/affiche.html",{"utilisateur" : utilisateur})

