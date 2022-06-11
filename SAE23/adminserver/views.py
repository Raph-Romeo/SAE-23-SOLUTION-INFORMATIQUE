from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import applicationsForm
from .forms import servicesForm
from .forms import utilisateursForm
from .forms import serveursForm
from .forms import type_de_serveursForm


from . import  models

def count_server_storage(element,id,type):
    count = 0
    if id == "":
        for q in list(models.services.objects.filter(serveur_de_lancement=element.id)):
            count = count + q.espace_memoire_utilise
        for q in list(models.applications.objects.filter(serveurs=element.id)):
            count = count + q.espace_memoire_utilise
        return count
    else:
        for q in list(models.services.objects.filter(serveur_de_lancement=element.id)):
            if q.id != id and type=="service":
                count = count + q.espace_memoire_utilise
        for q in list(models.applications.objects.filter(serveurs=element.id)):
            if q.id != id and type=="application":
                count = count + q.espace_memoire_utilise
        return count

def count_server_memory(element,id,type):
    count = 0
    if id == "":
        for q in list(models.services.objects.filter(serveur_de_lancement=element.id)):
            count = count + q.memoire_vive_necessaire
        for q in list(models.applications.objects.filter(serveurs=element.id)):
            count = count + q.memoire_vive_necessaire
        return count
    else:
        for q in list(models.services.objects.filter(serveur_de_lancement=element.id)):
            if q.id != id and type=="service":
                count = count + q.memoire_vive_necessaire
        for q in list(models.applications.objects.filter(serveurs=element.id)):
            if q.id != id and type=="application":
                count = count + q.memoire_vive_necessaire
        return count

# Create your views here.
def index(request):
    return render(request, 'index.html')

def ajout(request):
    return render(request, 'index_ajout.html')

#CRUD SERVEUR ==========================================================================================================================

def serveurs_index(request):
    URL = "serveur"
    serveurs = list(models.serveurs.objects.all())
    for i in serveurs:
        count = 0
        for q in list(models.services.objects.filter(serveur_de_lancement=i.id)):
            count = count + q.espace_memoire_utilise
        for q in list(models.applications.objects.filter(serveurs=i.id)):
            count = count + q.espace_memoire_utilise
        i.progress = round((count/i.stockage)*100,2)
        if i.progress >= 0:
            i.color = "#24a4dc"
            if i.progress >= 75:
                i.color = "orange"
                if i.progress >= 90:
                    i.color = "#d92624"
        if len(str(i.stockage - count)) > 6:
            i.ratio = str(round((i.stockage - count) / 1000000, 2)) + "To restants"
        elif len(str(i.stockage - count)) > 3:
            i.ratio = str(round((i.stockage - count)/1000,2)) + "Go restants"
        elif i.stockage - count > 0:
            i.ratio = str(i.stockage - count) + "Mo restants"
        elif i.stockage - count == 0:
            i.ratio = "FULL"
        else:
            i.ratio = "ERROR"
        i.progress = str(i.progress).replace(",", ".")
    num = len(list(models.serveurs.objects.all()))
    return render(request,"liste_index.html",{"objects" : serveurs,"title":"SERVEURS","extra":"server_img","url":URL,"count":num})

def ajout_serveur(request):
    title = "Ajouter un serveur"
    url = "serveur"
    if request.method == "POST":
        form = serveursForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/adminserver/serveurs")
        else:
            return render(request,"ajout.html",{"form" : form,"url":url,"title":title})
    else:
        form = serveursForm()
        return render(request,"ajout.html",{"form" : form,"url":url,"title":title})

def update_serveur(request, id):
    url = "serveur"
    title ="Mettre a jour un serveur"
    if request.method == "POST":
        form = serveursForm(request.POST)
        if form.is_valid():
            serveur = models.serveurs.objects.get(id=id)
            stockage = form.cleaned_data.get("stockage")
            memoire = form.cleaned_data.get("memoire")
            if (count_server_storage(serveur, "", "service") <= stockage) and (count_server_memory(serveur, "", "service") <= memoire):
                serveur = form.save(commit=False)
                serveur.id = id
                serveur.save()
                return HttpResponseRedirect("/adminserver/serveurs")
            else:
                return render(request, "update.html", {"form": form, "url": url,"title": "L'espace de stockage sur ce serveur est insufisant!","id":id})
        else:
            return render(request, "update.html", {"form": form, "url": url, "title": title,"id":id})
    else:
        serveur = models.serveurs.objects.get(pk=id)
        form = serveursForm(serveur.dico())
        return render(request, "update.html", {"form": form,"id":id,"url":url})

def delete_serveur(request, id):
    serveur = models.serveurs.objects.get(pk=id)
    serveur.delete()
    return HttpResponseRedirect("/adminserver/serveurs")

def affiche_serveur(request, id):
    serveur = models.serveurs.objects.get(pk=id)
    services = list(models.services.objects.filter(serveur_de_lancement=serveur.id))
    services_count = len(services)
    applications = list(models.applications.objects.filter(serveurs=serveur.id))
    applications_count = len(applications)
    count = count_server_storage(serveur,"","")
    temp = serveur.stockage - count
    if len(str(temp)) > 6:
        serveur.ratio = str(round((temp) / 1000000, 2)) + "To restants"
    elif len(str(temp)) > 3:
        serveur.ratio = str(round((temp) / 1000, 2)) + "Go restants"
    elif temp > 0:
        serveur.ratio = str(temp) + "Mo restants"
    elif temp == 0:
        serveur.ratio = "FULL"
    else:
        serveur.ratio = "ERROR"
    serveur.progress = str(round((count/serveur.stockage)*100,2)) + "%"
    if len(str(serveur.stockage)) > 6:
        serveur.stockage_adapt = str(serveur.stockage / 1000000) + "To"
    elif len(str(serveur.stockage)) > 3:
        serveur.stockage_adapt = str(serveur.stockage / 1000) + "Go"
    elif temp > 0:
        serveur.ratio = str(temp) + "Mo restants"
    serveur.memory_percent = str(round((count_server_memory(serveur, "", "") / serveur.memoire) * 100, 2)) + "%"
    return render(request,"serveur/affiche.html",{"serveur" : serveur,"applications":applications,"services":services,"services_count":services_count,"applications_count":applications_count})


#CRUD TYPE-SERVEUR ==========================================================================================================================
def typesServeurs_index(request):
    URL = "typeServeur"
    typesServeurs = list(models.type_de_serveurs.objects.all())
    num = len(list(models.type_de_serveurs.objects.all()))
    return render(request,"type_serveur/liste_index.html",{"objects" : typesServeurs,"title":"TYPES DE SERVEURS","extra":"","url":URL,"count":num})

def ajout_typeserveur(request):
    title = "Ajouter un type de serveur"
    url = "typeServeur"
    if request.method == "POST":
        form = type_de_serveursForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/adminserver/typesServeurs")
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
            return render(request, "update.html", {"form": form, "id": id,"url":"typeServeur"})
    else:
        type_serveur = models.type_de_serveurs.objects.get(pk=id)
        form = type_de_serveursForm(type_serveur.dico())
        return render(request, "update.html", {"form": form,"id":id,"url":"typeServeur"})

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
    num = len(list(models.services.objects.all()))
    return render(request,"liste_index.html",{"objects" : services,"title":"SERVICES","extra":"","url":URL,"count":num})

def ajout_service(request):
    title = "Ajouter un service"
    url = "service"
    if request.method == "POST":
        form = servicesForm(request.POST)
        if form.is_valid():
            serveur = form.cleaned_data.get("serveur_de_lancement")
            storage = form.cleaned_data.get("espace_memoire_utilise")
            memory = form.cleaned_data.get("memoire_vive_necessaire")
            if (storage <= serveur.stockage - count_server_storage(serveur,"","service")) and (memory <= serveur.memoire - count_server_memory(serveur,"","service")):
                form.save()
                return HttpResponseRedirect("/adminserver/services")
            else:
                return render(request,"ajout.html",{"form" : form,"url":url,"title":"L'espace de stockage sur ce serveur est insufisant!"})
        else:
            return render(request,"ajout.html",{"form" : form,"url":url,"title":title})
    else:
        form = servicesForm()
        return render(request,"ajout.html",{"form" : form,"url":url,"title":title})

def update_service(request, id):
    url = "service"
    title = "ARJOURNER LE SERVICE " + models.services.objects.get(id=id).nom_service
    if request.method == "POST":
        form = servicesForm(request.POST)
        if form.is_valid():
            serveur = form.cleaned_data.get("serveur_de_lancement")
            storage = form.cleaned_data.get("espace_memoire_utilise")
            memory = form.cleaned_data.get("memoire_vive_necessaire")
            if (storage <= serveur.stockage - count_server_storage(serveur,id,"service")) and (memory <= serveur.memoire - count_server_memory(serveur,id,"service")):
                service = form.save(commit=False)
                service.id = id
                service.save()
                return HttpResponseRedirect("/adminserver/services")
            else:
                return render(request, "update.html", {"form": form,"id":id, "url": url,"title": "L'espace de stockage sur le serveur est insufisant!"})
        else:
            return render(request, "update.html", {"form": form, "url": url,"id":id, "title": title})
    else:
        service = models.services.objects.get(pk=id)
        form = servicesForm(service.dico())
        return render(request, "update.html", {"form": form,"id":id,"url":"service","title": title})

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
    num = len(list(models.applications.objects.all()))
    return render(request,"liste_index.html",{"objects" : applications,"title":"APPLICATIONS","extra":"","url":URL,"count":num})

def ajout_application(request):
    title = "Ajouter une application"
    url = "application"
    if request.method == "POST":
        form = applicationsForm(request.POST,request.FILES)
        if form.is_valid():
            serveurs = form.cleaned_data.get("serveurs")
            temp = 0
            server_list = ""
            for i in serveurs:
                serveur = i
                storage = form.cleaned_data.get("espace_memoire_utilise")
                memory = form.cleaned_data.get("memoire_vive_necessaire")
                if (storage <= serveur.stockage - count_server_storage(serveur,"","application")) and (memory <= serveur.memoire - count_server_memory(serveur,"","application")):
                    pass
                else:
                    temp = temp + 1
                    if temp == 1:
                        server_list = str(i.nom)
                    else:
                        server_list = server_list + " , " + str(i.nom)
            if temp > 0:
                if temp == 1:
                    return render(request,"ajout.html",{"form" : form,"url":url,"title":"L'espace de stockage ou la memoire sur le serveur " + server_list + " sont insufisants!"})
                else:
                    return render(request, "ajout.html", {"form": form, "url": url,"title": "L'espace de stockage ou la memoire sur les serveurs: " + server_list + " sont insufisantes!"})
            else:
                form.save()
                return HttpResponseRedirect("/adminserver/applications")
        else:
            return render(request,"ajout.html",{"form" : form,"url":url,"title":title})
    else:
        form = applicationsForm()
        return render(request,"ajout.html",{"form" : form,"url":url,"title":title})

def update_application(request, id):
    url = "application"
    title = "Mettre a jour " + str(models.applications.objects.get(id=id).nom_application)
    if request.method == "POST":
        form = applicationsForm(request.POST, request.FILES)
        if form.is_valid():
            serveurs = form.cleaned_data.get("serveurs")
            temp = 0
            server_list = ""
            for i in serveurs:
                serveur = i
                storage = form.cleaned_data.get("espace_memoire_utilise")
                memory = form.cleaned_data.get("memoire_vive_necessaire")
                if (storage <= serveur.stockage - count_server_storage(serveur, id, "application")) and (memory <= serveur.memoire - count_server_memory(serveur,id, "application")):
                    pass
                else:
                    temp = temp + 1
                    if temp == 1:
                        server_list = str(i.nom)
                    else:
                        server_list = server_list + " , " + str(i.nom)
            if temp > 0:
                if temp == 1:
                    return render(request, "update.html", {"form": form, "url": url,"id":id,"title": "L'espace de stockage ou la memoire sur le serveur " + server_list + " sont insufisants!"})
                else:
                    return render(request, "update.html", {"form": form, "url": url,"id":id,"title": "L'espace de stockage ou la memoire sur les serveurs: " + server_list + " sont insufisantes!"})
            else:
                application = form.save(commit=False)
                application.id = id
                application.serveurs.set(form.cleaned_data.get("serveurs"))
                application.services_utilises.set(form.cleaned_data.get("services_utilises"))
                application.save()
                return HttpResponseRedirect("/adminserver/applications")
        else:
            return render(request, "ajout.html", {"form": form, "url": url,"id":id, "title": title})
    else:
        serveur = models.applications.objects.get(pk=id)
        form = applicationsForm(serveur.dico())
        return render(request, "update.html", {"form": form,"id":id,"url":"application","title":title})

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
    num = len(list(models.utilisateurs.objects.all()))
    return render(request,"liste_index.html",{"objects" : utilisateurs,"title":"UTILISATEURS","extra":"","url":URL,"count":num})

def ajout_utilisateur(request):
    title = "Ajouter un utilisateur"
    url = "utilisateur"
    if request.method == "POST":
        form = utilisateursForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/adminserver/utilisateurs")
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
            return render(request, "update.html", {"form": form, "id": id,"url":"utilisateur"})
    else:
        serveur = models.utilisateurs.objects.get(pk=id)
        form = utilisateursForm(serveur.dico())
        return render(request, "update.html", {"form": form,"id":id,"url":"utilisateur"})

def delete_utilisateur(request, id):
    utilisateur = models.utilisateurs.objects.get(pk=id)
    utilisateur.delete()
    return HttpResponseRedirect("/adminserver/utilisateurs")

def affiche_utilisateur(request, id):
    utilisateur = models.utilisateurs.objects.get(pk=id)
    return render(request,"utilisateurs/affiche.html",{"utilisateur" : utilisateur})

