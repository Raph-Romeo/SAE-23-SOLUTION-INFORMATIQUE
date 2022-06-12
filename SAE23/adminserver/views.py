from django.shortcuts import render
from django.http import HttpResponseRedirect
import os
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
            if type=="service":
                if q.id != id:
                    count = count + q.espace_memoire_utilise
            else:
                count = count + q.espace_memoire_utilise
        for q in list(models.applications.objects.filter(serveurs=element.id)):
            if type=="application":
                if q.id != id:
                    count = count + q.espace_memoire_utilise
            else:
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
            if type=="service":
                if q.id != id:
                    count = count + q.memoire_vive_necessaire
            else:
                count = count + q.memoire_vive_necessaire
        for q in list(models.applications.objects.filter(serveurs=element.id)):
            if type=="application":
                if q.id != id:
                    count = count + q.memoire_vive_necessaire
            else:
                count = count + q.memoire_vive_necessaire
        return count

# Create your views here.
def index(request):
    return render(request, 'index.html')

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
    if request.method == 'GET' and 'error' in request.GET:
        return render(request,"serveur/liste_index.html",{"objects" : serveurs,"title":"SERVEURS","extra":"server_img","url":URL,"count":num,"error":request.GET['error']})
    else:
        return render(request,"serveur/liste_index.html",{"objects" : serveurs,"title":"SERVEURS","extra":"server_img","url":URL,"count":num})

def ajout_serveur(request):
    title = "Ajouter un serveur"
    url = "serveur"
    if request.method == "POST":
        form = serveursForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data.get("nom")
            for i in list(models.serveurs.objects.all()):
                if i.nom == nom:
                    return render(request, "ajout.html", {"form": form, "url": url, "title": title,"error":"Un serveur avec ce nom existe deja."})
            form.save()
            return HttpResponseRedirect("/adminserver/serveurs")
        else:
            return render(request,"ajout.html",{"form" : form,"url":url,"title":title})
    else:
        form = serveursForm()
        return render(request,"ajout.html",{"form" : form,"url":url,"title":title})

def update_serveur(request, id):
    url = "serveur"
    title ="Mettre a jour le serveur : " + str(models.serveurs.objects.get(pk=id).nom)
    if request.method == "POST":
        form = serveursForm(request.POST)
        if form.is_valid():
            serveur = models.serveurs.objects.get(id=id)
            stockage = form.cleaned_data.get("stockage")
            memoire = form.cleaned_data.get("memoire")
            if (count_server_storage(serveur, "", "service") <= stockage) and (count_server_memory(serveur, "", "service") <= memoire):
                serveur = form.save(commit=False)
                serveur.id = id
                nom = form.cleaned_data.get("nom")
                for i in list(models.serveurs.objects.all()):
                    if i.id != id:
                        if i.nom == nom:
                            return render(request, "update.html", {"form": form, "url": url, "title": title,"error": "Un serveur avec ce nom existe deja.","id":id})
                serveur.save()
                return HttpResponseRedirect("/adminserver/serveurs")
            else:
                return render(request, "update.html", {"form": form, "url": url,"error": "L'espace de stockage sur ce serveur est insufisant!","id":id,"title":title})
        else:
            return render(request, "update.html", {"form": form, "url": url, "title": title,"id":id})
    else:
        serveur = models.serveurs.objects.get(pk=id)
        form = serveursForm(serveur.dico())
        return render(request, "update.html", {"form": form,"id":id,"url":url,"title":title})

def delete_serveur(request, id):
    serveur = models.serveurs.objects.get(pk=id)
    if len(list(models.applications.objects.filter(serveurs=serveur))) > 0:
        return HttpResponseRedirect("/adminserver/serveurs?error=Impossible de supprimer ce serveur car il contient des services ou des applications.")
    if len(list(models.services.objects.filter(serveur_de_lancement=serveur))) > 0:
        return HttpResponseRedirect("/adminserver/serveurs?error=Impossible de supprimer ce serveur car il contient des services ou des applications.")
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
    count = 0
    for q in list(models.services.objects.filter(serveur_de_lancement=serveur.id)):
        count = count + q.espace_memoire_utilise
    for q in list(models.applications.objects.filter(serveurs=serveur.id)):
        count = count + q.espace_memoire_utilise
    serveur.progress_stockage = round((count / serveur.stockage) * 100, 2)
    if serveur.progress_stockage >= 0:
        serveur.color_stockage = "#24a4dc"
        if serveur.progress_stockage >= 75:
            serveur.color_stockage = "orange"
            if serveur.progress_stockage >= 90:
                serveur.color_stockage = "#d92624"
    serveur.progress_stockage = str(serveur.progress_stockage).replace(",",".")
    count = 0
    for q in list(models.services.objects.filter(serveur_de_lancement=serveur.id)):
        count = count + q.memoire_vive_necessaire
    for q in list(models.applications.objects.filter(serveurs=serveur.id)):
        count = count + q.memoire_vive_necessaire
    serveur.progress_memoire = round((count / serveur.memoire) * 100, 2)
    if serveur.progress_memoire >= 0:
        serveur.color_memoire = "#24a4dc"
        if serveur.progress_memoire >= 75:
            serveur.color_memoire = "orange"
            if serveur.progress_memoire >= 90:
                serveur.color_memoire = "#d92624"
    if len(str(serveur.memoire)) > 6:
        serveur.memoire_adapt = str(serveur.memoire / 1000000) + "To"
    elif len(str(serveur.memoire)) > 3:
        serveur.memoire_adapt = str(serveur.memoire / 1000) + "Go"
    else:
        serveur.memoire_adapt = str(serveur.memoire) + "Mo"
    serveur.progress_memoire = str(serveur.progress_memoire).replace(",",".")
    return render(request,"serveur/affiche.html",{"serveur" : serveur,"applications":applications,"services":services,"services_count":services_count,"applications_count":applications_count})


#CRUD TYPE-SERVEUR ==========================================================================================================================
def typesServeurs_index(request):
    URL = "typeServeur"
    typesServeurs = list(models.type_de_serveurs.objects.all())
    num = len(list(models.type_de_serveurs.objects.all()))
    if request.method == 'GET' and 'error' in request.GET:
        return render(request, "type_serveur/liste_index.html",{"objects": typesServeurs, "title": "TYPES DE SERVEURS", "extra": "", "url": URL, "count": num,"error":request.GET["error"]})
    else:
        return render(request,"type_serveur/liste_index.html",{"objects" : typesServeurs,"title":"TYPES DE SERVEURS","extra":"","url":URL,"count":num})

def ajout_typeserveur(request):
    title = "Ajouter un type de serveur"
    url = "typeServeur"
    if request.method == "POST":
        form = type_de_serveursForm(request.POST)
        if form.is_valid():
            type = form.cleaned_data.get("type")
            for i in list(models.type_de_serveurs.objects.all()):
                if i.type == type:
                    return render(request, "ajout.html", {"form": form, "url": url, "title": title,"error": "Ce type de serveur existe deja."})
            form.save()
            return HttpResponseRedirect("/adminserver/typesServeurs")
        else:
            return render(request,"ajout.html",{"form" : form,"url":url,"title":title})
    else:
        form = type_de_serveursForm()
        return render(request,"ajout.html",{"form" : form,"url":url,"title":title})

def update_typeserveur(request, id):
    title = "Mettre a jour le type de serveur : " + str(models.type_de_serveurs.objects.get(pk=id).type)
    if request.method == "POST":
        form = type_de_serveursForm(request.POST)
        if form.is_valid():
            type_serveur = form.save(commit=False)
            type_serveur.id = id
            type = form.cleaned_data.get("type")
            for i in list(models.type_de_serveurs.objects.all()):
                if i.id != id:
                    if i.type == type:
                        return render(request, "update.html", {"form": form, "url": "typeServeur", "id": id,"title": title,"error": "Ce type de serveur existe deja."})
            type_serveur.save()
            return HttpResponseRedirect("/adminserver/typesServeurs")
        else:
            return render(request, "update.html", {"form": form, "id": id,"url":"typeServeur","title":title})
    else:
        type_serveur = models.type_de_serveurs.objects.get(pk=id)
        form = type_de_serveursForm(type_serveur.dico())
        return render(request, "update.html", {"form": form,"id":id,"url":"typeServeur","title":title})

def delete_typeserveur(request, id):
    type_serveur = models.type_de_serveurs.objects.get(pk=id)
    if len(list(models.serveurs.objects.filter(type_de_serveur = type_serveur))) > 0:
        return HttpResponseRedirect("/adminserver/typesServeurs?error=Impossible de supprimer ce type de serveur car certain serveurs sont déjà associés à celui-ci.")
    type_serveur.delete()
    return HttpResponseRedirect("/adminserver/typesServeurs")

def affiche_typeserveur(request, id):
    typeServeur = models.type_de_serveurs.objects.get(pk=id)
    serveurs = list(models.serveurs.objects.filter(type_de_serveur=typeServeur))
    num = len(serveurs)
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
    return render(request,"type_serveur/affiche.html",{"typeServeur" : typeServeur,"serveurs":serveurs,"count":num})

#CRUD SERVICE ==========================================================================================================================

def services_index(request):
    URL = "service"
    services = list(models.services.objects.all())
    num = len(list(models.services.objects.all()))
    if request.method == 'GET' and 'error' in request.GET:
        return render(request,"services/liste_index.html",{"objects" : services,"title":"SERVICES","extra":"","url":URL,"count":num,"error":request.GET["error"]})
    else:
        return render(request, "services/liste_index.html",{"objects": services, "title": "SERVICES", "extra": "", "url": URL, "count": num})

def ajout_service(request):
    title = "Ajouter un service"
    url = "service"
    if request.method == "POST":
        form = servicesForm(request.POST)
        if form.is_valid():
            serveur = form.cleaned_data.get("serveur_de_lancement")
            storage = form.cleaned_data.get("espace_memoire_utilise")
            memory = form.cleaned_data.get("memoire_vive_necessaire")
            if storage <= 0:
                return render(request, "ajout.html", {"form": form,"url": url,"error":"L'espace de stockage sur le serveur ne peut pas etre inferieur ou egal a 0.","title": title})
            if memory <= 0:
                return render(request, "ajout.html", {"form": form,"url": url,"error":"L'utilisation de memoire vive sur le serveur ne peut pas etre inferieur ou egal a 0.","title": title})
            if (storage <= serveur.stockage - count_server_storage(serveur,"","service")) and (memory <= serveur.memoire - count_server_memory(serveur,"","service")):
                form.save()
                return HttpResponseRedirect("/adminserver/services")
            else:
                return render(request,"ajout.html",{"form" : form,"url":url,"error":"L'espace de stockage ou la memoire vive disponible sur ce serveur sont insufisantes!","title":title})
        else:
            return render(request,"ajout.html",{"form" : form,"url":url,"title":title})
    else:
        form = servicesForm()
        return render(request,"ajout.html",{"form" : form,"url":url,"title":title})

def update_service(request, id):
    url = "service"
    title = "Mettre a jour le service: " + models.services.objects.get(id=id).nom_service
    if request.method == "POST":
        form = servicesForm(request.POST)
        if form.is_valid():
            serveur = form.cleaned_data.get("serveur_de_lancement")
            storage = form.cleaned_data.get("espace_memoire_utilise")
            memory = form.cleaned_data.get("memoire_vive_necessaire")
            if storage <= 0:
                return render(request, "update.html", {"form": form, "id": id, "url": url,"error":"L'espace de stockage sur le serveur ne peut pas etre inferieur ou egal a 0.","title": title})
            if memory <= 0:
                return render(request, "update.html", {"form": form, "id": id, "url": url,"error":"L'utilisation de memoire vive sur le serveur ne peut pas etre inferieur ou egal a 0.","title": title})
            if (storage <= serveur.stockage - count_server_storage(serveur,id,"service")) and (memory <= serveur.memoire - count_server_memory(serveur,id,"service")):
                service = form.save(commit=False)
                service.id = id
                service.save()
                return HttpResponseRedirect("/adminserver/services")
            else:
                return render(request, "update.html", {"form": form,"id":id, "url": url,"error": "L'espace de stockage ou la memoire vive disponible sur le serveur sont insufisantes!","title":title})
        else:
            return render(request, "update.html", {"form": form, "url": url,"id":id, "title": title})
    else:
        service = models.services.objects.get(pk=id)
        form = servicesForm(service.dico())
        return render(request, "update.html", {"form": form,"id":id,"url":"service","title": title})

def delete_service(request, id):
    service = models.services.objects.get(pk=id)
    if len(list(models.applications.objects.filter(services_utilises=service))) == 0:
        service.delete()
        return HttpResponseRedirect("/adminserver/services")
    else:
        return HttpResponseRedirect("/adminserver/services?error=Impossible de supprimer le service " + service.nom_service + " car certaines applications utilisent ce service.")

def affiche_service(request, id):
    service = models.services.objects.get(pk=id)
    serveur = service.serveur_de_lancement
    if len(str(service.memoire_vive_necessaire)) > 6:
        service.memoire_vive_necessaire_adapt = str(round(service.memoire_vive_necessaire/1000000,2)) + "To"
    elif len(str(service.memoire_vive_necessaire)) > 3:
        service.memoire_vive_necessaire_adapt = str(round(service.memoire_vive_necessaire/1000,2)) + "Go"
    else:
        service.memoire_vive_necessaire_adapt = str(service.memoire_vive_necessaire) + "Mo"

    if len(str(service.espace_memoire_utilise)) > 6:
        service.espace_memoire_utilise_adapt = str(round(service.espace_memoire_utilise/1000000,2)) + "To"
    elif len(str(service.espace_memoire_utilise)) > 3:
        service.espace_memoire_utilise_adapt = str(round(service.espace_memoire_utilise/1000,2)) + "Go"
    else:
        service.espace_memoire_utilise_adapt = str(service.espace_memoire_utilise) + "Mo"
    count = 0
    for q in list(models.services.objects.filter(serveur_de_lancement=serveur.id)):
        count = count + q.espace_memoire_utilise
    for q in list(models.applications.objects.filter(serveurs=serveur.id)):
        count = count + q.espace_memoire_utilise
    serveur.progress = round((count / serveur.stockage) * 100, 2)
    if serveur.progress >= 0:
        serveur.color = "#24a4dc"
        if serveur.progress >= 75:
            serveur.color = "orange"
            if serveur.progress >= 90:
                serveur.color = "#d92624"
    if len(str(serveur.stockage - count)) > 6:
        serveur.ratio = str(round((serveur.stockage - count) / 1000000, 2)) + "To restants"
    elif len(str(serveur.stockage - count)) > 3:
        serveur.ratio = str(round((serveur.stockage - count) / 1000, 2)) + "Go restants"
    elif serveur.stockage - count > 0:
        serveur.ratio = str(serveur.stockage - count) + "Mo restants"
    elif serveur.stockage - count == 0:
        serveur.ratio = "FULL"
    else:
        serveur.ratio = "ERROR"
    serveur.progress = str(serveur.progress).replace(",", ".")
    return render(request,"services/affiche.html",{"service" : service,"serveur":serveur})

#CRUD APPLICATION ==========================================================================================================================

def applications_index(request):
    URL = "application"
    applications = list(models.applications.objects.all())
    num = len(list(models.applications.objects.all()))
    return render(request,"application/liste_index.html",{"objects" : applications,"title":"APPLICATIONS","extra":"","url":URL,"count":num})

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
                    return render(request,"ajout.html",{"form" : form,"url":url,"title":title,"error":"L'espace de stockage ou la memoire sur le serveur " + server_list + " sont insufisants!"})
                else:
                    return render(request, "ajout.html", {"form": form, "url": url,"title":title,"error": "L'espace de stockage ou la memoire sur les serveurs: " + server_list + " sont insufisantes!"})
            else:
                if form.cleaned_data.get("espace_memoire_utilise") <= 0:
                    return render(request, "ajout.html", {"form": form, "url": url, "title": title,"error": "Une application ne peut pas avoir une valeure de stockage inferieure ou egale a 0 octets."})
                if form.cleaned_data.get("memoire_vive_necessaire") <= 0:
                    return render(request, "ajout.html", {"form": form, "url": url, "title": title,"error": "Une application ne peut pas avoir une utilisation de memoire vive inferieure ou egale a 0 octets."})
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
                storage = form.cleaned_data.get("espace_memoire_utilise")
                memory = form.cleaned_data.get("memoire_vive_necessaire")
                serveur = i
                if (storage <= serveur.stockage - count_server_storage(serveur,id,"application")) and (memory <= serveur.memoire - count_server_memory(serveur,id,"application")):
                    pass
                else:
                    temp = temp + 1
                    if temp == 1:
                        server_list = str(i.nom)
                    else:
                        server_list = server_list + " , " + str(i.nom)
            if temp > 0:
                if temp == 1:
                    return render(request, "update.html", {"form": form, "url": url,"id":id,"title":title,"error": "L'espace de stockage ou la memoire sur le serveur " + server_list + " sont insufisants!"})
                else:
                    return render(request, "update.html", {"form": form, "url": url,"id":id,"title":title,"error": "L'espace de stockage ou la memoire sur les serveurs: " + server_list + " sont insufisantes!"})
            else:
                if form.cleaned_data.get("espace_memoire_utilise") <= 0:
                    return render(request, "update.html", {"form": form, "url": url, "id": id, "title": title,"error":"Une application ne peut pas avoir une valeure de stockage inferieure ou egale a 0 octets."})
                if form.cleaned_data.get("memoire_vive_necessaire") <= 0:
                    return render(request, "update.html", {"form": form, "url": url, "id": id, "title": title,"error":"Une application ne peut pas avoir une utilisation de memoire vive inferieure ou egale a 0 octets."})
                application = form.save(commit=False)
                application.id = id
                application.serveurs.set(form.cleaned_data.get("serveurs"))
                application.services_utilises.set(form.cleaned_data.get("services_utilises"))
                application.save()
                return HttpResponseRedirect("/adminserver/applications")
        else:
            return render(request, "update.html", {"form": form, "url": url,"id":id, "title": title})
    else:
        serveur = models.applications.objects.get(pk=id)
        form = applicationsForm(serveur.dico())
        return render(request, "update.html", {"form": form,"id":id,"url":"application","title":title})

def delete_application(request, id):
    application = models.applications.objects.get(pk=id)
    os.remove("media/" + str(application.logo))
    application.delete()
    return HttpResponseRedirect("/adminserver/applications")

def affiche_application(request, id):
    application = models.applications.objects.get(pk=id)
    if len(str(application.memoire_vive_necessaire)) > 6:
        application.memoire_vive_necessaire_adapt = str(round(application.memoire_vive_necessaire/1000000,2)) + "To"
    elif len(str(application.memoire_vive_necessaire)) > 3:
        application.memoire_vive_necessaire_adapt = str(round(application.memoire_vive_necessaire/1000,2)) + "Go"
    else:
        application.memoire_vive_necessaire_adapt = str(application.memoire_vive_necessaire) + "Mo"
    if len(str(application.espace_memoire_utilise)) > 6:
        application.espace_memoire_utilise_adapt = str(round(application.espace_memoire_utilise/1000000,2)) + "To"
    elif len(str(application.espace_memoire_utilise)) > 3:
        application.espace_memoire_utilise_adapt = str(round(application.espace_memoire_utilise/1000,2)) + "Go"
    else:
        application.espace_memoire_utilise_adapt = str(application.espace_memoire_utilise) + "Mo"
    serveurs = list(application.serveurs.all())
    services = list(application.services_utilises.all())
    return render(request,"application/affiche.html",{"application" : application,"serveurs":serveurs,"services":services,"serveurs_count":len(serveurs),"services_count":len(services)})

#CRUD UTILISATEUR ==========================================================================================================================

def utilisateurs_index(request):
    URL = "utilisateur"
    utilisateurs = list(models.utilisateurs.objects.all())
    num = len(list(models.utilisateurs.objects.all()))
    return render(request,"utilisateurs/liste_index.html",{"objects" : utilisateurs,"title":"UTILISATEURS","extra":"","url":URL,"count":num})

def ajout_utilisateur(request):
    title = "Ajouter un utilisateur"
    url = "utilisateur"
    if request.method == "POST":
        form = utilisateursForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            for i in list(models.utilisateurs.objects.all()):
                if i.email == email:
                    return render(request, "ajout.html", {"form": form, "url": url, "title": title,"error": "Un utilisateur avec cet email existe deja."})
            form.save()
            return HttpResponseRedirect("/adminserver/utilisateurs")
        else:
            return render(request,"ajout.html",{"form" : form,"url":url,"title":title})
    else:
        form = utilisateursForm()
        return render(request,"ajout.html",{"form" : form,"url":url,"title":title})

def update_utilisateur(request, id):
    title = "Mettre a jour l'utilisateur : " + str(models.utilisateurs.objects.get(pk=id).email)
    if request.method == "POST":
        form = utilisateursForm(request.POST)
        if form.is_valid():
            utilisateur = form.save(commit=False)
            utilisateur.id = id
            email = form.cleaned_data.get("email")
            for i in list(models.utilisateurs.objects.all()):
                if i.id != id:
                    if i.email == email:
                        return render(request, "update.html", {"form": form, "url":"utilisateur", "title": title,"error": "Un compte avec cet email existe deja.","id":id})
            utilisateur.save()
            return HttpResponseRedirect("/adminserver/utilisateurs")
        else:
            return render(request, "update.html", {"form": form, "id": id,"url":"utilisateur","title":title})
    else:
        serveur = models.utilisateurs.objects.get(pk=id)
        form = utilisateursForm(serveur.dico())
        return render(request, "update.html", {"form": form,"id":id,"url":"utilisateur","title":title})

def delete_utilisateur(request, id):
    utilisateur = models.utilisateurs.objects.get(pk=id)
    for i in list(models.applications.objects.filter(utilisateurs=utilisateur)):
        i.delete()
    utilisateur.delete()
    return HttpResponseRedirect("/adminserver/utilisateurs")

def affiche_utilisateur(request, id):
    utilisateur = models.utilisateurs.objects.get(pk=id)
    objects = list(models.applications.objects.filter(utilisateurs=utilisateur))
    return render(request,"utilisateurs/affiche.html",{"utilisateur" : utilisateur,"objects":objects,"count":len(objects)})