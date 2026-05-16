-- ============================================================
-- INSERCIÓN DE PREGUNTAS Y OPCIONES DE RESPUESTA
-- Test: ¿Quién es tu candidato ideal?
-- ============================================================

BEGIN;

-- ============================================================
-- SEGURIDAD (3 preguntas)
-- ============================================================

INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Seguridad'),
    '¿La principal estrategia para reducir el crimen en ciudades como Cali, Medellín y Bogotá debería ser el aumento del pie de fuerza policial y militar en las calles?',
    'multiple_choice', 1, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿La principal estrategia para reducir el crimen en ciudades como Cali, Medellín y Bogotá debería ser el aumento del pie de fuerza policial y militar en las calles?'), 'Muy de acuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La principal estrategia para reducir el crimen en ciudades como Cali, Medellín y Bogotá debería ser el aumento del pie de fuerza policial y militar en las calles?'), 'De acuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La principal estrategia para reducir el crimen en ciudades como Cali, Medellín y Bogotá debería ser el aumento del pie de fuerza policial y militar en las calles?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La principal estrategia para reducir el crimen en ciudades como Cali, Medellín y Bogotá debería ser el aumento del pie de fuerza policial y militar en las calles?'), 'En desacuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La principal estrategia para reducir el crimen en ciudades como Cali, Medellín y Bogotá debería ser el aumento del pie de fuerza policial y militar en las calles?'), 'Muy en desacuerdo', 1, NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Seguridad'),
    'Frente a las disidencias y bandas criminales como el Clan del Golfo, ¿Colombia debería privilegiar operativos militares contundentes sobre programas de sometimiento y reincorporación?',
    'multiple_choice', 2, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = 'Frente a las disidencias y bandas criminales como el Clan del Golfo, ¿Colombia debería privilegiar operativos militares contundentes sobre programas de sometimiento y reincorporación?'), 'Muy de acuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = 'Frente a las disidencias y bandas criminales como el Clan del Golfo, ¿Colombia debería privilegiar operativos militares contundentes sobre programas de sometimiento y reincorporación?'), 'De acuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = 'Frente a las disidencias y bandas criminales como el Clan del Golfo, ¿Colombia debería privilegiar operativos militares contundentes sobre programas de sometimiento y reincorporación?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = 'Frente a las disidencias y bandas criminales como el Clan del Golfo, ¿Colombia debería privilegiar operativos militares contundentes sobre programas de sometimiento y reincorporación?'), 'En desacuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = 'Frente a las disidencias y bandas criminales como el Clan del Golfo, ¿Colombia debería privilegiar operativos militares contundentes sobre programas de sometimiento y reincorporación?'), 'Muy en desacuerdo', 1, NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Seguridad'),
    '¿El Estado debería invertir más en programas sociales, culturales y de empleo juvenil en barrios populares que en endurecer las penas para delitos comunes?',
    'multiple_choice', 3, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿El Estado debería invertir más en programas sociales, culturales y de empleo juvenil en barrios populares que en endurecer las penas para delitos comunes?'), 'Muy en desacuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El Estado debería invertir más en programas sociales, culturales y de empleo juvenil en barrios populares que en endurecer las penas para delitos comunes?'), 'En desacuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El Estado debería invertir más en programas sociales, culturales y de empleo juvenil en barrios populares que en endurecer las penas para delitos comunes?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El Estado debería invertir más en programas sociales, culturales y de empleo juvenil en barrios populares que en endurecer las penas para delitos comunes?'), 'De acuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El Estado debería invertir más en programas sociales, culturales y de empleo juvenil en barrios populares que en endurecer las penas para delitos comunes?'), 'Muy de acuerdo', 1, NOW(), NOW());


-- ============================================================
-- SALUD (3 preguntas)
-- ============================================================

INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Salud'),
    '¿Está de acuerdo con eliminar las EPS y reemplazarlas por un sistema público unificado administrado por el Estado?',
    'multiple_choice', 4, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿Está de acuerdo con eliminar las EPS y reemplazarlas por un sistema público unificado administrado por el Estado?'), 'Muy en desacuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Está de acuerdo con eliminar las EPS y reemplazarlas por un sistema público unificado administrado por el Estado?'), 'En desacuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Está de acuerdo con eliminar las EPS y reemplazarlas por un sistema público unificado administrado por el Estado?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Está de acuerdo con eliminar las EPS y reemplazarlas por un sistema público unificado administrado por el Estado?'), 'De acuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Está de acuerdo con eliminar las EPS y reemplazarlas por un sistema público unificado administrado por el Estado?'), 'Muy de acuerdo', 1, NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Salud'),
    '¿Las EPS privadas, en competencia regulada, son el mejor modelo para garantizar la atención en salud de los colombianos?',
    'multiple_choice', 5, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿Las EPS privadas, en competencia regulada, son el mejor modelo para garantizar la atención en salud de los colombianos?'), 'Muy de acuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Las EPS privadas, en competencia regulada, son el mejor modelo para garantizar la atención en salud de los colombianos?'), 'De acuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Las EPS privadas, en competencia regulada, son el mejor modelo para garantizar la atención en salud de los colombianos?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Las EPS privadas, en competencia regulada, son el mejor modelo para garantizar la atención en salud de los colombianos?'), 'En desacuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Las EPS privadas, en competencia regulada, son el mejor modelo para garantizar la atención en salud de los colombianos?'), 'Muy en desacuerdo', 1, NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Salud'),
    '¿El Estado debería ser el prestador directo de los servicios de salud en zonas rurales y apartadas, sin intermediación de aseguradoras?',
    'multiple_choice', 6, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿El Estado debería ser el prestador directo de los servicios de salud en zonas rurales y apartadas, sin intermediación de aseguradoras?'), 'Muy en desacuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El Estado debería ser el prestador directo de los servicios de salud en zonas rurales y apartadas, sin intermediación de aseguradoras?'), 'En desacuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El Estado debería ser el prestador directo de los servicios de salud en zonas rurales y apartadas, sin intermediación de aseguradoras?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El Estado debería ser el prestador directo de los servicios de salud en zonas rurales y apartadas, sin intermediación de aseguradoras?'), 'De acuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El Estado debería ser el prestador directo de los servicios de salud en zonas rurales y apartadas, sin intermediación de aseguradoras?'), 'Muy de acuerdo', 1, NOW(), NOW());


-- ============================================================
-- ECONOMÍA (3 preguntas)
-- ============================================================

INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Economía'),
    '¿Para impulsar el crecimiento, Colombia debería reducir impuestos a las empresas y mantener una estricta disciplina fiscal?',
    'multiple_choice', 7, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿Para impulsar el crecimiento, Colombia debería reducir impuestos a las empresas y mantener una estricta disciplina fiscal?'), 'Muy de acuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Para impulsar el crecimiento, Colombia debería reducir impuestos a las empresas y mantener una estricta disciplina fiscal?'), 'De acuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Para impulsar el crecimiento, Colombia debería reducir impuestos a las empresas y mantener una estricta disciplina fiscal?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Para impulsar el crecimiento, Colombia debería reducir impuestos a las empresas y mantener una estricta disciplina fiscal?'), 'En desacuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Para impulsar el crecimiento, Colombia debería reducir impuestos a las empresas y mantener una estricta disciplina fiscal?'), 'Muy en desacuerdo', 1, NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Economía'),
    '¿El Estado colombiano debería tener un rol activo en sectores estratégicos como energía, telecomunicaciones y minería mediante empresas públicas?',
    'multiple_choice', 8, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿El Estado colombiano debería tener un rol activo en sectores estratégicos como energía, telecomunicaciones y minería mediante empresas públicas?'), 'Muy en desacuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El Estado colombiano debería tener un rol activo en sectores estratégicos como energía, telecomunicaciones y minería mediante empresas públicas?'), 'En desacuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El Estado colombiano debería tener un rol activo en sectores estratégicos como energía, telecomunicaciones y minería mediante empresas públicas?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El Estado colombiano debería tener un rol activo en sectores estratégicos como energía, telecomunicaciones y minería mediante empresas públicas?'), 'De acuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El Estado colombiano debería tener un rol activo en sectores estratégicos como energía, telecomunicaciones y minería mediante empresas públicas?'), 'Muy de acuerdo', 1, NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Economía'),
    '¿Los subsidios y transferencias monetarias a hogares vulnerables deberían ampliarse aunque ello implique mayor gasto público?',
    'multiple_choice', 9, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿Los subsidios y transferencias monetarias a hogares vulnerables deberían ampliarse aunque ello implique mayor gasto público?'), 'Muy en desacuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Los subsidios y transferencias monetarias a hogares vulnerables deberían ampliarse aunque ello implique mayor gasto público?'), 'En desacuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Los subsidios y transferencias monetarias a hogares vulnerables deberían ampliarse aunque ello implique mayor gasto público?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Los subsidios y transferencias monetarias a hogares vulnerables deberían ampliarse aunque ello implique mayor gasto público?'), 'De acuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Los subsidios y transferencias monetarias a hogares vulnerables deberían ampliarse aunque ello implique mayor gasto público?'), 'Muy de acuerdo', 1, NOW(), NOW());


-- ============================================================
-- PAZ (2 preguntas)
-- ============================================================

INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Paz'),
    '¿El gobierno debería continuar con la política de "Paz Total" y diálogos con grupos armados como el ELN y las disidencias?',
    'multiple_choice', 10, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿El gobierno debería continuar con la política de "Paz Total" y diálogos con grupos armados como el ELN y las disidencias?'), 'Muy en desacuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El gobierno debería continuar con la política de "Paz Total" y diálogos con grupos armados como el ELN y las disidencias?'), 'En desacuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El gobierno debería continuar con la política de "Paz Total" y diálogos con grupos armados como el ELN y las disidencias?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El gobierno debería continuar con la política de "Paz Total" y diálogos con grupos armados como el ELN y las disidencias?'), 'De acuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El gobierno debería continuar con la política de "Paz Total" y diálogos con grupos armados como el ELN y las disidencias?'), 'Muy de acuerdo', 1, NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Paz'),
    '¿La JEP y la justicia restaurativa han sido un mecanismo adecuado para tramitar el conflicto armado en Colombia?',
    'multiple_choice', 11, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿La JEP y la justicia restaurativa han sido un mecanismo adecuado para tramitar el conflicto armado en Colombia?'), 'Muy en desacuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La JEP y la justicia restaurativa han sido un mecanismo adecuado para tramitar el conflicto armado en Colombia?'), 'En desacuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La JEP y la justicia restaurativa han sido un mecanismo adecuado para tramitar el conflicto armado en Colombia?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La JEP y la justicia restaurativa han sido un mecanismo adecuado para tramitar el conflicto armado en Colombia?'), 'De acuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La JEP y la justicia restaurativa han sido un mecanismo adecuado para tramitar el conflicto armado en Colombia?'), 'Muy de acuerdo', 1, NOW(), NOW());


-- ============================================================
-- CORRUPCIÓN (2 preguntas)
-- ============================================================

INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Corrupción'),
    '¿La mejor forma de combatir la corrupción en Colombia es endurecer las penas de cárcel e imponer muerte política inmediata a funcionarios condenados?',
    'multiple_choice', 12, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿La mejor forma de combatir la corrupción en Colombia es endurecer las penas de cárcel e imponer muerte política inmediata a funcionarios condenados?'), 'Muy de acuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La mejor forma de combatir la corrupción en Colombia es endurecer las penas de cárcel e imponer muerte política inmediata a funcionarios condenados?'), 'De acuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La mejor forma de combatir la corrupción en Colombia es endurecer las penas de cárcel e imponer muerte política inmediata a funcionarios condenados?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La mejor forma de combatir la corrupción en Colombia es endurecer las penas de cárcel e imponer muerte política inmediata a funcionarios condenados?'), 'En desacuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La mejor forma de combatir la corrupción en Colombia es endurecer las penas de cárcel e imponer muerte política inmediata a funcionarios condenados?'), 'Muy en desacuerdo', 1, NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Corrupción'),
    '¿La transparencia, los datos abiertos y los presupuestos participativos son herramientas más efectivas que el endurecimiento penal para prevenir la corrupción?',
    'multiple_choice', 13, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿La transparencia, los datos abiertos y los presupuestos participativos son herramientas más efectivas que el endurecimiento penal para prevenir la corrupción?'), 'Muy en desacuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La transparencia, los datos abiertos y los presupuestos participativos son herramientas más efectivas que el endurecimiento penal para prevenir la corrupción?'), 'En desacuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La transparencia, los datos abiertos y los presupuestos participativos son herramientas más efectivas que el endurecimiento penal para prevenir la corrupción?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La transparencia, los datos abiertos y los presupuestos participativos son herramientas más efectivas que el endurecimiento penal para prevenir la corrupción?'), 'De acuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La transparencia, los datos abiertos y los presupuestos participativos son herramientas más efectivas que el endurecimiento penal para prevenir la corrupción?'), 'Muy de acuerdo', 1, NOW(), NOW());


-- ============================================================
-- AGRARIA (2 preguntas)
-- ============================================================

INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Agraria'),
    '¿La reforma agraria con redistribución y compra de tierras a campesinos es prioritaria frente al impulso de la agroindustria exportadora?',
    'multiple_choice', 14, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿La reforma agraria con redistribución y compra de tierras a campesinos es prioritaria frente al impulso de la agroindustria exportadora?'), 'Muy en desacuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La reforma agraria con redistribución y compra de tierras a campesinos es prioritaria frente al impulso de la agroindustria exportadora?'), 'En desacuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La reforma agraria con redistribución y compra de tierras a campesinos es prioritaria frente al impulso de la agroindustria exportadora?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La reforma agraria con redistribución y compra de tierras a campesinos es prioritaria frente al impulso de la agroindustria exportadora?'), 'De acuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La reforma agraria con redistribución y compra de tierras a campesinos es prioritaria frente al impulso de la agroindustria exportadora?'), 'Muy de acuerdo', 1, NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Agraria'),
    '¿Los grandes proyectos agroindustriales en la Altillanura y la Orinoquía son la mejor vía para desarrollar el campo colombiano?',
    'multiple_choice', 15, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿Los grandes proyectos agroindustriales en la Altillanura y la Orinoquía son la mejor vía para desarrollar el campo colombiano?'), 'Muy de acuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Los grandes proyectos agroindustriales en la Altillanura y la Orinoquía son la mejor vía para desarrollar el campo colombiano?'), 'De acuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Los grandes proyectos agroindustriales en la Altillanura y la Orinoquía son la mejor vía para desarrollar el campo colombiano?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Los grandes proyectos agroindustriales en la Altillanura y la Orinoquía son la mejor vía para desarrollar el campo colombiano?'), 'En desacuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Los grandes proyectos agroindustriales en la Altillanura y la Orinoquía son la mejor vía para desarrollar el campo colombiano?'), 'Muy en desacuerdo', 1, NOW(), NOW());


-- ============================================================
-- TRANSFORMACIÓN SOCIAL (2 preguntas)
-- ============================================================

INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Tranformación social'),
    '¿Programas como Renta Ciudadana y subsidios universales deberían reemplazar a esquemas focalizados como Familias en Acción?',
    'multiple_choice', 16, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿Programas como Renta Ciudadana y subsidios universales deberían reemplazar a esquemas focalizados como Familias en Acción?'), 'Muy en desacuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Programas como Renta Ciudadana y subsidios universales deberían reemplazar a esquemas focalizados como Familias en Acción?'), 'En desacuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Programas como Renta Ciudadana y subsidios universales deberían reemplazar a esquemas focalizados como Familias en Acción?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Programas como Renta Ciudadana y subsidios universales deberían reemplazar a esquemas focalizados como Familias en Acción?'), 'De acuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Programas como Renta Ciudadana y subsidios universales deberían reemplazar a esquemas focalizados como Familias en Acción?'), 'Muy de acuerdo', 1, NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Tranformación social'),
    '¿La movilidad social en Colombia depende principalmente del esfuerzo individual y la igualdad de oportunidades, más que de políticas redistributivas?',
    'multiple_choice', 17, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿La movilidad social en Colombia depende principalmente del esfuerzo individual y la igualdad de oportunidades, más que de políticas redistributivas?'), 'Muy de acuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La movilidad social en Colombia depende principalmente del esfuerzo individual y la igualdad de oportunidades, más que de políticas redistributivas?'), 'De acuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La movilidad social en Colombia depende principalmente del esfuerzo individual y la igualdad de oportunidades, más que de políticas redistributivas?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La movilidad social en Colombia depende principalmente del esfuerzo individual y la igualdad de oportunidades, más que de políticas redistributivas?'), 'En desacuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La movilidad social en Colombia depende principalmente del esfuerzo individual y la igualdad de oportunidades, más que de políticas redistributivas?'), 'Muy en desacuerdo', 1, NOW(), NOW());


-- ============================================================
-- EMPRESAS (2 preguntas)
-- ============================================================

INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Empresas'),
    '¿Para reactivar la economía, el gobierno debería reducir trámites, cargas regulatorias e impuestos al sector empresarial?',
    'multiple_choice', 18, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿Para reactivar la economía, el gobierno debería reducir trámites, cargas regulatorias e impuestos al sector empresarial?'), 'Muy de acuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Para reactivar la economía, el gobierno debería reducir trámites, cargas regulatorias e impuestos al sector empresarial?'), 'De acuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Para reactivar la economía, el gobierno debería reducir trámites, cargas regulatorias e impuestos al sector empresarial?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Para reactivar la economía, el gobierno debería reducir trámites, cargas regulatorias e impuestos al sector empresarial?'), 'En desacuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Para reactivar la economía, el gobierno debería reducir trámites, cargas regulatorias e impuestos al sector empresarial?'), 'Muy en desacuerdo', 1, NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Empresas'),
    '¿Las empresas que operan en Colombia (mineras, financieras, de servicios públicos) deberían estar sujetas a una regulación estatal más estricta y a obligaciones de responsabilidad social vinculantes?',
    'multiple_choice', 19, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿Las empresas que operan en Colombia (mineras, financieras, de servicios públicos) deberían estar sujetas a una regulación estatal más estricta y a obligaciones de responsabilidad social vinculantes?'), 'Muy en desacuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Las empresas que operan en Colombia (mineras, financieras, de servicios públicos) deberían estar sujetas a una regulación estatal más estricta y a obligaciones de responsabilidad social vinculantes?'), 'En desacuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Las empresas que operan en Colombia (mineras, financieras, de servicios públicos) deberían estar sujetas a una regulación estatal más estricta y a obligaciones de responsabilidad social vinculantes?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Las empresas que operan en Colombia (mineras, financieras, de servicios públicos) deberían estar sujetas a una regulación estatal más estricta y a obligaciones de responsabilidad social vinculantes?'), 'De acuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Las empresas que operan en Colombia (mineras, financieras, de servicios públicos) deberían estar sujetas a una regulación estatal más estricta y a obligaciones de responsabilidad social vinculantes?'), 'Muy de acuerdo', 1, NOW(), NOW());


-- ============================================================
-- EDUCACIÓN (2 preguntas)
-- ============================================================

INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Educación'),
    '¿La educación superior pública debería ser gratuita y universal, financiada plenamente por el Estado?',
    'multiple_choice', 20, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿La educación superior pública debería ser gratuita y universal, financiada plenamente por el Estado?'), 'Muy en desacuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La educación superior pública debería ser gratuita y universal, financiada plenamente por el Estado?'), 'En desacuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La educación superior pública debería ser gratuita y universal, financiada plenamente por el Estado?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La educación superior pública debería ser gratuita y universal, financiada plenamente por el Estado?'), 'De acuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La educación superior pública debería ser gratuita y universal, financiada plenamente por el Estado?'), 'Muy de acuerdo', 1, NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Educación'),
    '¿El ICETEX y los subsidios a la demanda (becas a universidades privadas) son un mecanismo legítimo y eficiente para ampliar el acceso a la educación superior?',
    'multiple_choice', 21, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿El ICETEX y los subsidios a la demanda (becas a universidades privadas) son un mecanismo legítimo y eficiente para ampliar el acceso a la educación superior?'), 'Muy de acuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El ICETEX y los subsidios a la demanda (becas a universidades privadas) son un mecanismo legítimo y eficiente para ampliar el acceso a la educación superior?'), 'De acuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El ICETEX y los subsidios a la demanda (becas a universidades privadas) son un mecanismo legítimo y eficiente para ampliar el acceso a la educación superior?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El ICETEX y los subsidios a la demanda (becas a universidades privadas) son un mecanismo legítimo y eficiente para ampliar el acceso a la educación superior?'), 'En desacuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El ICETEX y los subsidios a la demanda (becas a universidades privadas) son un mecanismo legítimo y eficiente para ampliar el acceso a la educación superior?'), 'Muy en desacuerdo', 1, NOW(), NOW());


-- ============================================================
-- INFRAESTRUCTURA (2 preguntas)
-- ============================================================

INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Infraestructura'),
    '¿Las grandes obras de infraestructura en Colombia (vías 4G/5G, aeropuertos) deberían seguir desarrollándose principalmente bajo el modelo de concesiones y APP con privados?',
    'multiple_choice', 22, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿Las grandes obras de infraestructura en Colombia (vías 4G/5G, aeropuertos) deberían seguir desarrollándose principalmente bajo el modelo de concesiones y APP con privados?'), 'Muy de acuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Las grandes obras de infraestructura en Colombia (vías 4G/5G, aeropuertos) deberían seguir desarrollándose principalmente bajo el modelo de concesiones y APP con privados?'), 'De acuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Las grandes obras de infraestructura en Colombia (vías 4G/5G, aeropuertos) deberían seguir desarrollándose principalmente bajo el modelo de concesiones y APP con privados?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Las grandes obras de infraestructura en Colombia (vías 4G/5G, aeropuertos) deberían seguir desarrollándose principalmente bajo el modelo de concesiones y APP con privados?'), 'En desacuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Las grandes obras de infraestructura en Colombia (vías 4G/5G, aeropuertos) deberían seguir desarrollándose principalmente bajo el modelo de concesiones y APP con privados?'), 'Muy en desacuerdo', 1, NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Infraestructura'),
    '¿El Estado debería priorizar inversión pública directa en vías terciarias, acueductos rurales y obras de cercanía sobre megaproyectos?',
    'multiple_choice', 23, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿El Estado debería priorizar inversión pública directa en vías terciarias, acueductos rurales y obras de cercanía sobre megaproyectos?'), 'Muy en desacuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El Estado debería priorizar inversión pública directa en vías terciarias, acueductos rurales y obras de cercanía sobre megaproyectos?'), 'En desacuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El Estado debería priorizar inversión pública directa en vías terciarias, acueductos rurales y obras de cercanía sobre megaproyectos?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El Estado debería priorizar inversión pública directa en vías terciarias, acueductos rurales y obras de cercanía sobre megaproyectos?'), 'De acuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿El Estado debería priorizar inversión pública directa en vías terciarias, acueductos rurales y obras de cercanía sobre megaproyectos?'), 'Muy de acuerdo', 1, NOW(), NOW());


-- ============================================================
-- TERRITORIO, REGIONES Y DESCENTRALIZACIÓN (2 preguntas)
-- ============================================================

INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Territorio%'),
    '¿Los departamentos y municipios deberían tener mayor autonomía fiscal y administrativa frente al gobierno central?',
    'multiple_choice', 24, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿Los departamentos y municipios deberían tener mayor autonomía fiscal y administrativa frente al gobierno central?'), 'Muy en desacuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Los departamentos y municipios deberían tener mayor autonomía fiscal y administrativa frente al gobierno central?'), 'En desacuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Los departamentos y municipios deberían tener mayor autonomía fiscal y administrativa frente al gobierno central?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Los departamentos y municipios deberían tener mayor autonomía fiscal y administrativa frente al gobierno central?'), 'De acuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Los departamentos y municipios deberían tener mayor autonomía fiscal y administrativa frente al gobierno central?'), 'Muy de acuerdo', 1, NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Territorio%'),
    '¿Las decisiones sobre proyectos extractivos en los territorios deberían ser tomadas principalmente por el gobierno nacional, sin consultas locales vinculantes?',
    'multiple_choice', 25, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿Las decisiones sobre proyectos extractivos en los territorios deberían ser tomadas principalmente por el gobierno nacional, sin consultas locales vinculantes?'), 'Muy de acuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Las decisiones sobre proyectos extractivos en los territorios deberían ser tomadas principalmente por el gobierno nacional, sin consultas locales vinculantes?'), 'De acuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Las decisiones sobre proyectos extractivos en los territorios deberían ser tomadas principalmente por el gobierno nacional, sin consultas locales vinculantes?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Las decisiones sobre proyectos extractivos en los territorios deberían ser tomadas principalmente por el gobierno nacional, sin consultas locales vinculantes?'), 'En desacuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Las decisiones sobre proyectos extractivos en los territorios deberían ser tomadas principalmente por el gobierno nacional, sin consultas locales vinculantes?'), 'Muy en desacuerdo', 1, NOW(), NOW());


-- ============================================================
-- NATURALEZA (2 preguntas)
-- ============================================================

INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Naturaleza'),
    '¿Ríos como el Atrato o ecosistemas como los páramos deberían tener derechos jurídicos propios, por encima de proyectos productivos?',
    'multiple_choice', 26, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿Ríos como el Atrato o ecosistemas como los páramos deberían tener derechos jurídicos propios, por encima de proyectos productivos?'), 'Muy en desacuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Ríos como el Atrato o ecosistemas como los páramos deberían tener derechos jurídicos propios, por encima de proyectos productivos?'), 'En desacuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Ríos como el Atrato o ecosistemas como los páramos deberían tener derechos jurídicos propios, por encima de proyectos productivos?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Ríos como el Atrato o ecosistemas como los páramos deberían tener derechos jurídicos propios, por encima de proyectos productivos?'), 'De acuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Ríos como el Atrato o ecosistemas como los páramos deberían tener derechos jurídicos propios, por encima de proyectos productivos?'), 'Muy de acuerdo', 1, NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Naturaleza'),
    '¿La explotación de recursos naturales es compatible con el desarrollo si se aplican mecanismos de compensación y mitigación de mercado (bonos de carbono, pago por servicios ambientales)?',
    'multiple_choice', 27, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿La explotación de recursos naturales es compatible con el desarrollo si se aplican mecanismos de compensación y mitigación de mercado (bonos de carbono, pago por servicios ambientales)?'), 'Muy de acuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La explotación de recursos naturales es compatible con el desarrollo si se aplican mecanismos de compensación y mitigación de mercado (bonos de carbono, pago por servicios ambientales)?'), 'De acuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La explotación de recursos naturales es compatible con el desarrollo si se aplican mecanismos de compensación y mitigación de mercado (bonos de carbono, pago por servicios ambientales)?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La explotación de recursos naturales es compatible con el desarrollo si se aplican mecanismos de compensación y mitigación de mercado (bonos de carbono, pago por servicios ambientales)?'), 'En desacuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La explotación de recursos naturales es compatible con el desarrollo si se aplican mecanismos de compensación y mitigación de mercado (bonos de carbono, pago por servicios ambientales)?'), 'Muy en desacuerdo', 1, NOW(), NOW());


-- ============================================================
-- HIDROCARBUROS (2 preguntas)
-- ============================================================

INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Hidrocarburos'),
    '¿Colombia debería dejar de firmar nuevos contratos de exploración petrolera y de gas para acelerar la salida del extractivismo?',
    'multiple_choice', 28, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿Colombia debería dejar de firmar nuevos contratos de exploración petrolera y de gas para acelerar la salida del extractivismo?'), 'Muy en desacuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Colombia debería dejar de firmar nuevos contratos de exploración petrolera y de gas para acelerar la salida del extractivismo?'), 'En desacuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Colombia debería dejar de firmar nuevos contratos de exploración petrolera y de gas para acelerar la salida del extractivismo?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Colombia debería dejar de firmar nuevos contratos de exploración petrolera y de gas para acelerar la salida del extractivismo?'), 'De acuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Colombia debería dejar de firmar nuevos contratos de exploración petrolera y de gas para acelerar la salida del extractivismo?'), 'Muy de acuerdo', 1, NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Hidrocarburos'),
    '¿Ampliar la producción de petróleo y gas en Colombia es necesario en el corto plazo para sostener las finanzas públicas y el empleo regional (Casanare, Meta, Arauca)?',
    'multiple_choice', 29, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿Ampliar la producción de petróleo y gas en Colombia es necesario en el corto plazo para sostener las finanzas públicas y el empleo regional (Casanare, Meta, Arauca)?'), 'Muy de acuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Ampliar la producción de petróleo y gas en Colombia es necesario en el corto plazo para sostener las finanzas públicas y el empleo regional (Casanare, Meta, Arauca)?'), 'De acuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Ampliar la producción de petróleo y gas en Colombia es necesario en el corto plazo para sostener las finanzas públicas y el empleo regional (Casanare, Meta, Arauca)?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Ampliar la producción de petróleo y gas en Colombia es necesario en el corto plazo para sostener las finanzas públicas y el empleo regional (Casanare, Meta, Arauca)?'), 'En desacuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Ampliar la producción de petróleo y gas en Colombia es necesario en el corto plazo para sostener las finanzas públicas y el empleo regional (Casanare, Meta, Arauca)?'), 'Muy en desacuerdo', 1, NOW(), NOW());


-- ============================================================
-- ENERGÍA (2 preguntas)
-- ============================================================

INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Energia'),
    '¿La transición energética en Colombia debería ser planificada y liderada por el Estado, aunque implique acelerar el cierre de fuentes fósiles?',
    'multiple_choice', 30, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿La transición energética en Colombia debería ser planificada y liderada por el Estado, aunque implique acelerar el cierre de fuentes fósiles?'), 'Muy en desacuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La transición energética en Colombia debería ser planificada y liderada por el Estado, aunque implique acelerar el cierre de fuentes fósiles?'), 'En desacuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La transición energética en Colombia debería ser planificada y liderada por el Estado, aunque implique acelerar el cierre de fuentes fósiles?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La transición energética en Colombia debería ser planificada y liderada por el Estado, aunque implique acelerar el cierre de fuentes fósiles?'), 'De acuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La transición energética en Colombia debería ser planificada y liderada por el Estado, aunque implique acelerar el cierre de fuentes fósiles?'), 'Muy de acuerdo', 1, NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Energia'),
    '¿La matriz energética colombiana debería mantenerse principalmente basada en hidroeléctricas, gas y carbón, dejando que el mercado defina el ritmo de incorporación de energías renovables?',
    'multiple_choice', 31, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿La matriz energética colombiana debería mantenerse principalmente basada en hidroeléctricas, gas y carbón, dejando que el mercado defina el ritmo de incorporación de energías renovables?'), 'Muy de acuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La matriz energética colombiana debería mantenerse principalmente basada en hidroeléctricas, gas y carbón, dejando que el mercado defina el ritmo de incorporación de energías renovables?'), 'De acuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La matriz energética colombiana debería mantenerse principalmente basada en hidroeléctricas, gas y carbón, dejando que el mercado defina el ritmo de incorporación de energías renovables?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La matriz energética colombiana debería mantenerse principalmente basada en hidroeléctricas, gas y carbón, dejando que el mercado defina el ritmo de incorporación de energías renovables?'), 'En desacuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La matriz energética colombiana debería mantenerse principalmente basada en hidroeléctricas, gas y carbón, dejando que el mercado defina el ritmo de incorporación de energías renovables?'), 'Muy en desacuerdo', 1, NOW(), NOW());


-- ============================================================
-- POLÍTICA EXTERIOR (2 preguntas)
-- ============================================================

INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Política exterior'),
    '¿Colombia debería diversificar sus relaciones internacionales fortaleciendo vínculos con América Latina, BRICS y el Sur Global, en lugar de mantener una alineación prioritaria con Estados Unidos?',
    'multiple_choice', 32, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿Colombia debería diversificar sus relaciones internacionales fortaleciendo vínculos con América Latina, BRICS y el Sur Global, en lugar de mantener una alineación prioritaria con Estados Unidos?'), 'Muy en desacuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Colombia debería diversificar sus relaciones internacionales fortaleciendo vínculos con América Latina, BRICS y el Sur Global, en lugar de mantener una alineación prioritaria con Estados Unidos?'), 'En desacuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Colombia debería diversificar sus relaciones internacionales fortaleciendo vínculos con América Latina, BRICS y el Sur Global, en lugar de mantener una alineación prioritaria con Estados Unidos?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Colombia debería diversificar sus relaciones internacionales fortaleciendo vínculos con América Latina, BRICS y el Sur Global, en lugar de mantener una alineación prioritaria con Estados Unidos?'), 'De acuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Colombia debería diversificar sus relaciones internacionales fortaleciendo vínculos con América Latina, BRICS y el Sur Global, en lugar de mantener una alineación prioritaria con Estados Unidos?'), 'Muy de acuerdo', 1, NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Política exterior'),
    '¿La relación estratégica con Estados Unidos en materia de seguridad, comercio y lucha antinarcóticos debe seguir siendo el eje principal de la política exterior colombiana?',
    'multiple_choice', 33, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿La relación estratégica con Estados Unidos en materia de seguridad, comercio y lucha antinarcóticos debe seguir siendo el eje principal de la política exterior colombiana?'), 'Muy de acuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La relación estratégica con Estados Unidos en materia de seguridad, comercio y lucha antinarcóticos debe seguir siendo el eje principal de la política exterior colombiana?'), 'De acuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La relación estratégica con Estados Unidos en materia de seguridad, comercio y lucha antinarcóticos debe seguir siendo el eje principal de la política exterior colombiana?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La relación estratégica con Estados Unidos en materia de seguridad, comercio y lucha antinarcóticos debe seguir siendo el eje principal de la política exterior colombiana?'), 'En desacuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿La relación estratégica con Estados Unidos en materia de seguridad, comercio y lucha antinarcóticos debe seguir siendo el eje principal de la política exterior colombiana?'), 'Muy en desacuerdo', 1, NOW(), NOW());


-- ============================================================
-- TECNOLOGÍA (2 preguntas)
-- ============================================================

INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Tecnología'),
    '¿Colombia debería desarrollar capacidades estatales propias en infraestructura digital y datos (nube soberana, regulación fuerte a plataformas), en lugar de depender principalmente de la inversión privada extranjera?',
    'multiple_choice', 34, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿Colombia debería desarrollar capacidades estatales propias en infraestructura digital y datos (nube soberana, regulación fuerte a plataformas), en lugar de depender principalmente de la inversión privada extranjera?'), 'Muy en desacuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Colombia debería desarrollar capacidades estatales propias en infraestructura digital y datos (nube soberana, regulación fuerte a plataformas), en lugar de depender principalmente de la inversión privada extranjera?'), 'En desacuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Colombia debería desarrollar capacidades estatales propias en infraestructura digital y datos (nube soberana, regulación fuerte a plataformas), en lugar de depender principalmente de la inversión privada extranjera?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Colombia debería desarrollar capacidades estatales propias en infraestructura digital y datos (nube soberana, regulación fuerte a plataformas), en lugar de depender principalmente de la inversión privada extranjera?'), 'De acuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Colombia debería desarrollar capacidades estatales propias en infraestructura digital y datos (nube soberana, regulación fuerte a plataformas), en lugar de depender principalmente de la inversión privada extranjera?'), 'Muy de acuerdo', 1, NOW(), NOW());


INSERT INTO questions (test_id, category_id, title, type_question, question_order, is_active, created_at, updated_at)
VALUES (
    (SELECT id FROM tests WHERE title = '¿Quién es tu candidato ideal?'),
    (SELECT id FROM categories WHERE name LIKE 'Tecnología'),
    '¿Para impulsar el ecosistema tecnológico, Colombia debería abrir el mercado a empresas globales con incentivos tributarios y mínima regulación, aprovechando la inversión privada extranjera?',
    'multiple_choice', 35, true, NOW(), NOW()
);

INSERT INTO response_options (question_id, title, value, created_at, updated_at) VALUES
((SELECT id FROM questions WHERE title = '¿Para impulsar el ecosistema tecnológico, Colombia debería abrir el mercado a empresas globales con incentivos tributarios y mínima regulación, aprovechando la inversión privada extranjera?'), 'Muy de acuerdo', -1, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Para impulsar el ecosistema tecnológico, Colombia debería abrir el mercado a empresas globales con incentivos tributarios y mínima regulación, aprovechando la inversión privada extranjera?'), 'De acuerdo', -0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Para impulsar el ecosistema tecnológico, Colombia debería abrir el mercado a empresas globales con incentivos tributarios y mínima regulación, aprovechando la inversión privada extranjera?'), 'Neutral', 0, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Para impulsar el ecosistema tecnológico, Colombia debería abrir el mercado a empresas globales con incentivos tributarios y mínima regulación, aprovechando la inversión privada extranjera?'), 'En desacuerdo', 0.5, NOW(), NOW()),
((SELECT id FROM questions WHERE title = '¿Para impulsar el ecosistema tecnológico, Colombia debería abrir el mercado a empresas globales con incentivos tributarios y mínima regulación, aprovechando la inversión privada extranjera?'), 'Muy en desacuerdo', 1, NOW(), NOW());


COMMIT;