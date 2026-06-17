-- =============================================================================
-- Seed: questions + response_options (segunda vuelta 2026)
-- Cepeda (12) + De la Espriella (12) = 24 preguntas, 72 opciones
--
-- Reglas:
--   value (fijo):  De acuerdo = 1 | Neutral = 0 | Desacuerdo = -1
--   programmatic_alignment_value: tomado del Excel (Valor opción 1/2/3)
--   type_question: 'multiple_choice'  (cambiar a 'only_option' si aplica)
--
-- NOTA: ajusta @test_id y verifica que las columnas usadas en las
-- subconsultas (candidates.name, categories.name) existan en tu esquema.
-- Asume que la tabla `questions` arranca con los IDs 1..24 libres.
-- =============================================================================

START TRANSACTION;

INSERT INTO `tests` (`id`, `created_at`, `updated_at`, `deleted_at`, `name`, `description`, `image_url`, `type`) VALUES
(4, '2026-06-16 21:28:16', '2026-06-16 21:28:16', NULL, 'El Cara a Cara', 'Si en la primera etapa buscamos a tu \"Candidato Ideal\" entre todas las alternativas, hoy te invitamos a poner sus propuestas bajo la lupa en este cara a cara definitivo. Responde estas preguntas sobre los temas más cruciales para el país y descubre cuál de los dos finalistas se alinea mejor con tus ideas y valores en esta recta final.', 'https://img.luifereduardoo.com/elegio/foto-test-segunda-vuelta.webp', 'PROGRAMMATIC_ALIGNMENT');


-- ---------- Configuración ----------------------------------------------------
SET @test_id = 4;

-- Candidatos
SET @cand_cepeda    = (SELECT id FROM candidates WHERE presidential_candidate = 'Iván Cepeda Castro' LIMIT 1);
SET @cand_espriella = (SELECT id FROM candidates WHERE presidential_candidate = 'Abelardo Gabriel de la Espriella' LIMIT 1);

-- Categorías
SET @cat_paz            = (SELECT id FROM categories WHERE name = 'Paz' LIMIT 1);
SET @cat_hidrocarburos  = (SELECT id FROM categories WHERE name = 'Hidrocarburos' LIMIT 1);
SET @cat_empresas       = (SELECT id FROM categories WHERE name = 'Empresas' LIMIT 1);
SET @cat_salud          = (SELECT id FROM categories WHERE name = 'Salud' LIMIT 1);
SET @cat_seguridad      = (SELECT id FROM categories WHERE name = 'Seguridad' LIMIT 1);
SET @cat_corrupcion     = (SELECT id FROM categories WHERE name = 'Corrupción' LIMIT 1);
SET @cat_energia        = (SELECT id FROM categories WHERE name = 'Energia' LIMIT 1);
SET @cat_economia       = (SELECT id FROM categories WHERE name = 'Economía' LIMIT 1);
SET @cat_educacion      = (SELECT id FROM categories WHERE name = 'Educación' LIMIT 1);
SET @cat_agraria        = (SELECT id FROM categories WHERE name = 'Agraria' LIMIT 1);
SET @cat_transf_social  = (SELECT id FROM categories WHERE name = 'Tranformación social' LIMIT 1);

-- =============================================================================
-- QUESTIONS
-- =============================================================================
INSERT INTO questions
    (id, test_id, category_id, candidate_id, title, description,
     type_question, question_order, is_active, created_at, updated_at)
VALUES
-- ----- Iván Cepeda Castro --------------------------------------------------
(1, @test_id, @cat_paz, @cand_cepeda,
 '¿Está de acuerdo con seguir dialogando con los grupos al margen de la ley?',
 'El programa no renuncia al deber constitucional de buscar la paz y plantea diálogos "eficaces", orientados a resultados verificables y medibles. Establece una línea roja innegociable: respeto a la población civil, la niñez y los liderazgos sociales, sin permitir que el diálogo sea usado para el fortalecimiento militar o económico de las organizaciones armadas.',
 'multiple_choice', 1, 1, NOW(), NOW()),

(2, @test_id, @cat_hidrocarburos, @cand_cepeda,
 '¿Apoya la prohibición total del fracking?',
 'El documento rechaza el modelo extractivista y menciona el fracking, la minería ilegal y la deforestación como prácticas que destruyen ecosistemas y deben superarse. Propone reducir la dependencia de fósiles y avanzar hacia una matriz limpia, en línea con la oposición a la fractura hidráulica.',
 'multiple_choice', 2, 1, NOW(), NOW()),

(3, @test_id, @cat_hidrocarburos, @cand_cepeda,
 '¿Apoya la reducción progresiva de la dependencia del petróleo y el carbón hacia una matriz energética más limpia, sin volver a concentrar el desarrollo en exportación de materias primas?',
 'Plantea una transición energética justa y soberana que reduzca gradualmente la dependencia del petróleo y el carbón, sin volver a concentrar el desarrollo en la exportación de materias primas. Defiende a Ecopetrol como empresa multienergética y apuesta por solar y eólica como base de un nuevo modelo productivo.',
 'multiple_choice', 3, 1, NOW(), NOW()),

(4, @test_id, @cat_empresas, @cand_cepeda,
 '¿Está de acuerdo con hacer compras públicas como herramienta de política industrial priorizando producción nacional y economías populares?',
 'Propone reformar la Ley 80 para transformar las compras estatales en un instrumento de fomento sectorial y territorial, priorizando la producción nacional, las economías populares y campesinas, y permitiendo que organizaciones comunitarias sean sujetos directos de contratación.',
 'multiple_choice', 4, 1, NOW(), NOW()),

(5, @test_id, @cat_salud, @cand_cepeda,
 '¿Apoya revertir la privatización del sistema de salud?',
 'Critica el modelo de la Ley 100 por mercantilizar el servicio y propone un sistema mixto con rectoría del Estado, basado en Atención Primaria, giro directo a hospitales y eliminación de la intermediación que extrae recursos, recuperando lo público frente al lucro.',
 'multiple_choice', 5, 1, NOW(), NOW()),

(6, @test_id, @cat_seguridad, @cand_cepeda,
 '¿Está de acuerdo con la política de seguridad humana integral orientada a transformación territorial y protección de la vida?',
 'Plantea una seguridad humana integral cuyo éxito no se mide por bajas o capturas, sino por la reducción de violencias y la protección de la población. Combina presencia estatal, oportunidades, dignificación de la Fuerza Pública y ataque a las finanzas criminales.',
 'multiple_choice', 6, 1, NOW(), NOW()),

(7, @test_id, @cat_corrupcion, @cand_cepeda,
 '¿Apoya la creación de un sistema nacional contra la Macrocorrupción que actúe de forma integral para desmantelar redes, garantizar justicia y devolver al Estado cada peso robado?',
 'Propone un Sistema Nacional contra la Macrocorrupción que desmantele redes de forma integral, una Unidad de Investigación en la Fiscalía para perseguir a los determinadores, tipificar la gran corrupción como criminalidad organizada y devolver al Estado los recursos robados vía el Fondo de Reparación de Víctimas de la Corrupción.',
 'multiple_choice', 7, 1, NOW(), NOW()),

(8, @test_id, @cat_energia, @cand_cepeda,
 '¿Estaría de acuerdo con reformar la Ley 142 de 1994 para garantizar la energía como un derecho fundamental y no como una mercancía?',
 'Propone reformar la Ley 142 de 1994 por considerarla diseñada para privilegiar el mercado y a las empresas privadas sobre los usuarios, de modo que el acceso a la energía deje de ser un negocio y se garantice como derecho fundamental para toda la población.',
 'multiple_choice', 8, 1, NOW(), NOW()),

(9, @test_id, @cat_economia, @cand_cepeda,
 '¿Estaría de acuerdo con estructurar tres pactos nacionales (productivo, social y fiscal) para transformar la economía hacia la industrialización y el conocimiento, financiando con ello la duplicación de la Renta Ciudadana y la creación de un Sistema Nacional del Cuidado?',
 'Propone tres pactos —productivo, social y fiscal. Banca pública reformada (Grupo Bicentenario: Bancóldex, FINAGRO, Banco Agrario, FNA, Findeter) con crédito de fomento, créditos asociativos y verdes, e inclusión financiera. Pacto social: salario mínimo con incrementos reales atados a productividad y costo de vida; formalización laboral; eliminación de intermediación laboral ilegal; reducir aporte a salud de pensionados al 4%; defensoría pública laboral; marco regulatorio para trabajo en plataformas. Pacto fiscal: presupuestos programáticos con metas medibles; revisión del estatuto tributario eliminando exenciones injustificadas; mayor tributación a altas rentas y grandes patrimonios; fiscalidad digital a grandes plataformas; fortalecer la DIAN; catastro multipropósito e impuesto predial; estabilización gradual de la deuda.',
 'multiple_choice', 9, 1, NOW(), NOW()),

(10, @test_id, @cat_educacion, @cand_cepeda,
 '¿Apoya aprobar una Ley Estatutaria de la Educación que la convierta en un derecho fundamental e irrenunciable, aplicando un modelo de financiación que inyecte más recursos públicos a los colegios y universidades de las regiones más necesitadas?',
 'Impulsa la Ley Estatutaria de la Educación y un modelo de financiación diferencial que reconozca las necesidades de los territorios, con cofinanciación Nación–territorios para colegios y universidades de las regiones más excluidas, además de gratuidad y multicampus en zonas rurales.',
 'multiple_choice', 10, 1, NOW(), NOW()),

(11, @test_id, @cat_agraria, @cand_cepeda,
 '¿Estaría de acuerdo con impulsar una Revolución Agraria que redistribuya un millón de hectáreas adicionales de tierra y cree una Alianza Nacional Alimentaria para comprar cosechas directamente al campesinado sin intermediarios, abasteciendo los programas del Estado?',
 'Propone añadir un millón de hectáreas a las gestionadas por el gobierno Petro y ponerlas a producir, junto con la Alianza Nacional Alimentaria (ANA), entidad público-privado-popular que compra directo al campesinado, elimina intermediarios y abastece programas como el PAE.',
 'multiple_choice', 11, 1, NOW(), NOW()),

(12, @test_id, @cat_transf_social, @cand_cepeda,
 '¿Estaría de acuerdo con poner en marcha una Estrategia Nacional contra el Feminicidio y juzgados especializados, financiando la independencia económica de las mujeres a través del Fondo Mujer Libre y Productiva y la infraestructura del Sistema Nacional del Cuidado?',
 'Plantea consolidar la Estrategia Nacional contra el Feminicidio (ENAF 2026-2030), crear tribunales especializados y fortalecer el sistema SALVIA, financiando la autonomía económica de las mujeres mediante el Fondo Mujer Libre y Productiva y la infraestructura del Sistema Nacional del Cuidado.',
 'multiple_choice', 12, 1, NOW(), NOW()),

-- ----- Abelardo Gabriel de la Espriella ------------------------------------
(13, @test_id, @cat_paz, @cand_espriella,
 '¿Apoya impone la paz con la fuerza de las armas y las leyes de la República?',
 'El programa rechaza la negociación con criminales y califica la "Paz Total" como una traición a la Patria. Plantea recuperar la paz reafirmando el monopolio estatal de las armas, desmontando milicias y poderes coercitivos paralelos, y recuperando el control territorial mediante la Fuerza Pública y el cumplimiento estricto de la ley.',
 'multiple_choice', 1, 1, NOW(), NOW()),

(14, @test_id, @cat_hidrocarburos, @cand_espriella,
 '¿Apoya al fracking, siempre y cuando se realice de manera responsable y con respeto por el medio ambiente?',
 'Ante la pérdida de autosuficiencia energética y la caída de reservas, la propuesta busca recuperar la producción de petróleo y gas con seguridad jurídica y criterio técnico. Esto incluye evaluar con rigor los yacimientos no convencionales (fracking) como parte de tratar el gas como un asunto estratégico para el país.',
 'multiple_choice', 2, 1, NOW(), NOW()),

(15, @test_id, @cat_corrupcion, @cand_espriella,
 '¿Se encuentra de acuerdo que todas las contrataciones publicas se hagan mediante blockchain?',
 'Como medida anticorrupción, se propone que a 2030 todos los procesos de contratación pública se realicen mediante blockchain. El objetivo es que la información registrada no pueda ser modificada por nadie, garantizando trazabilidad, transparencia y menos discrecionalidad en el manejo de los recursos públicos.',
 'multiple_choice', 3, 1, NOW(), NOW()),

(16, @test_id, @cat_economia, @cand_espriella,
 '¿Estaría de acuerdo con impulsar un crecimiento económico del 7% anual mediante una Gran Revolución de Desregulación que elimine trabas burocráticas, reduciendo a su vez el tamaño del Estado en una cuarta parte para sanar las finanzas públicas?',
 'La propuesta busca pasar de "administrar escasez a desatar abundancia", aspirando a crecer al 7% anual como Corea del Sur o Singapur. Para ello plantea ordenar las finanzas públicas reduciendo el tamaño del Estado hasta en una cuarta parte y una "Gran Revolución de DesRegulación" que elimine trámites, trabas y cargas al sector empresarial.',
 'multiple_choice', 4, 1, NOW(), NOW()),

(17, @test_id, @cat_agraria, @cand_espriella,
 '¿Estaría de acuerdo con expandir la frontera productiva en más de 3 millones de hectáreas para generar empleos rurales, entregando la propiedad de la tierra al campesinado y formando a jóvenes mediante una Escuela de Emprendedores Rurales con tecnología y crédito?',
 'Frente al abandono del campo, se propone volver propietario al campesino y expandir la frontera productiva (2 millones de nuevas hectáreas más 1,5 millones agrícolas) para generar más de 600.000 empleos rurales. Incluye crear la Escuela de Emprendedores Rurales para formar a jóvenes con tecnología, crédito, asociatividad y mentoría.',
 'multiple_choice', 5, 1, NOW(), NOW()),

(18, @test_id, @cat_seguridad, @cand_espriella,
 '¿Estaría de acuerdo con la construcción de diez megacárceles de máxima seguridad en zonas aisladas y sin señal de telecomunicaciones para aislar a los reclusos de las redes criminales externas?',
 'Dentro de la estrategia de seguridad, el programa plantea recuperar el sistema carcelario para cortar el vínculo entre los reclusos y las redes criminales externas. La construcción de megacárceles aisladas y sin señal busca impedir que las estructuras delictivas sigan operando desde prisión.',
 'multiple_choice', 6, 1, NOW(), NOW()),

(19, @test_id, @cat_seguridad, @cand_espriella,
 '¿Se encuentra de acuerdo con crear un Bloque de Búsqueda contra la Extorsión respaldado por una Primera Línea de Seguridad conformada por veteranos y reservistas de las Fuerzas Armadas para recuperar la tranquilidad en los barrios?',
 'Para enfrentar las 12.180 extorsiones registradas y recuperar la seguridad en los barrios, se propone un Bloque de Búsqueda contra la Extorsión. Este se complementaría con una Primera Línea de Seguridad conformada por veteranos y reservistas de las Fuerzas Armadas, llevando la seguridad directamente al nivel barrial.',
 'multiple_choice', 7, 1, NOW(), NOW()),

(20, @test_id, @cat_transf_social, @cand_espriella,
 '¿Estaría de acuerdo con declarar la violencia contra la mujer como una prioridad de orden público para resolver rutas judiciales en menos de 72 horas?',
 'Partiendo de que el país "descansa sobre las mujeres pero no las protege", se propone enfrentar la violencia de género como un problema prioritario de orden público. Esto incluye rutas judiciales aceleradas en un máximo de 72 horas, atención psicológica y jurídica 24/7, y la meta de reducir los feminicidios en un 30%.',
 'multiple_choice', 8, 1, NOW(), NOW()),

(21, @test_id, @cat_empresas, @cand_espriella,
 '¿Estaría de acuerdo con ejecutar una desregulación masiva que elimine trámites ineficientes, y simplificar la estructura tributaria para incentivar la inversión privada?',
 'La propuesta busca aliviar al sector productivo eliminando ineficiencias en entidades como Invima, ICA, DIAN, superintendencias y notariado. Plantea simplificar la estructura tributaria y aplicar la política "Una entra y dos salen" (por cada nueva regulación se eliminan dos) para incentivar la inversión privada y reactivar la economía.',
 'multiple_choice', 9, 1, NOW(), NOW()),

(22, @test_id, @cat_salud, @cand_espriella,
 '¿Se encuentra de acuerdo con ejecutar un plan de choque para restablecer el flujo de recursos y garantizar el acceso oportuno a medicamentos, auditando estrictamente el uso de la UPC por parte de las EPS para poner fin al desvío de dinero?',
 'Ante la crisis humanitaria en salud y los fallecimientos por falta de atención, se propone un plan de choque de $10 billones. Busca restablecer el flujo de recursos, garantizar el acceso oportuno a medicamentos y revisar trimestralmente la ejecución de la UPC por parte de las EPS para frenar el desvío de dinero.',
 'multiple_choice', 10, 1, NOW(), NOW()),

(23, @test_id, @cat_energia, @cand_espriella,
 '¿Está de acuerdo con reducir los costos de las tarifas mediante licencias exprés para energías renovables, autosuficiencia energética y la implementación de una política de energía nuclear?',
 'Para reducir los altos costos de energía, el programa apuesta por la autosuficiencia energética y el desarrollo de energías renovables y nuevas energías. Esto incluye una política de energía nuclear y licenciamientos express que aceleren los proyectos, además de transformar el sistema eléctrico de la Costa Caribe.',
 'multiple_choice', 11, 1, NOW(), NOW()),

(24, @test_id, @cat_educacion, @cand_espriella,
 '¿Estaría de acuerdo con crear la Universidad Virtual en Casa con conectividad y computadores gratuitos, implementando ciclos cortos enfocados en bilingüismo y tecnologías de la cuarta revolución industrial (como IA y robótica)?',
 'Frente a la desigualdad educativa y la baja cobertura en educación superior, se propone crear la Universidad Virtual en Casa con conectividad y computadores gratuitos. Se acompaña de ciclos cortos formativos en bilingüismo y tecnologías de la cuarta revolución industrial (IA, robótica, computación cuántica) para formar jóvenes productivos.',
 'multiple_choice', 12, 1, NOW(), NOW());

-- =============================================================================
-- RESPONSE_OPTIONS
--   value:  De acuerdo=1 | Neutral=0 | Desacuerdo=-1
--   programmatic_alignment_value: del Excel
-- =============================================================================
INSERT INTO response_options
    (question_id, title, value, programmatic_alignment_value, created_at, updated_at)
VALUES
-- ----- Cepeda --------------------------------------------------------------
(1,  'De acuerdo',  1,  0.5,   NOW(), NOW()),
(1,  'Neutral',     0,  0,     NOW(), NOW()),
(1,  'Desacuerdo', -1, -0.5,   NOW(), NOW()),

(2,  'De acuerdo',  1,  0.75,  NOW(), NOW()),
(2,  'Neutral',     0,  0,     NOW(), NOW()),
(2,  'Desacuerdo', -1, -0.75,  NOW(), NOW()),

(3,  'De acuerdo',  1,  0.5,   NOW(), NOW()),
(3,  'Neutral',     0,  0,     NOW(), NOW()),
(3,  'Desacuerdo', -1, -0.5,   NOW(), NOW()),

(4,  'De acuerdo',  1,  0.75,  NOW(), NOW()),
(4,  'Neutral',     0,  0,     NOW(), NOW()),
(4,  'Desacuerdo', -1, -0.75,  NOW(), NOW()),

(5,  'De acuerdo',  1,  0.75,  NOW(), NOW()),
(5,  'Neutral',     0,  0,     NOW(), NOW()),
(5,  'Desacuerdo', -1, -0.75,  NOW(), NOW()),

(6,  'De acuerdo',  1,  0.75,  NOW(), NOW()),
(6,  'Neutral',     0,  0,     NOW(), NOW()),
(6,  'Desacuerdo', -1, -0.75,  NOW(), NOW()),

(7,  'De acuerdo',  1, -0.5,   NOW(), NOW()),
(7,  'Neutral',     0,  0,     NOW(), NOW()),
(7,  'Desacuerdo', -1,  0.5,   NOW(), NOW()),

(8,  'De acuerdo',  1,  0.25,  NOW(), NOW()),
(8,  'Neutral',     0,  0,     NOW(), NOW()),
(8,  'Desacuerdo', -1, -0.25,  NOW(), NOW()),

(9,  'De acuerdo',  1,  0.75,  NOW(), NOW()),
(9,  'Neutral',     0,  0,     NOW(), NOW()),
(9,  'Desacuerdo', -1, -0.75,  NOW(), NOW()),

(10, 'De acuerdo',  1,  0.75,  NOW(), NOW()),
(10, 'Neutral',     0,  0,     NOW(), NOW()),
(10, 'Desacuerdo', -1, -0.75,  NOW(), NOW()),

(11, 'De acuerdo',  1,  0.75,  NOW(), NOW()),
(11, 'Neutral',     0,  0,     NOW(), NOW()),
(11, 'Desacuerdo', -1, -0.75,  NOW(), NOW()),

(12, 'De acuerdo',  1,  0.75,  NOW(), NOW()),
(12, 'Neutral',     0,  0,     NOW(), NOW()),
(12, 'Desacuerdo', -1, -0.75,  NOW(), NOW()),

-- ----- De la Espriella -----------------------------------------------------
(13, 'De acuerdo',  1, -0.75,  NOW(), NOW()),
(13, 'Neutral',     0,  0,     NOW(), NOW()),
(13, 'Desacuerdo', -1,  0.75,  NOW(), NOW()),

(14, 'De acuerdo',  1, -0.75,  NOW(), NOW()),
(14, 'Neutral',     0,  0,     NOW(), NOW()),
(14, 'Desacuerdo', -1,  0.75,  NOW(), NOW()),

(15, 'De acuerdo',  1,  0.5,   NOW(), NOW()),
(15, 'Neutral',     0,  0,     NOW(), NOW()),
(15, 'Desacuerdo', -1, -0.5,   NOW(), NOW()),

(16, 'De acuerdo',  1, -1,     NOW(), NOW()),
(16, 'Neutral',     0,  0,     NOW(), NOW()),
(16, 'Desacuerdo', -1,  1,     NOW(), NOW()),

(17, 'De acuerdo',  1,  0.5,   NOW(), NOW()),
(17, 'Neutral',     0,  0,     NOW(), NOW()),
(17, 'Desacuerdo', -1, -0.5,   NOW(), NOW()),

(18, 'De acuerdo',  1, -0.75,  NOW(), NOW()),
(18, 'Neutral',     0,  0,     NOW(), NOW()),
(18, 'Desacuerdo', -1,  0.75,  NOW(), NOW()),

(19, 'De acuerdo',  1, -0.75,  NOW(), NOW()),
(19, 'Neutral',     0,  0,     NOW(), NOW()),
(19, 'Desacuerdo', -1,  0.75,  NOW(), NOW()),

(20, 'De acuerdo',  1,  0.25,  NOW(), NOW()),
(20, 'Neutral',     0,  0,     NOW(), NOW()),
(20, 'Desacuerdo', -1, -0.25,  NOW(), NOW()),

(21, 'De acuerdo',  1, -0.75,  NOW(), NOW()),
(21, 'Neutral',     0,  0,     NOW(), NOW()),
(21, 'Desacuerdo', -1,  0.75,  NOW(), NOW()),

(22, 'De acuerdo',  1, -0.25,  NOW(), NOW()),
(22, 'Neutral',     0,  0,     NOW(), NOW()),
(22, 'Desacuerdo', -1,  0.25,  NOW(), NOW()),

(23, 'De acuerdo',  1, -0.25,  NOW(), NOW()),
(23, 'Neutral',     0,  0,     NOW(), NOW()),
(23, 'Desacuerdo', -1,  0.25,  NOW(), NOW()),

(24, 'De acuerdo',  1,  0.5,   NOW(), NOW()),
(24, 'Neutral',     0,  0,     NOW(), NOW()),
(24, 'Desacuerdo', -1, -0.5,   NOW(), NOW());

-- =============================================================================
-- QUESTIONS
-- =============================================================================
INSERT INTO questions
    (id, test_id, category_id, candidate_id, title, description,
     type_question, question_order, is_active, video_url, created_at, updated_at)
VALUES
(25, @test_id, NULL, @cand_espriella,
 '¿Qué le genera este video?',
 NULL,
 'video_emotion_slider', 1, 1,
 'https://www.tiktok.com/@politendencia/video/7639411520744459521?q=abelardo%20hazle%20zoom%20a%20la%20foto&t=1781673728098',
 NOW(), NOW()),
 
(26, @test_id, NULL, @cand_cepeda,
 '¿Qué le genera este video?',
 NULL,
 'video_emotion_slider', 2, 1,
 'https://www.tiktok.com/@adiarioporlalibertad/video/7648682041407589640?q=aida%20quilcue&t=1781673899579',
 NOW(), NOW());

COMMIT;