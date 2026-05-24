export function normalizeMojibake(value: string): string {
  return value
    .replaceAll('Â¿', '¿')
    .replaceAll('Ã¡', 'á')
    .replaceAll('Ã©', 'é')
    .replaceAll('Ã­', 'í')
    .replaceAll('Ã³', 'ó')
    .replaceAll('Ãº', 'ú')
    .replaceAll('Ã±', 'ñ')
}

export function formatPercent(value: number): string {
  return `${Math.round(value * 100)}%`
}
