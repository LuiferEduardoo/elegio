-- ============================================================
-- INSERCIÓN DE PREGUNTAS Y OPCIONES DE RESPUESTA (MySQL)
-- Test: ¿Quién es tu candidato ideal?
-- ============================================================
-- Requisitos:
--   * Motor InnoDB para soportar transacciones.
--   * Columna `id` de las tablas `questions` y `response_options` con AUTO_INCREMENT.
-- ============================================================

START TRANSACTION;

-- ============================================================
-- Cargar IDs en variables de sesión
-- ============================================================
SELECT id INTO @test_id              FROM tests      WHERE name = '¿Quién es tu candidato ideal?';

SELECT id INTO @cat_seguridad        FROM categories WHERE name = 'Seguridad';
SELECT id INTO @cat_salud            FROM categories WHERE name = 'Salud';
SELECT id INTO @cat_economia         FROM categories WHERE name = 'Economía';
SELECT id INTO @cat_paz              FROM categories WHERE name = 'Paz';
SELECT id INTO @cat_corrupcion       FROM categories WHERE name = 'Corrupción';
SELECT id INTO @cat_agraria          FROM categories WHERE name = 'Agraria';
SELECT id INTO @cat_transformacion   FROM categories WHERE name = 'Tranformación social';
SELECT id INTO @cat_empresas         FROM categories WHERE name = 'Empresas';
SELECT id INTO @cat_educacion        FROM categories WHERE name = 'Educación';
SELECT id INTO @cat_infraestructura  FROM categories WHERE name = 'Infraestructura';
SELECT id INTO @cat_territorio       FROM categories WHERE name = 'Territorio, regiones y descentralización';
SELECT id INTO @cat_naturaleza       FROM categories WHERE name = 'Naturaleza';
SELECT id INTO @cat_hidrocarburos    FROM categories WHERE name = 'Hidrocarburos';
SELECT id INTO @cat_energia          FROM categories WHERE name = 'Energia';
SELECT id INTO @cat_politica_ext     FROM categories WHERE name = 'Política exterior';
SELECT id INTO @cat_tecnologia       FROM categories WHERE name = 'Tecnología';


-- ============================================================
-- SEGURIDAD (3 preguntas)
-- ============================================================
INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_seguridad,
    '¿La principal estrategia para reducir el crimen en ciudades como Cali, Medellín y Bogotá debería ser el aumento del pie de fuerza policial y militar en las calles?',
    'multiple_choice', 1, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy de acuerdo',     -1,   NOW(), NOW()),
(@q_id, 'De acuerdo',         -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'En desacuerdo',       0.5, NOW(), NOW()),
(@q_id, 'Muy en desacuerdo',   1,   NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_seguridad,
    'Frente a las disidencias y bandas criminales como el Clan del Golfo, ¿Colombia debería privilegiar operativos militares contundentes sobre programas de sometimiento y reincorporación?',
    'multiple_choice', 2, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy de acuerdo',     -1,   NOW(), NOW()),
(@q_id, 'De acuerdo',         -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'En desacuerdo',       0.5, NOW(), NOW()),
(@q_id, 'Muy en desacuerdo',   1,   NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_seguridad,
    '¿El Estado debería invertir más en programas sociales, culturales y de empleo juvenil en barrios populares que en endurecer las penas para delitos comunes?',
    'multiple_choice', 3, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy en desacuerdo',  -1,   NOW(), NOW()),
(@q_id, 'En desacuerdo',      -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'De acuerdo',          0.5, NOW(), NOW()),
(@q_id, 'Muy de acuerdo',      1,   NOW(), NOW());


-- ============================================================
-- SALUD (3 preguntas)
-- ============================================================
INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_salud,
    '¿Está de acuerdo con eliminar las EPS y reemplazarlas por un sistema público unificado administrado por el Estado?',
    'multiple_choice', 4, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy en desacuerdo',  -1,   NOW(), NOW()),
(@q_id, 'En desacuerdo',      -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'De acuerdo',          0.5, NOW(), NOW()),
(@q_id, 'Muy de acuerdo',      1,   NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_salud,
    '¿Las EPS privadas, en competencia regulada, son el mejor modelo para garantizar la atención en salud de los colombianos?',
    'multiple_choice', 5, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy de acuerdo',     -1,   NOW(), NOW()),
(@q_id, 'De acuerdo',         -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'En desacuerdo',       0.5, NOW(), NOW()),
(@q_id, 'Muy en desacuerdo',   1,   NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_salud,
    '¿El Estado debería ser el prestador directo de los servicios de salud en zonas rurales y apartadas, sin intermediación de aseguradoras?',
    'multiple_choice', 6, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy en desacuerdo',  -1,   NOW(), NOW()),
(@q_id, 'En desacuerdo',      -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'De acuerdo',          0.5, NOW(), NOW()),
(@q_id, 'Muy de acuerdo',      1,   NOW(), NOW());


-- ============================================================
-- ECONOMÍA (3 preguntas)
-- ============================================================
INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_economia,
    '¿Para impulsar el crecimiento, Colombia debería reducir impuestos a las empresas y mantener una estricta disciplina fiscal?',
    'multiple_choice', 7, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy de acuerdo',     -1,   NOW(), NOW()),
(@q_id, 'De acuerdo',         -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'En desacuerdo',       0.5, NOW(), NOW()),
(@q_id, 'Muy en desacuerdo',   1,   NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_economia,
    '¿El Estado colombiano debería tener un rol activo en sectores estratégicos como energía, telecomunicaciones y minería mediante empresas públicas?',
    'multiple_choice', 8, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy en desacuerdo',  -1,   NOW(), NOW()),
(@q_id, 'En desacuerdo',      -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'De acuerdo',          0.5, NOW(), NOW()),
(@q_id, 'Muy de acuerdo',      1,   NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_economia,
    '¿Los subsidios y transferencias monetarias a hogares vulnerables deberían ampliarse aunque ello implique mayor gasto público?',
    'multiple_choice', 9, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy en desacuerdo',  -1,   NOW(), NOW()),
(@q_id, 'En desacuerdo',      -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'De acuerdo',          0.5, NOW(), NOW()),
(@q_id, 'Muy de acuerdo',      1,   NOW(), NOW());


-- ============================================================
-- PAZ (2 preguntas)
-- ============================================================
INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_paz,
    '¿El gobierno debería continuar con la política de "Paz Total" y diálogos con grupos armados como el ELN y las disidencias?',
    'multiple_choice', 10, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy en desacuerdo',  -1,   NOW(), NOW()),
(@q_id, 'En desacuerdo',      -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'De acuerdo',          0.5, NOW(), NOW()),
(@q_id, 'Muy de acuerdo',      1,   NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_paz,
    '¿La JEP y la justicia restaurativa han sido un mecanismo adecuado para tramitar el conflicto armado en Colombia?',
    'multiple_choice', 11, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy en desacuerdo',  -1,   NOW(), NOW()),
(@q_id, 'En desacuerdo',      -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'De acuerdo',          0.5, NOW(), NOW()),
(@q_id, 'Muy de acuerdo',      1,   NOW(), NOW());


-- ============================================================
-- CORRUPCIÓN (2 preguntas)
-- ============================================================
INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_corrupcion,
    '¿La mejor forma de combatir la corrupción en Colombia es endurecer las penas de cárcel e imponer muerte política inmediata a funcionarios condenados?',
    'multiple_choice', 12, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy de acuerdo',     -1,   NOW(), NOW()),
(@q_id, 'De acuerdo',         -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'En desacuerdo',       0.5, NOW(), NOW()),
(@q_id, 'Muy en desacuerdo',   1,   NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_corrupcion,
    '¿La transparencia, los datos abiertos y los presupuestos participativos son herramientas más efectivas que el endurecimiento penal para prevenir la corrupción?',
    'multiple_choice', 13, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy en desacuerdo',  -1,   NOW(), NOW()),
(@q_id, 'En desacuerdo',      -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'De acuerdo',          0.5, NOW(), NOW()),
(@q_id, 'Muy de acuerdo',      1,   NOW(), NOW());


-- ============================================================
-- AGRARIA (2 preguntas)
-- ============================================================
INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_agraria,
    '¿La reforma agraria con redistribución y compra de tierras a campesinos es prioritaria frente al impulso de la agroindustria exportadora?',
    'multiple_choice', 14, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy en desacuerdo',  -1,   NOW(), NOW()),
(@q_id, 'En desacuerdo',      -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'De acuerdo',          0.5, NOW(), NOW()),
(@q_id, 'Muy de acuerdo',      1,   NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_agraria,
    '¿Los grandes proyectos agroindustriales en la Altillanura y la Orinoquía son la mejor vía para desarrollar el campo colombiano?',
    'multiple_choice', 15, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy de acuerdo',     -1,   NOW(), NOW()),
(@q_id, 'De acuerdo',         -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'En desacuerdo',       0.5, NOW(), NOW()),
(@q_id, 'Muy en desacuerdo',   1,   NOW(), NOW());


-- ============================================================
-- TRANSFORMACIÓN SOCIAL (2 preguntas)
-- ============================================================
INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_transformacion,
    '¿Programas como Renta Ciudadana y subsidios universales deberían reemplazar a esquemas focalizados como Familias en Acción?',
    'multiple_choice', 16, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy en desacuerdo',  -1,   NOW(), NOW()),
(@q_id, 'En desacuerdo',      -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'De acuerdo',          0.5, NOW(), NOW()),
(@q_id, 'Muy de acuerdo',      1,   NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_transformacion,
    '¿La movilidad social en Colombia depende principalmente del esfuerzo individual y la igualdad de oportunidades, más que de políticas redistributivas?',
    'multiple_choice', 17, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy de acuerdo',     -1,   NOW(), NOW()),
(@q_id, 'De acuerdo',         -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'En desacuerdo',       0.5, NOW(), NOW()),
(@q_id, 'Muy en desacuerdo',   1,   NOW(), NOW());


-- ============================================================
-- EMPRESAS (2 preguntas)
-- ============================================================
INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_empresas,
    '¿Para reactivar la economía, el gobierno debería reducir trámites, cargas regulatorias e impuestos al sector empresarial?',
    'multiple_choice', 18, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy de acuerdo',     -1,   NOW(), NOW()),
(@q_id, 'De acuerdo',         -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'En desacuerdo',       0.5, NOW(), NOW()),
(@q_id, 'Muy en desacuerdo',   1,   NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_empresas,
    '¿Las empresas que operan en Colombia (mineras, financieras, de servicios públicos) deberían estar sujetas a una regulación estatal más estricta y a obligaciones de responsabilidad social vinculantes?',
    'multiple_choice', 19, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy en desacuerdo',  -1,   NOW(), NOW()),
(@q_id, 'En desacuerdo',      -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'De acuerdo',          0.5, NOW(), NOW()),
(@q_id, 'Muy de acuerdo',      1,   NOW(), NOW());


-- ============================================================
-- EDUCACIÓN (2 preguntas)
-- ============================================================
INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_educacion,
    '¿La educación superior pública debería ser gratuita y universal, financiada plenamente por el Estado?',
    'multiple_choice', 20, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy en desacuerdo',  -1,   NOW(), NOW()),
(@q_id, 'En desacuerdo',      -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'De acuerdo',          0.5, NOW(), NOW()),
(@q_id, 'Muy de acuerdo',      1,   NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_educacion,
    '¿El ICETEX y los subsidios a la demanda (becas a universidades privadas) son un mecanismo legítimo y eficiente para ampliar el acceso a la educación superior?',
    'multiple_choice', 21, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy de acuerdo',     -1,   NOW(), NOW()),
(@q_id, 'De acuerdo',         -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'En desacuerdo',       0.5, NOW(), NOW()),
(@q_id, 'Muy en desacuerdo',   1,   NOW(), NOW());


-- ============================================================
-- INFRAESTRUCTURA (2 preguntas)
-- ============================================================
INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_infraestructura,
    '¿Las grandes obras de infraestructura en Colombia (vías 4G/5G, aeropuertos) deberían seguir desarrollándose principalmente bajo el modelo de concesiones y APP con privados?',
    'multiple_choice', 22, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy de acuerdo',     -1,   NOW(), NOW()),
(@q_id, 'De acuerdo',         -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'En desacuerdo',       0.5, NOW(), NOW()),
(@q_id, 'Muy en desacuerdo',   1,   NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_infraestructura,
    '¿El Estado debería priorizar inversión pública directa en vías terciarias, acueductos rurales y obras de cercanía sobre megaproyectos?',
    'multiple_choice', 23, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy en desacuerdo',  -1,   NOW(), NOW()),
(@q_id, 'En desacuerdo',      -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'De acuerdo',          0.5, NOW(), NOW()),
(@q_id, 'Muy de acuerdo',      1,   NOW(), NOW());


-- ============================================================
-- TERRITORIO, REGIONES Y DESCENTRALIZACIÓN (2 preguntas)
-- ============================================================
INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_territorio,
    '¿Los departamentos y municipios deberían tener mayor autonomía fiscal y administrativa frente al gobierno central?',
    'multiple_choice', 24, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy en desacuerdo',  -1,   NOW(), NOW()),
(@q_id, 'En desacuerdo',      -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'De acuerdo',          0.5, NOW(), NOW()),
(@q_id, 'Muy de acuerdo',      1,   NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_territorio,
    '¿Las decisiones sobre proyectos extractivos en los territorios deberían ser tomadas principalmente por el gobierno nacional, sin consultas locales vinculantes?',
    'multiple_choice', 25, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy de acuerdo',     -1,   NOW(), NOW()),
(@q_id, 'De acuerdo',         -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'En desacuerdo',       0.5, NOW(), NOW()),
(@q_id, 'Muy en desacuerdo',   1,   NOW(), NOW());


-- ============================================================
-- NATURALEZA (2 preguntas)
-- ============================================================
INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_naturaleza,
    '¿Ríos como el Atrato o ecosistemas como los páramos deberían tener derechos jurídicos propios, por encima de proyectos productivos?',
    'multiple_choice', 26, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy en desacuerdo',  -1,   NOW(), NOW()),
(@q_id, 'En desacuerdo',      -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'De acuerdo',          0.5, NOW(), NOW()),
(@q_id, 'Muy de acuerdo',      1,   NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_naturaleza,
    '¿La explotación de recursos naturales es compatible con el desarrollo si se aplican mecanismos de compensación y mitigación de mercado (bonos de carbono, pago por servicios ambientales)?',
    'multiple_choice', 27, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy de acuerdo',     -1,   NOW(), NOW()),
(@q_id, 'De acuerdo',         -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'En desacuerdo',       0.5, NOW(), NOW()),
(@q_id, 'Muy en desacuerdo',   1,   NOW(), NOW());


-- ============================================================
-- HIDROCARBUROS (2 preguntas)
-- ============================================================
INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_hidrocarburos,
    '¿Colombia debería dejar de firmar nuevos contratos de exploración petrolera y de gas para acelerar la salida del extractivismo?',
    'multiple_choice', 28, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy en desacuerdo',  -1,   NOW(), NOW()),
(@q_id, 'En desacuerdo',      -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'De acuerdo',          0.5, NOW(), NOW()),
(@q_id, 'Muy de acuerdo',      1,   NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_hidrocarburos,
    '¿Ampliar la producción de petróleo y gas en Colombia es necesario en el corto plazo para sostener las finanzas públicas y el empleo regional (Casanare, Meta, Arauca)?',
    'multiple_choice', 29, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy de acuerdo',     -1,   NOW(), NOW()),
(@q_id, 'De acuerdo',         -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'En desacuerdo',       0.5, NOW(), NOW()),
(@q_id, 'Muy en desacuerdo',   1,   NOW(), NOW());


-- ============================================================
-- ENERGÍA (2 preguntas)
-- ============================================================
INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_energia,
    '¿La transición energética en Colombia debería ser planificada y liderada por el Estado, aunque implique acelerar el cierre de fuentes fósiles?',
    'multiple_choice', 30, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy en desacuerdo',  -1,   NOW(), NOW()),
(@q_id, 'En desacuerdo',      -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'De acuerdo',          0.5, NOW(), NOW()),
(@q_id, 'Muy de acuerdo',      1,   NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_energia,
    '¿La matriz energética colombiana debería mantenerse principalmente basada en hidroeléctricas, gas y carbón, dejando que el mercado defina el ritmo de incorporación de energías renovables?',
    'multiple_choice', 31, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy de acuerdo',     -1,   NOW(), NOW()),
(@q_id, 'De acuerdo',         -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'En desacuerdo',       0.5, NOW(), NOW()),
(@q_id, 'Muy en desacuerdo',   1,   NOW(), NOW());


-- ============================================================
-- POLÍTICA EXTERIOR (2 preguntas)
-- ============================================================
INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_politica_ext,
    '¿Colombia debería diversificar sus relaciones internacionales fortaleciendo vínculos con América Latina, BRICS y el Sur Global, en lugar de mantener una alineación prioritaria con Estados Unidos?',
    'multiple_choice', 32, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy en desacuerdo',  -1,   NOW(), NOW()),
(@q_id, 'En desacuerdo',      -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'De acuerdo',          0.5, NOW(), NOW()),
(@q_id, 'Muy de acuerdo',      1,   NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_politica_ext,
    '¿La relación estratégica con Estados Unidos en materia de seguridad, comercio y lucha antinarcóticos debe seguir siendo el eje principal de la política exterior colombiana?',
    'multiple_choice', 33, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy de acuerdo',     -1,   NOW(), NOW()),
(@q_id, 'De acuerdo',         -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'En desacuerdo',       0.5, NOW(), NOW()),
(@q_id, 'Muy en desacuerdo',   1,   NOW(), NOW());


-- ============================================================
-- TECNOLOGÍA (2 preguntas)
-- ============================================================
INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_tecnologia,
    '¿Colombia debería desarrollar capacidades estatales propias en infraestructura digital y datos (nube soberana, regulación fuerte a plataformas), en lugar de depender principalmente de la inversión privada extranjera?',
    'multiple_choice', 34, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy en desacuerdo',  -1,   NOW(), NOW()),
(@q_id, 'En desacuerdo',      -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'De acuerdo',          0.5, NOW(), NOW()),
(@q_id, 'Muy de acuerdo',      1,   NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (@test_id, @cat_tecnologia,
    '¿Para impulsar el ecosistema tecnológico, Colombia debería abrir el mercado a empresas globales con incentivos tributarios y mínima regulación, aprovechando la inversión privada extranjera?',
    'multiple_choice', 35, true, NOW(), NOW());
SET @q_id = LAST_INSERT_ID();
INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
(@q_id, 'Muy de acuerdo',     -1,   NOW(), NOW()),
(@q_id, 'De acuerdo',         -0.5, NOW(), NOW()),
(@q_id, 'Neutral',             0,   NOW(), NOW()),
(@q_id, 'En desacuerdo',       0.5, NOW(), NOW()),
(@q_id, 'Muy en desacuerdo',   1,   NOW(), NOW());


COMMIT;