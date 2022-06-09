from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('home',views.index),
#INDEXAGE DES OBJECTS DE LA BASE DE DONNEE
    path('serveurs', views.serveurs_index),
    path('services',views.services_index),
    path('utilisateurs',views.utilisateurs_index),
    path('applications',views.applications_index),
    path('typesServeurs',views.typesServeurs_index),
#AJOUTS
    path('ajout',views.ajout), #DEBUG
    path('ajout/serveur',views.ajout_serveur),
    path('ajout/utilisateur',views.ajout_utilisateur),
    path('ajout/service',views.ajout_service),
    path('ajout/application',views.ajout_application),
    path('ajout/typeServeur',views.ajout_typeserveur),
#AFFICHAGES
    path('affiche/serveur/<int:id>/',views.affiche_serveur),
    path('affiche/typeServeur/<int:id>/',views.affiche_typeserveur),
    path('affiche/utilisateur/<int:id>/',views.affiche_utilisateur),
    path('affiche/service/<int:id>/',views.affiche_service),
    path('affiche/application/<int:id>/',views.ajout_application),
#UPDATES
    path('update/serveur/<int:id>/', views.update_serveur),
    path('update/typeServeur/<int:id>/', views.update_typeserveur),
    path('update/utilisateur/<int:id>/', views.update_utilisateur),
    path('update/service/<int:id>/', views.update_service),
    path('update/application/<int:id>/', views.update_application),
#DELETE
    path('delete/serveur/<int:id>/', views.delete_serveur),
    path('delete/typeServeur/<int:id>/', views.delete_typeserveur),
    path('delete/utilisateur/<int:id>/', views.delete_utilisateur),
    path('delete/service/<int:id>/', views.delete_service),
    path('delete/application/<int:id>/', views.delete_application),
]