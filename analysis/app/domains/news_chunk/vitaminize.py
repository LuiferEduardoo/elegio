"""Build the "vitaminized" chunk text that gets embedded.

Each chunk is prefixed with the candidate and outlet, plus the headline, so a
retrieved chunk carries who/where/what context on its own — improving recall
for candidate- or outlet-scoped queries. Example:

    [Candidato: Iván Cepeda Castro] [Medio: La Silla Vacía]. Titular: Cepeda no
    pidió una "segunda oportunidad"... Contenido: En redes sociales circula...
"""


def vitaminize(
    *, candidate_name: str, publishing_house: str, title: str, chunk: str
) -> str:
    return (
        f"[Candidato: {candidate_name}] [Medio: {publishing_house}]. "
        f"Titular: {title}. Contenido: {chunk}"
    )
