const MOJIBAKE_REPLACEMENTS: Array<[string, string]> = [
  ['Â¿', '¿'],
  ['Â¡', '¡'],
  ['Â°', '°'],
  ['Âº', 'º'],
  ['Âª', 'ª'],
  ['Â·', '·'],
  ['â', '’'],
  ['â', '“'],
  ['â', '”'],
  ['â', '–'],
  ['â', '—'],
  ['Ã', 'Á'],
  ['Ã', 'É'],
  ['Ã', 'Í'],
  ['Ã', 'Ó'],
  ['Ã', 'Ú'],
  ['Ã', 'Ü'],
  ['Ã', 'Ñ'],
  ['Ã¡', 'á'],
  ['Ã©', 'é'],
  ['Ã­', 'í'],
  ['Ã³', 'ó'],
  ['Ãº', 'ú'],
  ['Ã¼', 'ü'],
  ['Ã±', 'ñ'],
]

export function normalizeMojibake(value: string): string {
  return MOJIBAKE_REPLACEMENTS.reduce(
    (normalized, [broken, fixed]) => normalized.replaceAll(broken, fixed),
    value,
  )
}

export function formatPercent(value: number): string {
  return `${Math.round(value * 100)}%`
}
