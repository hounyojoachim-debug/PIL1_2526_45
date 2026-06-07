-- =============================================================
-- data_test.sql — IFRI_MentorLink · Groupe 45
-- Données de test : 5 utilisateurs + compétences + offres
-- Mot de passe de tous les comptes test : Test1234!
-- Hash bcrypt généré avec Python : bcrypt.generate_password_hash('Test1234!')
-- =============================================================

USE ifri_mentorlink;

-- Vider les tables dans l'ordre (FK oblige)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE offres_demandes_competences;
TRUNCATE TABLE offres_demandes;
TRUNCATE TABLE user_competences;
TRUNCATE TABLE disponibilites;
TRUNCATE TABLE matchings;
TRUNCATE TABLE messages;
TRUNCATE TABLE conversations;
TRUNCATE TABLE notifications;
TRUNCATE TABLE users;
TRUNCATE TABLE competences;
SET FOREIGN_KEY_CHECKS = 1;

-- Compétences
INSERT INTO competences (nom, categorie) VALUES
('Python',              'Programmation'),
('Algorithmique',       'Programmation'),
('Sécurité Web',        'Cybersécurité'),
('Base de données SQL', 'Données'),
('HTML/CSS',            'Web'),
('Machine Learning',    'IA'),
('Flask',               'Web'),
('Réseau',              'Infrastructure');

-- Utilisateurs (mot de passe : Test1234!)
INSERT INTO users (nom, prenom, email, telephone, mot_de_passe, filiere, niveau, bio, actif) VALUES
('AMADOU',       'Tobie',    'tobie@ifri.bj',    '97000001',
 '$2b$12$DKn6XWrgaO9hMnx4Ia5xJuW2ksymE3fYORZIU3W0k9nIL8LLDbvje',
 'SI', 'L2', 'Chef de projet MentorLink · Architecture · Sécurité', 1),

('SOULE',        'Moubarak', 'moubarak@ifri.bj', '97000002',
 '$2b$12$DKn6XWrgaO9hMnx4Ia5xJuW2ksymE3fYORZIU3W0k9nIL8LLDbvje',
 'SI', 'L2', 'Spécialiste messagerie temps réel et Flask-SocketIO', 1),

('CAKPO',        'Curtis',   'curtis@ifri.bj',   '97000003',
 '$2b$12$DKn6XWrgaO9hMnx4Ia5xJuW2ksymE3fYORZIU3W0k9nIL8LLDbvje',
 'IA', 'L2', 'Algorithmes de matching et intelligence artificielle', 1),

('DAKOU',        'Charnel',  'charnel@ifri.bj',  '97000004',
 '$2b$12$DKn6XWrgaO9hMnx4Ia5xJuW2ksymE3fYORZIU3W0k9nIL8LLDbvje',
 'IM', 'L1', 'Frontend Bootstrap · Design UI/UX', 1),

('ASSOGBAHOU',   'Fanelle',  'fanelle@ifri.bj',  '97000005',
 '$2b$12$DKn6XWrgaO9hMnx4Ia5xJuW2ksymE3fYORZIU3W0k9nIL8LLDbvje',
 'GL', 'L1', 'Gestion base de données MySQL · Modélisation', 1);

-- Compétences des utilisateurs
INSERT INTO user_competences (user_id, competence_id, type) VALUES
(1, 1, 'maitrise'),
(1, 3, 'maitrise'),
(1, 7, 'maitrise'),
(2, 1, 'maitrise'),
(2, 7, 'maitrise'),
(3, 1, 'maitrise'),
(3, 6, 'maitrise'),
(3, 2, 'maitrise'),
(4, 5, 'a_ameliorer'),
(5, 4, 'a_ameliorer');

-- Disponibilités
INSERT INTO disponibilites (user_id, jour, heure_debut, heure_fin) VALUES
(1, 'lundi',    '18:00:00', '20:00:00'),
(1, 'samedi',   '09:00:00', '12:00:00'),
(2, 'mardi',    '17:00:00', '19:00:00'),
(3, 'mercredi', '18:00:00', '21:00:00'),
(3, 'samedi',   '10:00:00', '13:00:00'),
(4, 'jeudi',    '17:00:00', '19:00:00'),
(5, 'vendredi', '16:00:00', '18:00:00');

-- Offres de mentorat
INSERT INTO offres_demandes (user_id, type, format_seance, description, statut) VALUES
(1, 'offre',   'les_deux',  'Propose du mentorat en Algorithmique et Sécurité informatique', 'actif'),
(3, 'demande', 'en_ligne',  'Disponible pour aider en IA et Python', 'actif'),
(2, 'offre',   'les_deux',  'Propose de l aide en Python et développement web', 'actif');
