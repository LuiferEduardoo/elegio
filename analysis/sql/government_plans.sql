INSERT INTO government_plans (
    candidate_id,
    plan_url,
    created_at,
    updated_at,
    deleted_at
) VALUES
((SELECT id FROM candidates WHERE presidential_candidate = 'Iván Cepeda Castro'), 'https://www.movimientopactohistorico.co/docs/programa-gobierno-2026-2030.pdf', NOW(), NOW(), NULL),
((SELECT id FROM candidates WHERE presidential_candidate = 'Abelardo Gabriel de la Espriella'), 'https://defensoresdelapatria.com/', NOW(), NOW(), NULL),
((SELECT id FROM candidates WHERE presidential_candidate = 'Paloma Susana Valencia Laserna'), 'https://palomapresidente.com.co/', NOW(), NOW(), NULL),
((SELECT id FROM candidates WHERE presidential_candidate = 'Óscar Mauricio Lizcano Arango'), 'https://www.elespectador.com/politica/elecciones-colombia-2026/propuestas-de-mauricio-lizcano-este-es-su-plan-de-gobierno-sobre-seguridad-salud-y-reforma-tributaria-noticias-hoy/', NOW(), NOW(), NULL),
((SELECT id FROM candidates WHERE presidential_candidate = 'Raúl Santiago Botero Jaramillo'), 'https://romperelsistema.com/programa', NOW(), NOW(), NULL),
((SELECT id FROM candidates WHERE presidential_candidate = 'Miguel Uribe Londoño'), 'https://migueluribe.com/', NOW(), NOW(), NULL),
((SELECT id FROM candidates WHERE presidential_candidate = 'Sondra Macollins Garvin Pinto'), 'https://sondramacollins.com', NOW(), NOW(), NULL),
((SELECT id FROM candidates WHERE presidential_candidate = 'Claudia Nayibe López Hernández'), 'https://claudia-lopez.com/campana/', NOW(), NOW(), NULL),
((SELECT id FROM candidates WHERE presidential_candidate = 'Sergio Fajardo Valderrama'), 'https://www.sergiofajardo.com/propuestas', NOW(), NOW(), NULL),
((SELECT id FROM candidates WHERE presidential_candidate = 'Roy Leonardo Barreras Montealegre'), 'https://roybarreras.com/#propuestas', NOW(), NOW(), NULL),
((SELECT id FROM candidates WHERE presidential_candidate = 'Gustavo Matamoros Camacho'), NULL, NOW(), NOW(), NULL),
((SELECT id FROM candidates WHERE presidential_candidate = 'Luis Gilberto Murillo Urrutia'), 'https://www.instagram.com/p/DU_ZiZ-kcj1/?img_index=7', NOW(), NOW(), NULL),
((SELECT id FROM candidates WHERE presidential_candidate = 'Carlos Eduardo Caicedo Omar'), 'https://fuerzaciudadana.com.co/nuestro-proyecto', NOW(), NOW(), NULL);