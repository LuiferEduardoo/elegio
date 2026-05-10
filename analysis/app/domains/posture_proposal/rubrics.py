RUBRICS = {
    "corrupcion": {
        "polo_negativo": {
            "nombre": "punitivo",
            "descripcion": "endurecimiento penal y sanción ejemplar como eje"
        },
        "polo_positivo": {
            "nombre": "preventivo-participativo",
            "descripcion": "transparencia, datos abiertos y participación ciudadana como eje"
        },
        "anclajes": {
            -1.0: "Centra la lucha anticorrupción en penas más severas, "
                  "cárcel sin beneficios, muerte civil, o medidas penales "
                  "como respuesta principal.",
            -0.5: "Énfasis en sanción y persecución penal, con menciones "
                  "secundarias a transparencia.",
             0.0: "Mezcla sanción y prevención sin prioridad clara, o "
                  "propuestas genéricas sin mecanismo concreto.",
            +0.5: "Énfasis en transparencia, datos abiertos y contratación "
                  "pública abierta, con sanción como complemento.",
            +1.0: "Centra la lucha anticorrupción en participación "
                  "ciudadana, veedurías, presupuestos abiertos, rendición "
                  "de cuentas y prevención sistémica.",
        }
    },

    "paz": {
        "polo_negativo": {
            "nombre": "seguridad-orden",
            "descripcion": "fuerza pública y operaciones militares como vía principal"
        },
        "polo_positivo": {
            "nombre": "negociacion-justicia-transicional",
            "descripcion": "diálogo, acuerdos y justicia restaurativa como vía principal"
        },
        "anclajes": {
            -1.0: "Rechaza negociación con grupos armados, propone revisar "
                  "o desmontar acuerdos existentes, prioriza operaciones "
                  "militares.",
            -0.5: "Énfasis en autoridad y fuerza pública; negociación solo "
                  "bajo sometimiento o condiciones muy estrictas.",
             0.0: "Combina ambos enfoques sin prioridad clara.",
            +0.5: "Apoya implementación del Acuerdo de 2016 y diálogo "
                  "selectivo con ciertos actores.",
            +1.0: "Promueve paz total, negociación con todos los actores "
                  "armados, enfoque de justicia restaurativa y reformas "
                  "estructurales.",
        }
    },

    "economia": {
        "polo_negativo": {
            "nombre": "mercado",
            "descripcion": "libre mercado, disciplina fiscal y Estado mínimo"
        },
        "polo_positivo": {
            "nombre": "intervencion-estatal",
            "descripcion": "Estado activo, redistribución y política industrial"
        },
        "anclajes": {
            -1.0: "Reducción del Estado, recorte del gasto, reducción de "
                  "impuestos, desregulación, austeridad fiscal.",
            -0.5: "Inclinación al mercado con regulación mínima; ajuste "
                  "fiscal moderado.",
             0.0: "Economía mixta sin énfasis claro, o propuestas vagas.",
            +0.5: "Estado activo en sectores estratégicos, política "
                  "industrial, gasto social ampliado, reforma tributaria "
                  "progresiva moderada.",
            +1.0: "Estado como actor económico central, redistribución "
                  "fuerte, control de precios, reforma tributaria profunda, "
                  "renta básica o transferencias amplias.",
        }
    },

    "agraria": {
        "polo_negativo": {
            "nombre": "agroindustrial",
            "descripcion": "agroindustria, productividad y titulación de mercado"
        },
        "polo_positivo": {
            "nombre": "reforma-rural-campesina",
            "descripcion": "reforma agraria, economía campesina y redistribución de tierra"
        },
        "anclajes": {
            -1.0: "Prioriza agroindustria, ZIDRES, grandes proyectos "
                  "productivos, titulación individual con lógica de mercado.",
            -0.5: "Apoyo al pequeño productor dentro de un modelo "
                  "agroindustrial dominante.",
             0.0: "Combina ambos modelos sin prioridad clara.",
            +0.5: "Fortalece economía campesina, asociatividad, compras "
                  "públicas locales, sin redistribución profunda de tierra.",
            +1.0: "Reforma agraria integral, redistribución de tierra, "
                  "territorios campesinos, soberanía alimentaria como eje.",
        }
    },

    "seguridad": {
        "polo_negativo": {
            "nombre": "punitivo-militarizado",
            "descripcion": "mano dura, aumento de penas y militarización"
        },
        "polo_positivo": {
            "nombre": "preventivo-derechos",
            "descripcion": "prevención social, DDHH y seguridad humana"
        },
        "anclajes": {
            -1.0: "Aumento de penas, militarización urbana, reducción de "
                  "garantías procesales, estado de excepción.",
            -0.5: "Énfasis en autoridad y fuerza pública con menciones "
                  "secundarias a prevención.",
             0.0: "Mezcla represión y prevención sin prioridad clara.",
            +0.5: "Énfasis en policía comunitaria, prevención del delito, "
                  "intervención social en territorios.",
            +1.0: "Seguridad humana integral, desmilitarización, "
                  "intervención socioeconómica como eje, reforma policial "
                  "con enfoque de DDHH.",
        }
    },

    "hidrocarburos": {
        "polo_negativo": {
            "nombre": "expansion-extractiva",
            "descripcion": "expansión de exploración y producción"
        },
        "polo_positivo": {
            "nombre": "transicion-acelerada",
            "descripcion": "no nuevos contratos y salida del extractivismo"
        },
        "anclajes": {
            -1.0: "Promueve nuevos contratos de exploración, fracking, "
                  "expansión costa afuera, hidrocarburos como pilar fiscal "
                  "de largo plazo.",
            -0.5: "Mantiene la producción actual y abre algunos nuevos "
                  "contratos con criterios ambientales.",
             0.0: "No se pronuncia claramente o mezcla expansión y "
                  "transición sin prioridad.",
            +0.5: "Limita nuevos contratos, prioriza diversificación de "
                  "ingresos fiscales, transición ordenada.",
            +1.0: "No firma nuevos contratos de exploración, prohíbe "
                  "fracking, plan explícito de salida del extractivismo.",
        }
    },

    "transformacion_social": {
        "polo_negativo": {
            "nombre": "meritocratico-individual",
            "descripcion": "esfuerzo individual, oportunidades y focalización"
        },
        "polo_positivo": {
            "nombre": "redistributivo-derechos",
            "descripcion": "redistribución, derechos universales y enfoques diferenciales"
        },
        "anclajes": {
            -1.0: "Énfasis en esfuerzo individual, reducción de "
                  "transferencias, focalización estricta, rechazo a "
                  "enfoques diferenciales (género, étnico).",
            -0.5: "Foco en oportunidades y empleo formal como vía "
                  "principal de movilidad; subsidios condicionados.",
             0.0: "Combina ambos enfoques sin prioridad clara.",
            +0.5: "Amplía derechos sociales y reconoce enfoques "
                  "diferenciales como complemento a política universal.",
            +1.0: "Redistribución estructural, derechos sociales "
                  "universales, enfoques de género, étnico, LGBTIQ+ y "
                  "antirracista como eje transversal.",
        }
    },

    "empresas": {
        "polo_negativo": {
            "nombre": "facilitacion-privada",
            "descripcion": "reducción de cargas y desregulación al sector privado"
        },
        "polo_positivo": {
            "nombre": "regulacion-estatal",
            "descripcion": "regulación activa, responsabilidad social y empresa pública"
        },
        "anclajes": {
            -1.0: "Reducción de impuestos a empresas, desregulación "
                  "laboral, flexibilización, privatización de empresas "
                  "estatales.",
            -0.5: "Estímulos al sector privado con regulación mínima; "
                  "mantiene empresas estatales sin expandirlas.",
             0.0: "Mezcla apoyo al privado y regulación sin prioridad "
                  "clara.",
            +0.5: "Regulación activa de prácticas empresariales, "
                  "responsabilidad social, fortalecimiento de empresas "
                  "públicas existentes.",
            +1.0: "Expansión del rol empresarial del Estado, regulación "
                  "fuerte, exigencias laborales y ambientales estrictas, "
                  "nacionalizaciones selectivas.",
        }
    },

    "energia": {
        "polo_negativo": {
            "nombre": "matriz-tradicional",
            "descripcion": "matriz fósil con transición gradual de mercado"
        },
        "polo_positivo": {
            "nombre": "transicion-planificada",
            "descripcion": "transición acelerada con planificación estatal"
        },
        "anclajes": {
            -1.0: "Mantiene matriz fósil como base, transición vista como "
                  "amenaza fiscal, expansión de generación térmica.",
            -0.5: "Transición gradual liderada por el mercado, sin metas "
                  "ambiciosas, mantiene rol importante de fósiles.",
             0.0: "Apoya transición sin definir velocidad ni mecanismos.",
            +0.5: "Transición acelerada con incentivos a renovables, "
                  "metas claras, rol mixto público-privado.",
            +1.0: "Transición rápida planificada por el Estado, "
                  "comunidades energéticas, soberanía energética, "
                  "fortalecimiento de empresas públicas del sector.",
        }
    },

    "educacion": {
        "polo_negativo": {
            "nombre": "mercado-eleccion",
            "descripcion": "subsidios a la demanda, competencia y libertad de elección"
        },
        "polo_positivo": {
            "nombre": "publica-universal",
            "descripcion": "educación pública gratuita y universal como derecho"
        },
        "anclajes": {
            -1.0: "Prioriza vouchers, subsidios a la demanda, expansión de "
                  "educación privada, evaluación punitiva, educación "
                  "superior como inversión privada.",
            -0.5: "Calidad y competencia como ejes; sistema mixto con "
                  "fuerte rol privado.",
             0.0: "Sistema mixto sin énfasis claro.",
            +0.5: "Fortalece educación pública, gratuidad parcial en "
                  "superior, mejora de infraestructura pública.",
            +1.0: "Gratuidad universal en educación superior pública, "
                  "fortalecimiento profundo de lo público en todos los "
                  "niveles, reducción del peso del privado.",
        }
    },

    "infraestructura": {
        "polo_negativo": {
            "nombre": "concesiones-app",
            "descripcion": "concesiones, APP y grandes obras lideradas por privados"
        },
        "polo_positivo": {
            "nombre": "inversion-publica-directa",
            "descripcion": "inversión pública directa y obras de cercanía"
        },
        "anclajes": {
            -1.0: "Modelo basado en concesiones de cuarta y quinta "
                  "generación, APPs como vía principal, peajes como "
                  "financiación.",
            -0.5: "Combina concesiones con inversión pública, con "
                  "prioridad a las primeras.",
             0.0: "Mezcla ambos enfoques sin prioridad clara.",
            +0.5: "Inversión pública directa importante, énfasis en vías "
                  "terciarias y obras regionales, APPs como complemento.",
            +1.0: "Inversión pública como eje, obras de cercanía y "
                  "terciarias prioritarias, revisión o renegociación de "
                  "concesiones, fortalecimiento de empresas públicas "
                  "constructoras.",
        }
    },

    "politica_exterior": {
        "polo_negativo": {
            "nombre": "alineacion-occidental",
            "descripcion": "alineación con EE.UU. y bloque occidental"
        },
        "polo_positivo": {
            "nombre": "diversificacion-sur-global",
            "descripcion": "integración regional y relaciones con Sur Global"
        },
        "anclajes": {
            -1.0: "Alineación estrecha con EE.UU., distancia de Venezuela "
                  "y gobiernos de izquierda regional, prioridad OTAN/"
                  "occidente.",
            -0.5: "Relación preferente con EE.UU. con apertura limitada a "
                  "otros socios.",
             0.0: "Política exterior pragmática sin alineación clara.",
            +0.5: "Diversifica relaciones, fortalece integración "
                  "latinoamericana, mantiene relación con EE.UU.",
            +1.0: "Reorientación hacia Sur Global, integración regional "
                  "como eje, distancia crítica de EE.UU., relaciones con "
                  "China/Rusia/BRICS.",
        }
    },

    "tecnologia": {
        "polo_negativo": {
            "nombre": "apertura-mercado",
            "descripcion": "apertura al mercado global y atracción de inversión privada"
        },
        "polo_positivo": {
            "nombre": "soberania-digital",
            "descripcion": "soberanía digital, regulación fuerte y desarrollo estatal"
        },
        "anclajes": {
            -1.0: "Apertura total a plataformas y proveedores extranjeros, "
                  "incentivos tributarios al sector tecnológico privado, "
                  "regulación mínima.",
            -0.5: "Apertura con regulación ligera de protección de datos.",
             0.0: "Combina apertura y soberanía sin énfasis claro.",
            +0.5: "Regulación activa de plataformas, protección de datos, "
                  "fomento a desarrollo nacional sin restricciones fuertes "
                  "al privado.",
            +1.0: "Soberanía digital como eje, infraestructura pública de "
                  "datos, software libre en el Estado, regulación fuerte "
                  "a Big Tech, desarrollo tecnológico estatal.",
        }
    },

    "territorio": {
        "polo_negativo": {
            "nombre": "centralizacion",
            "descripcion": "centralización fiscal y administrativa"
        },
        "polo_positivo": {
            "nombre": "descentralizacion-autonomia",
            "descripcion": "descentralización, autonomía territorial y enfoque regional"
        },
        "anclajes": {
            -1.0: "Refuerza control central sobre regalías y "
                  "transferencias, decisiones desde Bogotá, debilita "
                  "autoridades locales.",
            -0.5: "Mantiene esquema actual con ajustes menores hacia "
                  "centralización.",
             0.0: "Descentralización mencionada sin mecanismos concretos.",
            +0.5: "Fortalece capacidades locales, mejora distribución de "
                  "regalías, mayor autonomía fiscal regional.",
            +1.0: "Descentralización profunda, regiones administrativas "
                  "y de planificación con poder real, autonomía fiscal y "
                  "política amplia, reconocimiento de territorialidades "
                  "étnicas y campesinas.",
        }
    },

    "naturaleza": {
        "polo_negativo": {
            "nombre": "uso-productivo",
            "descripcion": "uso productivo de recursos con mitigación de mercado"
        },
        "polo_positivo": {
            "nombre": "proteccion-derechos-naturaleza",
            "descripcion": "protección ambiental y derechos de la naturaleza"
        },
        "anclajes": {
            -1.0: "Prioriza uso productivo (minería, ganadería, "
                  "agroindustria) sobre protección, flexibiliza licencias "
                  "ambientales, mecanismos de mercado como única vía.",
            -0.5: "Producción con regulación ambiental moderada, sin "
                  "expansión de áreas protegidas.",
             0.0: "Combina ambos enfoques sin prioridad clara.",
            +0.5: "Expansión de áreas protegidas, regulación ambiental "
                  "más estricta, transición productiva en zonas sensibles.",
            +1.0: "Derechos de la naturaleza, prohibición de minería en "
                  "ecosistemas estratégicos, restauración ecológica masiva, "
                  "protección de líderes ambientales como eje.",
        }
    },

    "salud": {
        "polo_negativo": {
            "nombre": "mercado-aseguramiento",
            "descripcion": "aseguramiento privado en competencia regulada"
        },
        "polo_positivo": {
            "nombre": "publico-unificado",
            "descripcion": "sistema público unificado de prestación directa"
        },
        "anclajes": {
            -1.0: "Fortalece EPS privadas, libre competencia entre "
                  "aseguradores, expansión del rol privado en "
                  "aseguramiento y prestación.",
            -0.5: "Mantiene sistema mixto con énfasis en eficiencia "
                  "privada y regulación ligera.",
             0.0: "Sistema mixto sin inclinación clara, o propuestas "
                  "ambiguas / no se pronuncia.",
            +0.5: "Fortalece lo público (ADRES, hospitales públicos, red "
                  "pública) manteniendo rol privado regulado.",
            +1.0: "Sistema único público, transformación profunda o "
                  "eliminación de EPS, administración y prestación "
                  "estatal como eje.",
        }
    },
}