"""simplify test question wording

Revision ID: a6c2f8d4e1b9
Revises: f0c8a3e2b9d1
Create Date: 2026-05-26 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'a6c2f8d4e1b9'
down_revision: Union[str, None] = 'f0c8a3e2b9d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


QUESTION_TITLES: dict[int, str] = {
    71: '¿Para mejorar la seguridad en las ciudades, preferís más policías y militares en las calles?',
    72: 'Frente a grupos armados y bandas criminales, ¿preferís mano dura militar antes que negociaciones o reintegración?',
    73: '¿Creés que para bajar el delito sirve más invertir en empleo, cultura y oportunidades para jóvenes que aumentar castigos?',
    74: '¿Te gustaría que el sistema de salud fuera manejado directamente por el Estado, sin EPS?',
    75: '¿Creés que las EPS privadas deberían seguir siendo parte central del sistema de salud?',
    76: 'En zonas rurales o apartadas, ¿preferís que el Estado atienda directamente la salud sin intermediarios?',
    77: '¿Para que la economía crezca, el gobierno debería bajar impuestos a las empresas y cuidar más el gasto público?',
    78: '¿El Estado debería manejar directamente sectores clave como energía, telecomunicaciones o minería?',
    79: '¿El gobierno debería ampliar ayudas económicas a familias vulnerables aunque aumente el gasto público?',
    80: '¿El gobierno debería seguir dialogando con grupos armados para buscar acuerdos de paz?',
    81: '¿Creés que la justicia para el conflicto armado debe enfocarse más en reparar a las víctimas que en castigar con cárcel?',
    82: '¿Para combatir la corrupción, preferís castigos más duros y prohibir de por vida que los corruptos vuelvan a cargos públicos?',
    83: '¿Creés que mostrar mejor cómo se gasta la plata pública ayuda más contra la corrupción que solo aumentar penas?',
    84: '¿El país debería priorizar entregar o comprar tierras para campesinos antes que impulsar grandes empresas del agro?',
    85: '¿Creés que los grandes proyectos agroindustriales son la mejor forma de desarrollar el campo colombiano?',
    86: '¿Preferís ayudas económicas más amplias para muchas personas, en vez de subsidios solo para grupos muy específicos?',
    87: '¿Creés que salir adelante depende más del esfuerzo personal que de ayudas o redistribución del Estado?',
    88: '¿Para ayudar a las empresas, el gobierno debería reducir trámites, reglas e impuestos?',
    89: '¿Las grandes empresas deberían tener reglas más estrictas y mayores responsabilidades con las comunidades?',
    90: '¿La universidad pública debería ser gratuita para todos y pagada por el Estado?',
    91: '¿Creés que becas, créditos o apoyos para estudiar en universidades privadas ayudan a ampliar el acceso a la educación?',
    92: '¿Las grandes obras como vías y aeropuertos deberían hacerse principalmente con empresas privadas?',
    93: '¿El Estado debería invertir primero en obras cercanas a la gente, como vías rurales y acueductos, antes que en megaproyectos?',
    94: '¿Las regiones y municipios deberían tener más poder para manejar su plata y tomar decisiones?',
    95: '¿El gobierno nacional debería poder aprobar proyectos mineros o petroleros aunque las comunidades locales no estén de acuerdo?',
    96: '¿La naturaleza, como ríos y páramos, debería tener protección especial incluso si eso frena proyectos económicos?',
    97: '¿Creés que se puede explotar recursos naturales de forma responsable si se compensa el daño ambiental?',
    98: '¿Colombia debería dejar de buscar nuevos pozos de petróleo y gas para acelerar la transición energética?',
    99: '¿Colombia debería seguir produciendo petróleo y gas por ahora para sostener empleo e ingresos del país?',
    100: '¿La transición energética debería ser dirigida por el Estado, incluso si eso acelera el cierre de combustibles fósiles?',
    101: '¿El país debería cambiar a energías limpias poco a poco, dejando que el mercado marque el ritmo?',
    102: '¿Colombia debería acercarse más a otros países de América Latina y del Sur Global, no solo a Estados Unidos?',
    103: '¿Estados Unidos debería seguir siendo el aliado principal de Colombia en seguridad, comercio y drogas?',
    104: '¿Colombia debería tener más control propio sobre sus datos, internet y plataformas digitales?',
    105: '¿Para atraer tecnología, Colombia debería dar facilidades a empresas globales y regularlas menos?',
}


def upgrade() -> None:
    connection = op.get_bind()
    update_question = sa.text(
        "UPDATE questions SET title = :title, updated_at = NOW() WHERE id = :question_id"
    )

    for question_id, title in QUESTION_TITLES.items():
        connection.execute(update_question, {"question_id": question_id, "title": title})


def downgrade() -> None:
    # Content-only migration. The previous wording came from seed data and should not be
    # restored automatically because production content may have evolved independently.
    pass
