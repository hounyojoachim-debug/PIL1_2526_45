-- ============================================================
-- IFRI_MentorLink — Groupe 45 · PIL1_2526_45
-- schema.sql — Structure complète de la base de données
-- Généré le 04/06/2026
-- Chef de projet : AMADOU Geduld Tobie Vincent
-- ============================================================

-- ============================================================
-- 0. CRÉATION ET SÉLECTION DE LA BASE
-- ============================================================

CREATE DATABASE IF NOT EXISTS ifri_mentorlink
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE ifri_mentorlink;

-- ============================================================
-- MODULE 1 — COMPTES & PROFILS
-- 4 tables : users · competences · user_competences · disponibilites
-- ============================================================

-- ----------------------------------------------------------
-- Table : users
-- Rôle  : Contient tous les comptes étudiants de la plateforme.
--         C'est la table centrale — presque toutes les autres
--         tables lui sont reliées via une FK.
-- ----------------------------------------------------------
CREATE TABLE users (
    -- Identifiant unique, auto-incrémenté par MySQL
    id              INT             NOT NULL AUTO_INCREMENT,

    -- Nom et prénom obligatoires, max 100 caractères
    nom             VARCHAR(100)    NOT NULL,
    prenom          VARCHAR(100)    NOT NULL,

    -- Email unique (pas deux comptes avec le même email)
    -- 255 = longueur max standard d'un email (RFC 5321)
    email           VARCHAR(255)    NOT NULL,

    -- Téléphone unique (pas deux comptes avec le même numéro)
    -- VARCHAR(20) = stocké comme texte pour gérer les formats
    --               internationaux (+229...) sans perdre le zéro initial
    telephone       VARCHAR(20)     NOT NULL,

    -- Mot de passe hashé par bcrypt
    -- bcrypt génère un hash de 60 caractères, on prend 255 par sécurité
    -- JAMAIS stocker le mot de passe en clair ici
    mot_de_passe    VARCHAR(255)    NOT NULL,

    -- Filière de l'étudiant à l'IFRI
    -- ENUM = liste fermée de valeurs autorisées — MySQL rejette toute autre valeur
    filiere         ENUM('SI','GL','IA','IM','RS','Autre')  NOT NULL,

    -- Niveau d'études
    niveau          ENUM('L1','L2','L3','M1','M2')          NOT NULL,

    -- Photo de profil : chemin vers le fichier uploadé dans static/uploads/
    -- NULL = pas de photo (facultatif selon le cahier des charges)
    photo           VARCHAR(255)    DEFAULT NULL,

    -- Biographie courte, texte libre
    -- TEXT = jusqu'à 65 535 caractères (plus souple que VARCHAR)
    bio             TEXT            DEFAULT NULL,

    -- Date d'inscription : remplie automatiquement à l'INSERT
    date_inscription DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Compte actif ou désactivé (soft delete : on ne supprime pas,
    -- on désactive — l'historique est conservé)
    actif           BOOLEAN         NOT NULL DEFAULT TRUE,

    -- Contraintes de la table
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_email     (email),
    UNIQUE KEY uq_users_telephone (telephone)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------------------------------------
-- Table : competences
-- Rôle  : Référentiel des matières/compétences disponibles.
--         Table de référence — les autres tables y pointent.
-- ----------------------------------------------------------
CREATE TABLE competences (
    id          INT             NOT NULL AUTO_INCREMENT,

    -- Nom de la compétence : "Algorithmique", "Python", "Réseaux"...
    nom         VARCHAR(150)    NOT NULL,

    -- Catégorie : regroupe les compétences ("Langages", "Mathématiques"...)
    categorie   VARCHAR(100)    NOT NULL,

    PRIMARY KEY (id)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------------------------------------
-- Table : user_competences
-- Rôle  : Table de liaison entre users et competences.
--         Elle dit : "tel utilisateur maîtrise / veut améliorer telle compétence".
--         Clé primaire composite (user_id + competence_id) = une seule
--         ligne par paire utilisateur–compétence, pas de doublons.
-- ----------------------------------------------------------
CREATE TABLE user_competences (
    user_id         INT     NOT NULL,
    competence_id   INT     NOT NULL,

    -- 'maitrise'    = l'étudiant peut enseigner cette compétence
    -- 'a_ameliorer' = l'étudiant veut apprendre cette compétence
    type            ENUM('maitrise','a_ameliorer')  NOT NULL,

    -- Clé primaire composite : pas deux fois la même paire (user + compétence)
    PRIMARY KEY (user_id, competence_id),

    -- Si on supprime un user → on supprime aussi ses lignes ici (CASCADE)
    CONSTRAINT fk_uc_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- Pareil si la compétence est supprimée
    CONSTRAINT fk_uc_competence
        FOREIGN KEY (competence_id)
        REFERENCES competences(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------------------------------------
-- Table : disponibilites
-- Rôle  : Créneaux horaires où un étudiant est disponible
--         pour des séances de mentorat.
--         Un étudiant peut avoir plusieurs créneaux.
-- ----------------------------------------------------------
CREATE TABLE disponibilites (
    id          INT     NOT NULL AUTO_INCREMENT,
    user_id     INT     NOT NULL,

    -- Jour de la semaine
    jour        ENUM('lundi','mardi','mercredi','jeudi',
                     'vendredi','samedi','dimanche')  NOT NULL,

    -- Heure de début et de fin du créneau
    -- TIME = format HH:MM:SS — MySQL
    heure_debut TIME    NOT NULL,
    heure_fin   TIME    NOT NULL,

    PRIMARY KEY (id),

    CONSTRAINT fk_dispo_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- MODULE 2 — MATCHING
-- 3 tables : offres_demandes · offres_demandes_competences · matchings
-- ============================================================

-- ----------------------------------------------------------
-- Table : offres_demandes  (anciennement "offres")
-- Rôle  : Un étudiant publie soit une OFFRE de mentorat
--         (il peut enseigner) soit une DEMANDE (il cherche
--         quelqu'un qui enseigne). Une seule table pour les deux.
--         Le champ 'type' différencie les deux cas.
-- ----------------------------------------------------------
CREATE TABLE offres_demandes (
    id              INT     NOT NULL AUTO_INCREMENT,

    -- L'étudiant qui publie l'offre ou la demande
    user_id         INT     NOT NULL,

    -- 'offre'   = "je peux enseigner cette matière"
    -- 'demande' = "je cherche quelqu'un pour m'enseigner cette matière"
    type            ENUM('offre','demande')                          NOT NULL,

    -- Format de séance souhaité
    format_seance   ENUM('presentiel','en_ligne','les_deux')         NOT NULL,

    -- Description libre (optionnelle)
    description     TEXT            DEFAULT NULL,

    -- Date de publication, automatique
    date_creation   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- 'actif'   = visible dans les recherches
    -- 'inactif' = archivée (matching trouvé ou retrait)
    statut          ENUM('actif','inactif')  NOT NULL DEFAULT 'actif',

    PRIMARY KEY (id),

    CONSTRAINT fk_od_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------------------------------------
-- Table : offres_demandes_competences  (anciennement "offre_competences")
-- Rôle  : Lie chaque offre/demande aux compétences concernées.
--         Ex : offre #1 porte sur "Algorithmique" ET "Sécurité".
--         Clé primaire composite = pas de doublons.
-- ----------------------------------------------------------
CREATE TABLE offres_demandes_competences (
    offre_demande_id    INT     NOT NULL,
    competence_id       INT     NOT NULL,

    PRIMARY KEY (offre_demande_id, competence_id),

    CONSTRAINT fk_odc_offre
        FOREIGN KEY (offre_demande_id)
        REFERENCES offres_demandes(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_odc_competence
        FOREIGN KEY (competence_id)
        REFERENCES competences(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------------------------------------
-- Table : matchings
-- Rôle  : Enregistre les mises en correspondance entre
--         un mentor et un mentoré.
--
--   POINT CLÉ — deux FK vers la même table users :
--     mentor_id  = ID de l'étudiant qui ENSEIGNE dans ce matching
--     mentore_id = ID de l'étudiant qui APPREND dans ce matching
--   Un même étudiant peut être mentor_id dans une ligne
--   et mentore_id dans une autre → c'est voulu.
--
--   se mentorer lui-même.
-- ----------------------------------------------------------
CREATE TABLE matchings (
    id              INT     NOT NULL AUTO_INCREMENT,

    -- Le mentor (celui qui enseigne) — FK vers users
    mentor_id       INT     NOT NULL,

    -- Le mentoré (celui qui apprend) — FK vers users
    mentore_id      INT     NOT NULL,

    -- Score de compatibilité calculé par l'algorithme (Curtis)
    -- 0.0 à 100.0 — plus c'est élevé, plus ils sont compatibles
    score           FLOAT   NOT NULL DEFAULT 0.0,

    -- Cycle de vie du matching :
    -- propose  → matching suggéré par l'algo, pas encore accepté
    -- accepte  → les deux ont dit oui
    -- refuse   → l'un des deux a refusé
    -- actif    → mentorat en cours
    -- termine  → mentorat terminé
    statut          ENUM('propose','accepte','refuse','actif','termine')
                    NOT NULL DEFAULT 'propose',

    date_matching   DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),

    -- Un étudiant ne peut pas se mentorer lui-même

    -- Score entre 0 et 100
    CONSTRAINT chk_matching_score
        CHECK (score >= 0.0 AND score <= 100.0),

    CONSTRAINT fk_matching_mentor
        FOREIGN KEY (mentor_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_matching_mentore
        FOREIGN KEY (mentore_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- MODULE 3 — MESSAGERIE
-- 3 tables : conversations · messages · notifications
-- ============================================================

-- ----------------------------------------------------------
-- Table : conversations
-- Rôle  : Une conversation = un espace de messagerie lié
--         à UN SEUL matching.
--         UNIQUE sur matching_id = pas deux conversations
--         pour le même matching.
-- ----------------------------------------------------------
CREATE TABLE conversations (
    id              INT     NOT NULL AUTO_INCREMENT,

    -- Chaque conversation est liée à exactement 1 matching
    -- UNIQUE = impossible d'avoir 2 conversations pour le même matching
    matching_id     INT     NOT NULL,

    date_creation   DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_conv_matching (matching_id),

    CONSTRAINT fk_conv_matching
        FOREIGN KEY (matching_id)
        REFERENCES matchings(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------------------------------------
-- Table : messages
-- Rôle  : Chaque message envoyé dans une conversation.
--         expediteur_id = qui a envoyé le message.
--         lu = a-t-il été lu par le destinataire ?
-- ----------------------------------------------------------
CREATE TABLE messages (
    id                  INT     NOT NULL AUTO_INCREMENT,

    -- Dans quelle conversation ce message a été envoyé
    conversation_id     INT     NOT NULL,

    -- Qui a envoyé ce message — FK vers users
    expediteur_id       INT     NOT NULL,

    -- Contenu du message (texte)
    contenu             TEXT    NOT NULL,

    -- Date et heure d'envoi, automatique
    date_envoi          DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- FALSE = pas encore lu · TRUE = lu par le destinataire
    lu                  BOOLEAN     NOT NULL DEFAULT FALSE,

    PRIMARY KEY (id),

    CONSTRAINT fk_msg_conversation
        FOREIGN KEY (conversation_id)
        REFERENCES conversations(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_msg_expediteur
        FOREIGN KEY (expediteur_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------------------------------------
-- Table : notifications
-- Rôle  : Alertes envoyées à un utilisateur.
--         Peut venir d'un nouveau message, d'un matching
--         proposé, ou d'un événement système.
-- ----------------------------------------------------------
CREATE TABLE notifications (
    id              INT     NOT NULL AUTO_INCREMENT,

    -- L'utilisateur qui reçoit la notification
    user_id         INT     NOT NULL,

    -- Texte de la notification — max 500 caractères
    contenu         VARCHAR(500)    NOT NULL,

    -- Type de notification pour filtrer côté frontend
    type            ENUM('message','matching','systeme')  NOT NULL,

    -- FALSE = non lue (badge rouge) · TRUE = lue
    lu              BOOLEAN     NOT NULL DEFAULT FALSE,

    date_creation   DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),

    CONSTRAINT fk_notif_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- DONNÉES DE TEST
-- 7 utilisateurs · 10 compétences · disponibilités · offres · matching · messages
-- ============================================================

-- ----------------------------------------------------------
-- Compétences de référence (matières IFRI)
-- ----------------------------------------------------------
INSERT INTO competences (nom, categorie) VALUES
('Algorithmique',           'Informatique fondamentale'),  -- id=1
('Programmation C',         'Langages'),                   -- id=2
('Programmation Python',    'Langages'),                   -- id=3
('Bases de données SQL',    'Données'),                    -- id=4
('Réseaux informatiques',   'Systèmes'),                   -- id=5
('Sécurité informatique',   'Cybersécurité'),              -- id=6
('Développement web',       'Développement'),              -- id=7
('Intelligence artificielle','IA/Data'),                   -- id=8
('Mathématiques discrètes', 'Mathématiques'),              -- id=9
('Systèmes d exploitation', 'Systèmes');                   -- id=10

-- ----------------------------------------------------------
-- Utilisateurs de test — les 7 membres du Groupe 45
-- IMPORTANT : Les mots de passe ci-dessous sont des
--             PLACEHOLDERS. En production, ils seront
--             générés par bcrypt dans le code Flask.
--             Format bcrypt réel : $2b$12$[22 chars salt][31 chars hash]
--             Mot de passe test pour tous : "MentorLink2026!"
-- ----------------------------------------------------------
INSERT INTO users (nom, prenom, email, telephone, mot_de_passe, filiere, niveau, bio) VALUES
('AMADOU',          'Tobie',    'geduldamadou@gmail.com',       '197221065', '$2b$12$PLACEHOLDER_TOBIE_HASH_BCRYPT_60C',    'SI', 'L1', 'Chef de projet · Architecture BDD · Sécurité'),
('ADANMITONDE',     'Fritzell', 'fritzelladan@gmail.com',       '151901326', '$2b$12$PLACEHOLDER_FRITZELL_HASH_BCRYPT_60C', 'SI', 'L1', 'Backend Flask · Module Profils'),
('SOULE',           'Moubarak', 'moubasoule08@gmail.com',       '193493067', '$2b$12$PLACEHOLDER_MOUBARAK_HASH_BCRYPT_60C', 'SI', 'L1', 'Backend Flask · Module Messagerie'),
('ASSOGBAHOU',      'Auriane',  'aurianeassogbahou@gmail.com',  '199719796', '$2b$12$PLACEHOLDER_AURIANE_HASH_BCRYPT_60C',  'GL', 'L1', 'Qualité · Tests · Rapport HTML'),
('HOUNYO ASSOU',    'Joachim',  'hounyojoachim@gmail.com',      '164765656', '$2b$12$PLACEHOLDER_JOACHIM_HASH_BCRYPT_60C',  'GL', 'L1', 'Base de données MySQL'),
('CAKPO',           'Curtis',   'j74123484@gmail.com',          '40603989',  '$2b$12$PLACEHOLDER_CURTIS_HASH_BCRYPT_60C',   'IA', 'L1', 'Algorithme de matching'),
('DAKOU',           'Charnel',  'charneldakou01@gmail.com',     '69610577',  '$2b$12$PLACEHOLDER_CHARNEL_HASH_BCRYPT_60C',  'IM', 'L1', 'Frontend Bootstrap 5');
-- Résultat : Tobie=id1 · Fritzell=id2 · Moubarak=id3 · Auriane=id4 · Joachim=id5 · Curtis=id6 · Charnel=id7

-- ----------------------------------------------------------
-- Compétences des utilisateurs
-- ----------------------------------------------------------
INSERT INTO user_competences (user_id, competence_id, type) VALUES
-- Tobie (id=1) : maîtrise Algo + Sécurité · veut améliorer IA + BDD
(1, 1, 'maitrise'),         -- Algo
(1, 6, 'maitrise'),         -- Sécurité
(1, 8, 'a_ameliorer'),      -- IA
(1, 4, 'a_ameliorer'),      -- BDD SQL
-- Curtis (id=6) : maîtrise IA + Python · veut améliorer Sécurité
(6, 8, 'maitrise'),         -- IA
(6, 3, 'maitrise'),         -- Python
(6, 6, 'a_ameliorer'),      -- Sécurité
-- Joachim (id=5) : maîtrise BDD · veut améliorer Réseaux + Algo
(5, 4, 'maitrise'),         -- BDD SQL
(5, 5, 'a_ameliorer'),      -- Réseaux
(5, 1, 'a_ameliorer'),      -- Algo
-- Fritzell (id=2) : maîtrise Python + Web · veut améliorer Sécurité
(2, 3, 'maitrise'),         -- Python
(2, 7, 'maitrise'),         -- Développement web
(2, 6, 'a_ameliorer'),      -- Sécurité
-- Moubarak (id=3) : maîtrise Réseaux · veut améliorer IA
(3, 5, 'maitrise'),         -- Réseaux
(3, 8, 'a_ameliorer');      -- IA

-- ----------------------------------------------------------
-- Disponibilités
-- ----------------------------------------------------------
INSERT INTO disponibilites (user_id, jour, heure_debut, heure_fin) VALUES
(1, 'lundi',    '18:00:00', '20:00:00'),    -- Tobie : lundi soir
(1, 'samedi',   '09:00:00', '12:00:00'),    -- Tobie : samedi matin
(6, 'mardi',    '17:00:00', '19:00:00'),    -- Curtis : mardi après-midi
(6, 'samedi',   '10:00:00', '13:00:00'),    -- Curtis : samedi matin
(5, 'mercredi', '16:00:00', '18:00:00'),    -- Joachim : mercredi après-midi
(5, 'dimanche', '14:00:00', '17:00:00');    -- Joachim : dimanche après-midi

-- ----------------------------------------------------------
-- Offres et demandes de mentorat
-- ----------------------------------------------------------
INSERT INTO offres_demandes (user_id, type, format_seance, description, statut) VALUES
(1, 'offre',   'les_deux',   'Propose du mentorat en Algorithmique et Sécurité informatique', 'actif'),   -- id=1
(6, 'offre',   'en_ligne',   'Disponible pour aider en IA et Python', 'actif'),                          -- id=2
(5, 'demande', 'presentiel', 'Cherche un mentor en Réseaux informatiques et Algorithmique', 'actif'),    -- id=3
(2, 'offre',   'les_deux',   'Propose de l aide en Python et développement web', 'actif');               -- id=4

-- Compétences liées aux offres/demandes
INSERT INTO offres_demandes_competences (offre_demande_id, competence_id) VALUES
(1, 1),     -- Offre Tobie → Algorithmique
(1, 6),     -- Offre Tobie → Sécurité
(2, 8),     -- Offre Curtis → IA
(2, 3),     -- Offre Curtis → Python
(3, 5),     -- Demande Joachim → Réseaux
(3, 1),     -- Demande Joachim → Algo
(4, 3),     -- Offre Fritzell → Python
(4, 7);     -- Offre Fritzell → Développement web

-- ----------------------------------------------------------
-- Matchings de test
-- ----------------------------------------------------------
INSERT INTO matchings (mentor_id, mentore_id, score, statut) VALUES
(1, 5, 78.5, 'accepte'),    -- id=1 : Tobie mentor · Joachim mentoré (Algo)
(6, 1, 65.0, 'propose');    -- id=2 : Curtis mentor · Tobie mentoré (IA)
-- Curtis peut enseigner l'IA à Tobie → mentor_id=6, mentore_id=1
-- Tobie peut enseigner l'Algo à Joachim → mentor_id=1, mentore_id=5

-- ----------------------------------------------------------
-- Conversations liées aux matchings
-- ----------------------------------------------------------
INSERT INTO conversations (matching_id) VALUES
(1);    -- id=1 : conversation du matching Tobie→Joachim

-- ----------------------------------------------------------
-- Messages de test
-- ----------------------------------------------------------
INSERT INTO messages (conversation_id, expediteur_id, contenu) VALUES
(1, 1, 'Salut Joachim ! Prêt pour une session sur les réseaux ce samedi ?'),
(1, 5, 'Oui Tobie, je suis disponible samedi matin à partir de 9h !'),
(1, 1, 'Parfait. On se retrouve en salle info ou en ligne ?');

-- ----------------------------------------------------------
-- Notifications de test
-- ----------------------------------------------------------
INSERT INTO notifications (user_id, contenu, type) VALUES
(5, 'Nouveau matching proposé avec AMADOU Tobie', 'matching'),
(5, 'AMADOU Tobie vous a envoyé un message', 'message'),
(1, 'CAKPO Curtis propose un matching avec vous', 'matching');

-- ============================================================
-- FIN DU FICHIER schema.sql
-- Pour exécuter : mysql -u root -p < schema.sql
-- Pour vérifier : USE ifri_mentorlink; SHOW TABLES;
-- ============================================================
