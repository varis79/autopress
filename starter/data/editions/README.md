# data/editions/ — el almacén de ediciones ("Git como base de datos")

Cada edición **publicada** se guarda aquí como `<fecha>-edicion.json`. El pipeline
reconstruye el sitio entero (home, permalinks, archivo, RSS, sitemap) **desde estos
ficheros**, así que el histórico se **acumula** en lugar de perderse.

- **Esta carpeta SÍ se versiona** (a diferencia de `site/`, que es generado). Es el estado
  persistente de tu medio: si borras `site/`, se regenera desde aquí.
- Se escribe solo en publicación real (`--production`, edición no bloqueada). Los previews
  locales no tocan este almacén.
- Un fichero por edición; el nombre sale de la fecha (`YYYY-MM-DD-edicion.json`).
