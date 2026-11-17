# Módulo 03 — Fundamentos de automatización

| Duración estimada | Nivel | Requisitos |
| --- | --- | --- |
| 2 horas | Beginner | Módulo 02 completado |

## Objetivos

Usar con soltura los nodos que aparecen en casi todos los workflows: triggers básicos, peticiones HTTP, lógica condicional, combinación de ramas, bucles, código y manejo de errores.

## Índice

| Concepto | Workflow de demostración |
| --- | --- |
| [Manual Trigger](#manual-trigger) | [01-hello-world.json](../../workflows/01-getting-started/01-hello-world.json) |
| [Schedule Trigger](#schedule-trigger) | [02-schedule-trigger.json](../../workflows/01-getting-started/02-schedule-trigger.json) |
| [Webhook](#webhook) | [03-webhook-basics.json](../../workflows/01-getting-started/03-webhook-basics.json) |
| [HTTP Request](#http-request) | [04-http-request-api.json](../../workflows/01-getting-started/04-http-request-api.json) |
| [IF](#if) | 03 y 04 |
| [Switch](#switch) | [05-logic-switch-merge-loop.json](../../workflows/01-getting-started/05-logic-switch-merge-loop.json) |
| [Merge](#merge) | 04 y 05 |
| [Edit Fields (Set)](#edit-fields-set) | Todos |
| [Code](#code) | Todos |
| [Loop Over Items](#loop-over-items) | 05 |
| [Manejo de errores](#manejo-de-errores) | [06-error-handling.json](../../workflows/01-getting-started/06-error-handling.json), [08-error-workflow.json](../../workflows/01-getting-started/08-error-workflow.json) |
| [Ejecuciones y depuración](#ejecuciones-y-depuración) | Todos |

Al final: [ejercicio guiado](#ejercicio-guiado), [reto](#reto-individual) y [solución](#solución-explicada).

---

## Manual Trigger

Inicia el workflow al pulsar **Execute workflow**. Es el trigger para aprender y probar. No funciona en producción: un workflow publicado necesita otro trigger.

**Ejemplo práctico:** todos los workflows de `01-getting-started` lo usan.

## Schedule Trigger

Ejecuta el workflow según un horario. Configuraciones habituales:

| Necesidad | Configuración |
| --- | --- |
| Cada día a las 07:00 | *Trigger Interval*: Days, *Trigger at Hour*: 7am |
| Cada lunes a las 09:00 | *Trigger Interval*: Weeks, *Trigger on Weekdays*: Monday, hora 9am |
| Cada 15 minutos | *Trigger Interval*: Minutes, *Minutes Between Triggers*: 15 |
| Expresión cron | *Trigger Interval*: Custom (Cron), por ejemplo `0 7 * * 1-5` (laborables a las 07:00) |

Usa la zona horaria de `GENERIC_TIMEZONE`. Solo se ejecuta solo si el workflow está **publicado**.

## Webhook

Crea una URL que, al recibir una petición HTTP, inicia el workflow.

| Opción | Valor en el ejemplo 03 | Significado |
| --- | --- | --- |
| HTTP Method | POST | Método aceptado |
| Path | `taller-saludo` | Parte final de la URL |
| Respond | Using 'Respond to Webhook' Node | La respuesta la construye un nodo posterior |

URL de prueba: `/webhook-test/taller-saludo` (al pulsar *Execute workflow*). URL de producción: `/webhook/taller-saludo` (al publicar).

## HTTP Request

Llama a cualquier API REST. Puntos clave del ejemplo 04:

- **Method** y **URL**.
- **Send Query Parameters**: `userId=1` (n8n construye `?userId=1`).
- Si la respuesta es un array, n8n crea un item por elemento.
- **Settings > Retry On Fail**: reintentos automáticos ante errores temporales.
- **Authentication**: credenciales predefinidas o genéricas (Header Auth, Bearer, Basic...). Nunca pongas el token en la URL ni en un header escrito a mano.

## IF

Divide los items en dos salidas, `true` y `false`, según condiciones.

```text
{{ $json.completed }}   is true          -> salida true
{{ $json.longitud }}    is greater than 50
{{ $json.prioridad }}   is equal to alta
```

Varias condiciones se combinan con **AND** u **OR**.

## Switch

Como IF, pero con varias salidas. En el ejemplo 05, una regla por prioridad (`alta`, `media`, `baja`). La opción **Fallback Output** crea una salida extra para los items que no cumplen ninguna regla; el Proyecto A la usa como `Respuesta directa`.

## Merge

Combina datos de varias ramas.

| Modo | Uso |
| --- | --- |
| **Append** | Une todos los items de todas las entradas en una lista (ejemplos 04 y 05). |
| **Combine > Matching Fields** | Une items de dos fuentes que comparten un campo (como un JOIN). |
| **Combine > By Position** | Une el item 1 con el 1, el 2 con el 2... |
| **Choose Branch** | Espera a ambas ramas y deja pasar solo una. |

## Edit Fields (Set)

Crea, modifica o elimina campos sin código. Cada campo tiene nombre, tipo y valor (fijo o expresión). **Include Other Input Fields** decide si se conservan los campos de entrada. Los workflows del taller lo usan como nodo `Configuración`.

## Code

JavaScript para lo que no resuelven los nodos visuales.

```javascript
// Modo "Run Once for All Items" (por defecto)
const items = $input.all();                 // todos los items de entrada
const primero = $input.first().json;        // el primero
const config = $('Configuración').first().json;  // datos de otro nodo
return items.map((item) => ({ json: { ...item.json, procesado: true } }));
```

Reglas:

- Devuelve siempre un **array** de objetos con clave `json`.
- `$now` y `DateTime` (Luxon) están disponibles.
- En n8n 2.x el código se ejecuta en *task runners* aislados y **no puede leer variables de entorno**.
- El nodo Code con Python requiere *task runners* en modo externo; el taller usa solo JavaScript.

## Loop Over Items

Procesa los items en lotes. Útil para respetar límites de una API (por ejemplo, 10 peticiones cada vez).

- Salida **loop**: el lote actual; conecta aquí los nodos a repetir y vuelve a la entrada del bucle.
- Salida **done**: todos los items procesados, cuando no quedan lotes.

La mayoría de nodos ya procesan todos los items sin bucle explícito: usa Loop Over Items solo cuando necesites lotes o pausas.

## Manejo de errores

| Técnica | Dónde | Ejemplo |
| --- | --- | --- |
| Retry On Fail | *Settings* del nodo | 06: 2 intentos con 1 s de espera |
| On Error > Continue (using error output) | *Settings* del nodo | 06: el 404 sale por la rama de error |
| On Error > Continue | *Settings* del nodo | El error se guarda en el item y el flujo sigue |
| Stop and Error | Nodo | 06: detiene con un mensaje claro |
| Error workflow | *Settings* del workflow | 08: se ejecuta cuando falla un workflow publicado |
| Validación previa | Nodo Code | 03: rechaza datos incorrectos antes de usarlos |

## Ejecuciones y depuración

1. **Execute step** en un nodo para probarlo aislado.
2. **Pin data** para no repetir llamadas externas mientras pruebas.
3. Revisa *INPUT* y *OUTPUT* de cada nodo: la mayoría de errores son datos con otra forma de la esperada.
4. En nodos Code, `console.log(valor)` escribe en la consola del navegador (F12) durante ejecuciones manuales.
5. Pestaña **Executions** para ejecuciones de producción. **Debug in editor** carga los datos de una ejecución pasada en el editor.

---

## Ejercicio guiado

**Objetivo:** construir un workflow que consulte una API, filtre datos y combine ramas.

1. Crea un workflow con **Manual Trigger**.
2. Añade **HTTP Request**: GET `https://jsonplaceholder.typicode.com/users`.
3. Añade **IF**: `{{ $json.address.city }}` *is equal to* `Gwenborough` **OR** `{{ $json.id }}` *is less than* `3`.
4. En `true`, un **Edit Fields** con `grupo = destacado` (incluyendo los demás campos). En `false`, otro con `grupo = normal`.
5. **Merge** en modo Append.
6. **Code** que devuelva `{ destacados: n, normales: m, nombres: [...] }`.

**Resultado esperado:** `destacados: 2`, `normales: 8` (el usuario 1 vive en Gwenborough y tiene id menor que 3, igual que el 2).

## Reto individual

Modifica [05-logic-switch-merge-loop.json](../../workflows/01-getting-started/05-logic-switch-merge-loop.json):

1. Añade al Switch una salida *Fallback* renombrada `sin prioridad`.
2. Añade en **Tareas de ejemplo** una tarea con prioridad `urgentisima`.
3. Conecta la salida fallback a un **Edit Fields** con `plazoRecomendado = revisar prioridad` y llévalo al Merge (necesitarás 4 entradas).
4. Cambia el tamaño de lote a 3.

## Solución explicada

1. En el Switch: *Options > Fallback Output > Extra Output* y *Rename Fallback Output* = `sin prioridad`. Aparece una cuarta salida.
2. Añade `{ titulo: 'Tarea rara', prioridad: 'urgentisima' }` al array.
3. En el Merge: *Number of Inputs* = 4. Conecta el nuevo Edit Fields a la entrada 4.
4. En *Recorrer en lotes*: *Batch Size* = 3.

**Resultado esperado** en **Resumen final**: `totalTareas: 7`, `lotes: 3` (3 + 3 + 1), y `porPrioridad` incluye `urgentisima: 1`. La tarea nueva tiene `plazoRecomendado: "revisar prioridad"`.

---

Anterior: [Módulo 02](../02-installation-and-setup/README.md) | Siguiente: [Módulo 04 — Datos y expresiones](../04-data-and-expressions/README.md)
