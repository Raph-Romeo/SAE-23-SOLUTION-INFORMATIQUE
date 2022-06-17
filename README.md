# SAE-23 : SOLUTION-INFORMATIQUE
 SUJET 6 : ADMINISTRATION DE SERVEURS

ce sujet va vous permettre de fournir une interface de gestion de serveurs informatiques et des services qui seront déployé dessus. Le gestionnaire pourra ajouter des serveurs, démarrer des services,… Le schéma de données est le suivant

- des serveurs (id, nom, type de serveur, nombre de processeur, capacité mémoire, capacité de stockage)
- des type de serveurs (id, type, description)
- des utilisateurs (id, nom, prénom, email)
- des services (id, nom du service, date de lancement, espace mémoire utilisé, mémoire vive nécessaire, serveur de lancement)
- des applications (id, nom de l'application, logo, serveurs, utilisateur)
- usage des ressources qui lient des applications à l'ensemble des services qu'elles peuvent utiliser (web, DB, stockage, …)

Vous devez implémenter un CRUD pour chacun de ces types de données. vous préparerez la base en avance et la remplirez avec des type de serveurs, des serveurs, des services, et des utilisateurs.
Votre site web devra permettre la saisie de nouveaux serveurs, services  et application. L'ajout de service et d'application devra vérifier que l'espace mémoire et le nombre de processeur est suffisant sur la machine. Vous devrez aussi pouvoir insérer une application et ses services associés sur un serveur l'aide d'un fichier. La structure du fichier attendu devra bien sur être décrite soit dans une aide, soit en préambule de la page de chargement.

Vous devrez être à même de pouvoir générer une fiche des services et applications lancées sur un serveur.
