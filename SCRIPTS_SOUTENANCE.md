# SCRIPTS DE SOUTENANCE — IFRI_MentorLink · Groupe 45
Présentation 12-13 juin 2026
Durée totale estimée : 15-20 minutes + questions

---

## DÉROULÉ GÉNÉRAL DE LA PRÉSENTATION

```
[1] TOBIE — Introduction + architecture + lancement démo         (4 min)
[2] CHARNEL — Module Frontend (Bootstrap 5, templates)           (1-2 min)
[3] FANELLE — Base de données (schéma, 10 tables)                (1-2 min)
[4] CURTIS — Algorithme de matching                              (2 min)
[5] MOUBARAK — Module Messagerie (SocketIO)                      (2 min)
[6] JOACHIM — Module Profils                                     (1-2 min)
[7] FRITZELL — Documentation + conclusion                        (1 min)
[8] TOBIE — Démo live                                            (3-4 min)
[TOUS] Questions des encadrants
```

---

# ═══════════════════════════════════════
# [1] TOBIE — Introduction & Architecture
# (chef de projet — parle en premier et en dernier)
# ═══════════════════════════════════════

"Bonjour. Je suis Tobie AMADOU, chef de projet du groupe 45. Notre groupe de sept étudiants vous présente aujourd'hui IFRI_MentorLink, l'application web qu'on a réalisée dans le cadre du projet intégrateur 2025-2026.

Le problème qu'on a voulu résoudre, on le vit tous ici à l'IFRI. Quand tu bloques sur un exercice de réseau ou sur une requête SQL, tu cherches quelqu'un qui peut t'aider. Et tu ne sais pas toujours qui contacter, ni si cette personne est disponible. À l'inverse, si tu maîtrises bien l'algorithmique et que tu voudrais aider un camarade, tu ne sais pas forcément qui en a besoin. IFRI_MentorLink automatise cette mise en relation.

Concrètement, chaque étudiant crée un profil avec ses compétences maîtrisées, ses lacunes et ses disponibilités. L'algorithme analyse ces informations et propose les meilleures correspondances avec un score de compatibilité sur 100. Dès qu'une correspondance intéresse les deux parties, une messagerie en temps réel leur permet de s'organiser directement dans l'application.

L'application est structurée en trois modules obligatoires : la gestion des comptes et profils, la mise en correspondance par algorithme, et la messagerie instantanée.

Pour le choix technique, on a opté pour Flask côté backend — c'est Python, c'est léger et ça nous laisse la liberté de structurer le projet comme on veut. La base de données est en MySQL 8, comme recommandé dans le cahier des charges. La messagerie temps réel est gérée par Flask-SocketIO avec des WebSockets. Les mots de passe sont hashés avec bcrypt. Et le frontend utilise Bootstrap 5 avec les templates Jinja2.

Je vais maintenant laisser chaque membre de l'équipe présenter sa partie. On commencera par la démo live après les présentations."

---

# ═══════════════════════════════════════
# [2] CHARNEL — Frontend Bootstrap 5
# ═══════════════════════════════════════

"Bonjour, je m'appelle Charnel DAKOU, j'ai travaillé sur la partie frontend — tout ce que l'utilisateur voit et avec quoi il interagit.

J'ai développé l'ensemble des pages de l'application avec Bootstrap 5 et le moteur de templates Jinja2. Bootstrap 5, c'est un framework CSS qui donne un design propre et responsive sans devoir tout écrire de zéro. Jinja2, c'est le système de templates de Flask — il permet d'injecter des données Python directement dans les pages HTML.

Les pages que j'ai produites : le layout principal avec la navbar et les messages flash, les formulaires d'inscription et de connexion, le tableau de bord avec les deux sections de matching, les pages de profil, la liste et le formulaire de création des offres, et les deux pages de messagerie — la liste des conversations et l'interface de chat.

Le défi principal pour moi, c'était de faire en sorte que les formulaires communiquent correctement avec le backend Flask — par exemple que les cases à cocher des compétences soient bien envoyées et enregistrées en base de données. Globalement, j'ai voulu faire quelque chose de clair et facile à utiliser."

---

# ═══════════════════════════════════════
# [3] FANELLE — Base de données MySQL
# ═══════════════════════════════════════

"Bonjour, je m'appelle Fanelle ASSOGBAHOU, j'ai travaillé sur la base de données du projet.

Mon rôle principal était de concevoir le schéma relationnel et de produire le fichier schema.sql qui crée toutes les tables. En partant du cahier des charges, j'ai identifié les entités nécessaires et les relations entre elles, et on a abouti à une base de 10 tables organisées en trois groupes qui correspondent aux trois modules de l'application.

Le premier groupe — Module 1 — contient les tables users, competences, user_competences et disponibilites. Ces tables stockent les profils des étudiants, leurs compétences maîtrisées ou à améliorer, et leurs disponibilités horaires.

Le deuxième groupe — Module 2 — contient les tables offres_demandes, offres_demandes_competences et matchings. Ces tables gèrent les offres publiées par les étudiants et les correspondances calculées par l'algorithme.

Le troisième groupe — Module 3 — contient les tables conversations, messages et notifications. Ces tables supportent la messagerie en temps réel.

Les clés étrangères assurent l'intégrité référentielle entre les tables — on ne peut pas avoir un message qui pointe vers une conversation qui n'existe pas, par exemple."

---

# ═══════════════════════════════════════
# [4] CURTIS — Algorithme de matching
# ═══════════════════════════════════════

"Bonjour, je m'appelle Curtis CAKPO, j'ai développé l'algorithme de matching — le cœur de l'application.

L'objectif de cet algorithme, c'est de répondre à la question : parmi tous les étudiants inscrits, lesquels sont les plus compatibles avec moi pour du mentorat ? Pour calculer ça, on utilise un score sur 100 points basé sur trois critères.

Le premier critère, c'est la compatibilité des compétences — il représente 60 points sur 100. L'algorithme regarde combien de matières correspondent entre ce que l'utilisateur A maîtrise et ce que l'utilisateur B veut améliorer. Plus il y a de matières en commun dans ce sens, plus le score monte.

Le deuxième critère, ce sont les disponibilités communes — 30 points. Si un mentor et un mentoré n'ont aucun créneau en commun dans la semaine, le mentorat ne peut pas fonctionner en pratique. L'algorithme comptabilise les créneaux qui se recoupent.

Le troisième critère, c'est la proximité de filière — 10 points. Deux étudiants de la même filière partagent souvent les mêmes cours et les mêmes problèmes. C'est un bonus mais pas un critère éliminatoire.

Dans le code Flask, cette logique est implémentée en Python dans les routes du module matching. Le dashboard affiche les résultats en deux sections : les mentors recommandés en bleu et les étudiants qu'on peut mentorer en vert."

---

# ═══════════════════════════════════════
# [5] MOUBARAK — Messagerie Flask-SocketIO
# ═══════════════════════════════════════

"Bonjour, je m'appelle Moubarak SOULE, j'ai développé le module de messagerie instantanée.

La particularité de ce module, c'est que les messages s'affichent en temps réel — sans qu'on ait besoin de rafraîchir la page. Pour ça, j'ai utilisé Flask-SocketIO, qui implémente le protocole WebSocket. La différence avec HTTP classique, c'est que la connexion reste ouverte entre le navigateur et le serveur. Dès qu'un message est envoyé, le serveur le pousse directement à tous les participants de la conversation, sans attendre une nouvelle requête.

Techniquement, j'ai créé trois modèles SQLAlchemy — Conversation, Message et Notification. Les routes HTTP gèrent la liste des conversations et l'accès à chaque chat. Les événements SocketIO gèrent l'envoi et la réception des messages en temps réel.

Une conversation est créée automatiquement quand deux utilisateurs acceptent un matching — ils n'ont pas besoin d'initier manuellement le contact. L'historique complet de chaque conversation est conservé en base de données."

---

# ═══════════════════════════════════════
# [6] JOACHIM — Module Profils
# ═══════════════════════════════════════

"Bonjour, je m'appelle Joachim HOUNYO, j'ai développé le module de gestion des profils utilisateurs.

Mon module couvre deux fonctionnalités principales. La première, c'est la consultation du profil : depuis n'importe quelle page, on peut cliquer sur le nom d'un utilisateur pour voir son profil — ses compétences, ses lacunes, sa filière et sa bio. La route Flask pour ça, c'est /profil/<id>.

La deuxième fonctionnalité, c'est la modification du profil. L'utilisateur peut changer ses informations personnelles, mettre à jour ses compétences maîtrisées, ses lacunes et ses disponibilités horaires à tout moment. Ces informations sont directement liées à l'algorithme de matching — les modifier change les correspondances proposées par le tableau de bord.

Pour l'enregistrement en base de données, j'ai utilisé des requêtes SQL directes pour les compétences et les disponibilités. Ça nous a donné plus de contrôle sur les opérations DELETE et INSERT pour éviter les doublons."

---

# ═══════════════════════════════════════
# [7] FRITZELL — Documentation & Conclusion
# ═══════════════════════════════════════

"Bonjour, je m'appelle Fritzell ADANMITONDE, j'ai travaillé sur la documentation du projet.

Mon rôle était de produire le rapport de projet — le fichier index.html que vous pouvez consulter directement dans le navigateur depuis le dépôt GitHub. Ce rapport couvre les informations obligatoires du cahier des charges : la présentation du groupe et les contributions de chaque membre, notre mode de fonctionnement interne et la chronologie du projet, la description complète de l'architecture technique et de la base de données, les instructions de déploiement en local pour Ubuntu et pour Windows, et le manuel d'utilisation de toutes les fonctionnalités.

Pour conclure, en dix jours, le groupe 45 a développé une application web fonctionnelle qui répond à l'ensemble des exigences du cahier des charges. L'application couvre les trois modules obligatoires, la messagerie est en temps réel avec SocketIO, les mots de passe sont sécurisés avec bcrypt, et Git a été utilisé tout au long du projet avec une branche par module.

Je laisse la parole à Tobie pour la démonstration live."

---

# ═══════════════════════════════════════
# [8] TOBIE — Script démo live
# (à faire pendant que l'appli tourne)
# ═══════════════════════════════════════

```
ORDRE DE LA DÉMO (à faire dans cet ordre exact) :

1. ./lancer.sh (ou python app.py si déjà lancé)
   → "L'application tourne sur localhost:5000"

2. Ouvrir http://127.0.0.1:5000/auth/connexion
   → "Voici la page de connexion"

3. Se connecter avec tobie@ifri.bj / Test1234!
   → "On a nos données de test chargées. Là vous voyez le flash message de bienvenue."

4. Montrer le Dashboard
   → "Deux sections : mentors recommandés en bleu à gauche, mentorés potentiels en vert à droite. Le score 75 par exemple, ça veut dire 75/100 de compatibilité."

5. Cliquer sur "Contacter" sur un mentor
   → "On clique Contacter — l'algorithme crée le matching, crée la conversation, et on arrive directement dans le chat."

6. Envoyer un message
   → "Je tape un message et j'appuie sur Entrée. Le message s'affiche instantanément."

7. (Si deuxième machine disponible) Ouvrir avec moubarak@ifri.bj
   → "Sur cette machine, je suis connecté avec un autre compte. Vous voyez la conversation qui est déjà là. Si j'envoie un message depuis ici — [envoyer] — il apparaît immédiatement sur l'autre écran. C'est le temps réel SocketIO."

8. Aller sur Offres & Demandes
   → "Section offres — on peut créer une offre, la modifier, la supprimer."

9. Montrer la page Modifier le profil
   → "Ici les compétences et lacunes sont pré-cochées, les disponibilités pré-remplies. On modifie, on enregistre."

10. Déconnexion
    → "Voilà pour la démo. L'ensemble des fonctionnalités du CDC sont présentes et fonctionnelles."
```

---

---

# ═══════════════════════════════════════════════════════
# RÉPONSES AUX QUESTIONS DES ENCADRANTS
# ═══════════════════════════════════════════════════════

## QUESTIONS GÉNÉRALES (tout le monde doit pouvoir répondre)

---

**Q : Quel est votre rôle dans le projet ?**

- **Tobie :** Chef de projet. J'ai coordonné l'équipe, conçu l'architecture Flask, développé le module d'authentification, et intégré toutes les branches Git. J'ai aussi fait la revue de code de chaque membre.
- **Charnel :** Frontend — toutes les pages HTML/CSS avec Bootstrap 5 et Jinja2.
- **Fanelle :** Base de données — conception du schéma relationnel et fichier schema.sql.
- **Curtis :** Algorithme de matching — le calcul du score de compatibilité sur 100 points.
- **Moubarak :** Module messagerie — Flask-SocketIO, WebSockets, conversations en temps réel.
- **Joachim :** Module profils — routes pour voir et modifier les profils, gestion des compétences et disponibilités.
- **Fritzell :** Documentation — rapport HTML (index.html), manuel d'utilisation.

---

**Q : Comment avez-vous organisé le travail en équipe ?**

*Réponse (tout le monde peut répondre) :*
"On a utilisé Git et GitHub avec une branche par membre — chaque personne travaillait sur sa propre branche sans toucher au code des autres. Tobie s'occupait de valider et fusionner les branches dans main. Pour la communication, on avait un groupe WhatsApp actif. Les décisions techniques importantes se prenaient collectivement ou lors des sessions avec l'encadrement."

---

**Q : Quelles difficultés avez-vous rencontrées ?**

*Réponse :*
"La principale difficulté, c'était l'intégration — faire communiquer tous les modules développés séparément. Il y avait des incohérences entre les noms de colonnes, des imports manquants, des formats de données différents. On a passé du temps en phase d'intégration à corriger ces points. La messagerie temps réel avec SocketIO a aussi demandé des ajustements pour que les événements WebSocket fonctionnent bien avec le reste de l'application."

---

## QUESTIONS TECHNIQUES — TOBIE (chef de projet)

---

**Q : Pourquoi avoir choisi Flask plutôt que Django ?**

"Flask est minimaliste — il n'impose rien par défaut. On a pu construire la structure qu'on voulait, module par module, avec les blueprints. Django aurait imposé beaucoup de structure qu'on n'utiliserait pas dans ce projet de dix jours. Flask correspond mieux à notre niveau et à la durée du projet."

---

**Q : Expliquez l'Application Factory Pattern.**

"C'est un design pattern Flask où l'application n'est pas créée au niveau du module mais dans une fonction — create_app(). Cette fonction crée l'instance Flask, initialise les extensions (SQLAlchemy, SocketIO, etc.) et enregistre les blueprints. L'avantage principal : on évite les imports circulaires. Quand app.py importe les routes et que les routes importent db depuis extensions.py, sans le Factory, on aurait une boucle d'imports impossible à résoudre."

---

**Q : Comment fonctionne bcrypt pour les mots de passe ?**

"bcrypt prend le mot de passe en clair et le transforme en une chaîne de caractères hashée. Cette transformation est à sens unique — impossible de retrouver le mot de passe original depuis le hash. Chaque hash est unique grâce à un salt aléatoire généré automatiquement par bcrypt. Même si deux utilisateurs ont le même mot de passe, leur hash sera différent. Quand un utilisateur se connecte, on hash le mot de passe saisi et on compare avec le hash stocké en base."

---

**Q : Pourquoi Flask-Login pour la gestion des sessions ?**

"Flask-Login gère les sessions utilisateur côté serveur. Il stocke l'identifiant de l'utilisateur dans un cookie signé avec la SECRET_KEY de l'application. Ça nous donne le décorateur @login_required qu'on applique sur toutes les routes protégées — si quelqu'un essaie d'accéder au dashboard sans être connecté, Flask-Login le redirige automatiquement vers la page de connexion."

---

**Q : Pourquoi avoir utilisé du SQL brut pour la modification du profil ?**

"SQLAlchemy ORM a un comportement appelé autoflush — il envoie automatiquement des requêtes en base avant chaque query. Pour les compétences et disponibilités, quand on faisait un DELETE+INSERT via ORM, l'autoflush créait des doublons en base. On a résolu ça en utilisant des requêtes SQL directes avec db.session.execute() — on a plus de contrôle et on évite le comportement inattendu de l'ORM sur ces opérations."

---

**Q : Votre application est-elle sécurisée ?**

"Plusieurs mesures de sécurité sont en place. Les mots de passe sont hashés avec bcrypt, jamais stockés en clair. Toutes les routes protégées ont le décorateur @login_required. La SECRET_KEY et l'URL de la base de données sont dans un fichier .env qui n'est jamais commité sur GitHub. Il y a aussi une protection contre le self-contact dans le matching — un utilisateur ne peut pas s'envoyer un message à lui-même."

---

## QUESTIONS TECHNIQUES — CURTIS (matching)

---

**Q : Détaillez le calcul du score de matching.**

"Le score est sur 100 points, pondéré sur 3 critères. Premièrement : 60 points pour les compétences — on compte le nombre de matières qui correspondent entre ce que A maîtrise et ce que B veut améliorer, plus ce que B maîtrise et ce que A veut améliorer. Deuxièmement : 30 points pour les disponibilités — on compte les créneaux horaires communs. Troisièmement : 10 points pour la filière — bonus si les deux étudiants sont dans la même filière. On ramène chaque critère à son maximum (60, 30, 10) en fonction du nombre max de matchs possibles."

---

**Q : Pourquoi cette pondération 60/30/10 ?**

"La compatibilité de compétences, c'est le cœur du mentorat — si personne n'a rien à apprendre à l'autre, ça ne sert à rien. Les disponibilités sont cruciales aussi — pas de mentorat possible si les gens ne sont jamais libres en même temps. La filière, c'est un bonus parce que des étudiants de filières différentes peuvent très bien se compléter."

---

## QUESTIONS TECHNIQUES — MOUBARAK (messagerie)

---

**Q : Qu'est-ce qu'un WebSocket et pourquoi l'utiliser pour la messagerie ?**

"HTTP classique fonctionne en requête-réponse : le navigateur envoie une requête, le serveur répond, la connexion est fermée. Pour avoir des messages en temps réel, il faudrait que le navigateur envoie une requête toutes les secondes pour vérifier les nouveaux messages — c'est inefficace. WebSocket ouvre une connexion persistante bidirectionnelle entre le navigateur et le serveur. Quand un message arrive, le serveur le pousse directement au navigateur sans attendre une requête. Flask-SocketIO implémente ce protocole."

---

**Q : Qu'arrive-t-il si l'utilisateur ferme son navigateur en cours de conversation ?**

"La connexion WebSocket est fermée automatiquement. L'utilisateur quitte la 'room' SocketIO. Les messages qu'il a envoyés et reçus sont conservés en base de données dans la table messages. Quand il reviendra, l'historique sera intact et affiché tel quel."

---

## QUESTIONS TECHNIQUES — FANELLE (BDD)

---

**Q : Expliquez la relation entre users et competences.**

"C'est une relation many-to-many — un utilisateur peut avoir plusieurs compétences, et une compétence peut être associée à plusieurs utilisateurs. Cette relation passe par la table de jointure user_competences qui ajoute une colonne type pour indiquer si c'est une compétence maîtrisée ou une lacune. Sans cette table de jointure, on ne pourrait pas stocker cette information supplémentaire sur la relation."

---

**Q : Pourquoi avoir une table notifications séparée ?**

"Pour les alertes en temps réel sur les nouveaux messages. Quand un message arrive, une notification est créée en base avec le user_id du destinataire. Ça permet de savoir si l'utilisateur a des notifications non lues, même s'il n'est pas dans la conversation au moment de la réception. C'est la base technique pour un badge 'X nouveaux messages' sur l'icône messagerie."

---

## QUESTIONS TECHNIQUES — CHARNEL (frontend)

---

**Q : Comment Jinja2 permet d'afficher des données dynamiques ?**

"Flask passe des variables Python aux templates via la fonction render_template(). Dans le fichier HTML, on utilise la syntaxe Jinja2 pour afficher ces données. Par exemple, {{ current_user.prenom }} affiche le prénom de l'utilisateur connecté. Les boucles {% for mentor in mentors %} parcourent des listes. Les conditions {% if %} permettent d'afficher ou cacher des éléments selon les données. Tout ça est rendu côté serveur — le navigateur reçoit du HTML statique final."

---

**Q : Pourquoi Bootstrap 5 et pas du CSS pur ?**

"Bootstrap 5 nous donne des composants prêts à l'emploi — grille responsive, boutons, formulaires, badges, navbar — qui ont un rendu propre et cohérent. Écrire tout ça de zéro en CSS pur aurait pris beaucoup plus de temps. Avec Bootstrap, on peut se concentrer sur la logique plutôt que sur le design pixel par pixel."

---

## QUESTIONS GÉNÉRALES FINALES

---

**Q : Si vous aviez plus de temps, qu'est-ce que vous rajouteriez ?**

"Plusieurs choses. Les notifications toast en temps réel quand on est sur une autre page — comme un badge sur l'icône messagerie. La réinitialisation du mot de passe par email. La photo de profil uploadable. Une page de recherche avancée des offres par matière ou par filière. Et peut-être une notation après la fin d'un mentorat."

---

**Q : L'application est-elle déployée en ligne ?**

"On a fait le choix de ne pas déployer en ligne. Le déploiement nécessiterait une migration de MySQL vers une base compatible cloud, la configuration de SocketIO en mode production, et la gestion de variables d'environnement sur un serveur distant. Ça représentait un risque trop important sur les deux jours restants avant la deadline. Le cahier des charges ne mentionnait pas de déploiement en ligne, donc on a concentré notre énergie sur la qualité des fonctionnalités en local."

---

**Q : Avez-vous testé l'application ?**

"Oui. On a chargé cinq utilisateurs de test complets avec différentes compétences et disponibilités. On a testé le flux complet : inscription, connexion, consultation du dashboard avec les scores de matching, clic sur 'Contacter', ouverture du chat, envoi et réception de messages en temps réel depuis deux navigateurs différents, modification du profil, création et suppression d'offres. On a aussi vérifié que les routes protégées redirigent bien vers la connexion si on n'est pas authentifié."

---

*Document créé le 09 juin 2026 · Groupe 45 · IFRI_MentorLink · Soutenance 12-13 juin*
