# Plantillas de Google Sheets

Cada CSV corresponde a una pestaña de la hoja `Productivity Workshop`. La **primera fila** contiene los encabezados que esperan los workflows; las demás son datos ficticios de ejemplo.

## Cómo importarlas

1. Crea una hoja nueva en <https://sheets.new>.
2. Crea una pestaña por cada CSV con el **nombre exacto** de la tabla.
3. En cada pestaña: **Archivo > Importar > Subir > Reemplazar hoja actual**.
4. Opcional: borra las filas de ejemplo (deja la fila 1).

Guía completa: [guides/google-sheets-setup.md](../../guides/google-sheets-setup.md).

> [!NOTE]
> Los datos de ejemplo usan el `chat_id` ficticio `000000000`. No aparecerán en tus consultas de Telegram, que filtran por tu propio `chat_id`. Sirven para ver el formato.

## Estructura de las tablas

### `Tareas` — [tareas.csv](tareas.csv)

Usada por: Proyecto A, Proyecto B, Proyecto Final.

| Columna | Tipo | Ejemplo | Descripción |
| --- | --- | --- | --- |
| `id` | Texto | `T-4F9K2A` | Identificador único generado por el workflow. Clave para actualizar. |
| `titulo` | Texto | `Preparar presentación` | Entre 3 y 200 caracteres. |
| `prioridad` | Texto | `alta` | `alta`, `media` o `baja`. |
| `fecha_limite` | Texto ISO | `2026-12-01` | Opcional. Formato `AAAA-MM-DD`. |
| `estado` | Texto | `pendiente` | `pendiente`, `en_progreso` o `completada`. |
| `creada_en` | Texto | `2026-11-17 09:00` | Fecha y hora de creación. |
| `actualizada_en` | Texto | `2026-11-17 09:00` | Última modificación. |
| `chat_id` | Texto | `123456789` | Chat de Telegram propietario de la tarea. |

### `Habitos` — [habitos.csv](habitos.csv)

Catálogo de hábitos. **Lo editas tú a mano.**

| Columna | Tipo | Ejemplo | Descripción |
| --- | --- | --- | --- |
| `habito` | Texto | `leer` | Nombre corto, sin espacios. Se usa en `/habito leer`. |
| `descripcion` | Texto | `Leer 20 minutos` | Texto descriptivo. |
| `meta_semanal` | Número | `5` | Días por semana que quieres cumplirlo (1 a 7). |
| `activo` | Texto | `si` | `si` o `no`. Los inactivos no se pueden registrar ni cuentan en estadísticas. |

### `RegistroHabitos` — [registro-habitos.csv](registro-habitos.csv)

Una fila por hábito cumplido y día. La escribe el workflow.

| Columna | Tipo | Ejemplo |
| --- | --- | --- |
| `fecha` | Texto ISO | `2026-11-17` |
| `habito` | Texto | `leer` |
| `chat_id` | Texto | `123456789` |
| `nota` | Texto | `Capítulo 4` |
| `registrado_en` | Texto | `2026-11-17 22:10` |

### `RegistroCorreos` — [registro-correos.csv](registro-correos.csv)

Una fila por correo clasificado. **No guarda el cuerpo del correo.**

| Columna | Tipo | Ejemplo |
| --- | --- | --- |
| `fecha_procesado` | Texto | `2026-11-17 08:05` |
| `message_id` | Texto | ID interno de Gmail |
| `remitente` | Texto | `soporte@proveedor.example.com` |
| `asunto` | Texto | Máximo 200 caracteres |
| `categoria` | Texto | `importante`, `tarea`, `notificacion`, `newsletter`, `otros` |
| `motivo` | Texto | Regla que decidió la categoría |

### `Conocimiento` — [conocimiento.csv](conocimiento.csv)

Notas estructuradas por el Proyecto E y el comando `/nota` del proyecto final.

| Columna | Tipo | Descripción |
| --- | --- | --- |
| `id` | Texto | `K-...` generado por el workflow |
| `fecha` | Texto | Fecha y hora de procesamiento |
| `fuente` | Texto | Origen del texto (`telegram`, `ejemplo-manual`, el valor enviado al webhook) |
| `categoria` | Texto | Una de la lista configurada |
| `titulo` | Texto | Máximo 80 caracteres |
| `resumen` | Texto | Máximo 600 caracteres |
| `puntos_clave` | Texto | Puntos separados por ` \| ` |
| `etiquetas` | Texto | Separadas por comas |
| `modelo` | Texto | Modelo usado o `simulado` |
| `estado` | Texto | `ok` o `revisar` (la validación detectó problemas) |
| `texto_original` | Texto | Primeros 1000 caracteres del texto analizado |

## Por qué las fechas se guardan como texto

Los workflows escriben con **Cell Format: RAW**, de modo que `2026-12-01` se guarda como texto y no como fecha con formato regional. Así:

- Las comparaciones (`fecha_limite < hoy`) funcionan igual en cualquier idioma de Google Sheets.
- Al leer, n8n recibe exactamente el mismo valor que escribió.
