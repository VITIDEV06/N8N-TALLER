# Referencia de expresiones

Las expresiones permiten usar datos dinámicos en cualquier parámetro de un nodo. Se escriben entre dobles llaves `{{ }}` y contienen JavaScript. En el JSON exportado, un parámetro con expresión empieza por `=`: `"={{ $json.titulo }}"`.

Para aprender con ejercicios, sigue el [Módulo 04](../modules/04-data-and-expressions/README.md).

## Variables principales

| Expresión | Devuelve |
| --- | --- |
| `$json` | Los datos JSON del item actual de entrada. |
| `$json.titulo` | Un campo del item actual. |
| `$json['fecha limite']` | Un campo con espacios o caracteres especiales. |
| `$input.first().json` | El primer item de la entrada. |
| `$input.all()` | Todos los items de la entrada (array). |
| `$('Nombre del nodo').item.json` | El item **relacionado** del nodo indicado (*paired item*). |
| `$('Nombre del nodo').first().json` | El primer item de salida de ese nodo. |
| `$('Nombre del nodo').all()` | Todos los items de salida de ese nodo. |
| `$now` | Fecha y hora actual (objeto Luxon `DateTime`) en la zona horaria de n8n. |
| `$today` | Hoy a medianoche (Luxon). |
| `$execution.id` | ID de la ejecución actual. |
| `$workflow.name` | Nombre del workflow. |
| `$runIndex` | Número de vez que se ejecuta el nodo en esta ejecución (bucles). |

> [!TIP]
> En los workflows del taller, los valores del nodo `Configuración` se leen con `$('Configuración').first().json.campo`. `first()` evita problemas de emparejamiento de items cuando hay ramas o bucles.

## Cadenas de texto

| Expresión | Resultado |
| --- | --- |
| `{{ $json.titulo.trim() }}` | Quita espacios al principio y al final. |
| `{{ $json.titulo.toUpperCase() }}` | Mayúsculas. |
| `{{ $json.texto.slice(0, 100) }}` | Primeros 100 caracteres. |
| `{{ $json.texto.includes('urgente') }}` | `true` / `false`. |
| `{{ $json.texto.split('\|') }}` | Array separado por `\|`. |
| `` {{ `Hola ${$json.nombre}` }} `` | Plantilla de texto. |

## Números

| Expresión | Resultado |
| --- | --- |
| `{{ Number($json.cantidad) }}` | Convierte texto a número. |
| `{{ ($json.hechos / $json.total * 100).toFixed(1) }}` | Porcentaje con un decimal (texto). |
| `{{ Math.round($json.valor) }}` | Redondeo. |

## Arrays

| Expresión | Resultado |
| --- | --- |
| `{{ $json.etiquetas.length }}` | Número de elementos. |
| `{{ $json.etiquetas.join(', ') }}` | Texto separado por comas. |
| `{{ $json.tareas.filter(t => t.estado === 'pendiente').length }}` | Cuántas tareas pendientes. |
| `{{ $json.tareas.map(t => t.titulo) }}` | Solo los títulos. |

## Fechas con Luxon

n8n incluye la librería [Luxon](https://moment.github.io/luxon/). `$now` y `$today` ya son objetos Luxon.

| Expresión | Resultado de ejemplo |
| --- | --- |
| `{{ $now.toISO() }}` | `2026-11-17T09:30:00.000-06:00` |
| `{{ $now.toFormat('yyyy-MM-dd') }}` | `2026-11-17` |
| `{{ $now.toFormat('HH:mm') }}` | `09:30` |
| `{{ $now.setLocale('es').toFormat('cccc d LLLL') }}` | `martes 17 noviembre` |
| `{{ $now.startOf('day').toISO() }}` | Hoy a las 00:00 |
| `{{ $now.endOf('day').toISO() }}` | Hoy a las 23:59:59.999 |
| `{{ $now.plus({ days: 7 }).toFormat('yyyy-MM-dd') }}` | Dentro de 7 días |
| `{{ $now.minus({ days: 6 }).startOf('day') }}` | Inicio del periodo de 7 días |
| `{{ DateTime.fromISO($json.fecha).toFormat('dd/MM/yyyy') }}` | Convierte texto ISO a otro formato |
| `{{ DateTime.fromISO($json.fecha) < $now }}` | Compara fechas |
| `{{ $now.weekday }}` | 1 (lunes) a 7 (domingo) |

> [!NOTE]
> Usa el formato ISO `AAAA-MM-DD` para guardar fechas en Google Sheets. Es inequívoco, se ordena correctamente como texto y Luxon lo interpreta sin configuración.

## Condiciones en una línea

```text
{{ $json.prioridad === 'alta' ? 'URGENTE' : 'normal' }}
{{ $json.nota || 'sin nota' }}
{{ $json.cliente?.nombre ?? 'desconocido' }}
```

## Expresiones frente a nodo Code

| Usa una expresión cuando... | Usa un nodo Code cuando... |
| --- | --- |
| Transformas un campo concreto. | Necesitas varias líneas de lógica. |
| Construyes un texto o una fecha. | Validas varios campos y generas mensajes de error. |
| Lees un valor de otro nodo. | Agrupas, cuentas o calculas estadísticas sobre muchos items. |

## Errores habituales

| Mensaje | Causa |
| --- | --- |
| `Cannot read properties of undefined` | El campo no existe en ese item. Usa `?.` o comprueba la salida del nodo anterior. |
| `Referenced node is unexecuted` | La expresión apunta a un nodo que no se ha ejecutado en esta rama. |
| `Paired item data is unavailable` | `.item` no puede relacionar el item con el nodo indicado. Usa `.first()` o `.all()`. |
| `access to env vars denied` | Se usó `$env`, bloqueado por defecto en n8n 2.x. Usa credenciales o el nodo `Configuración`. |

Referencia oficial: <https://docs.n8n.io/code/expressions/> y <https://docs.n8n.io/code/builtin/overview/>.
