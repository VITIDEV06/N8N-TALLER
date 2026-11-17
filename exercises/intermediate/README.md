# Ejercicios — Nivel Intermediate

Requisitos: módulos 04 y 05. I1 e I2 no necesitan credenciales; I3 necesita Google Sheets y Telegram.

---

## I1 — Webhook con validación

**Enunciado.** Amplía [03-webhook-basics.json](../../workflows/01-getting-started/03-webhook-basics.json) para que acepte una **tarea** en lugar de un nombre:

```json
{ "titulo": "Preparar demo", "prioridad": "alta", "fecha_limite": "2026-12-01" }
```

- Responde `201` con la tarea normalizada y un `id` generado si es válida.
- Responde `400` con la lista de errores si el título tiene menos de 3 caracteres, la prioridad no es `alta`, `media` o `baja`, o la fecha no tiene formato `AAAA-MM-DD`.

<details>
<summary>Pistas</summary>

- En el webhook, el cuerpo de la petición está en `$json.body`.
- Valida en un Code y devuelve `valida: true/false`; después usa un IF.
- En **Respond to Webhook**, *Options > Response Code*.

</details>

### Solución explicada

Code `Validar tarea`:

```javascript
const b = $input.first().json.body || {};
const errores = [];
const titulo = String(b.titulo || '').trim();
const prioridad = String(b.prioridad || 'media').toLowerCase();
const fecha = String(b.fecha_limite || '');
if (titulo.length < 3) errores.push('titulo: mínimo 3 caracteres');
if (!['alta', 'media', 'baja'].includes(prioridad)) errores.push('prioridad: alta, media o baja');
if (fecha && (!/^\d{4}-\d{2}-\d{2}$/.test(fecha) || !DateTime.fromISO(fecha).isValid)) errores.push('fecha_limite: formato AAAA-MM-DD');
const id = 'T-' + Math.random().toString(36).slice(2, 8).toUpperCase();
return [{ json: { valida: errores.length === 0, errores, tarea: { id, titulo, prioridad, fecha_limite: fecha } } }];
```

IF sobre `{{ $json.valida }}`; rama `true` a **Respond to Webhook** con *Response Code* 201 y cuerpo `{{ $json.tarea }}`; rama `false` con 400 y `{{ { errores: $json.errores } }}`.

**Resultado esperado:**

```bash
curl -i -X POST http://localhost:5678/webhook-test/taller-saludo -H "Content-Type: application/json" \
  -d '{"titulo":"ok","prioridad":"urgente"}'
# HTTP/1.1 400 ... {"errores":["titulo: mínimo 3 caracteres","prioridad: alta, media o baja"]}
```

---

## I2 — API pública con agregación

**Enunciado.** Obtén las 100 publicaciones de `https://jsonplaceholder.typicode.com/posts` y devuelve **un único item** con el total, el número de usuarios distintos y un ranking de publicaciones por usuario (de más a menos; a igualdad, por id de usuario).

<details>
<summary>Pistas</summary>

- El HTTP Request ya divide el array en 100 items.
- En un Code, recorre `$input.all()` y acumula en un objeto.

</details>

### Solución explicada

```javascript
const conteo = {};
for (const { json } of $input.all()) conteo[json.userId] = (conteo[json.userId] || 0) + 1;
const ranking = Object.entries(conteo)
  .map(([usuario, total]) => ({ usuario: Number(usuario), total }))
  .sort((a, b) => b.total - a.total || a.usuario - b.usuario);
return [{ json: { totalPublicaciones: $input.all().length, usuarios: ranking.length, ranking } }];
```

Solución importable: [solutions/i2-api-agregacion.json](solutions/i2-api-agregacion.json).

**Resultado esperado:** `totalPublicaciones: 100`, `usuarios: 10` y cada usuario con `total: 10` (los datos de JSONPlaceholder son fijos).

**Ampliación:** con un segundo HTTP Request a `/users` y un **Merge** en modo *Combine > Matching Fields* (`id` con `usuario`), añade el nombre de cada usuario al ranking.

---

## I3 — Aviso de tareas vencidas

**Enunciado.** Con la pestaña `Tareas` del [Proyecto A](../../workflows/02-task-manager/README.md), crea un workflow programado (cada día a las 09:00) que envíe por Telegram la lista de tareas **no completadas** cuya `fecha_limite` sea anterior a hoy. Si no hay ninguna, no envía nada.

<details>
<summary>Pistas</summary>

- Google Sheets *Get Rows* con *Always Output Data*.
- Las fechas `AAAA-MM-DD` se pueden comparar como texto: `'2026-11-10' < '2026-11-17'`.
- Para no enviar nada, el Code puede devolver `[]`: los nodos siguientes no se ejecutan.

</details>

### Solución explicada

| Nodo | Configuración |
| --- | --- |
| Schedule Trigger | Days, hora 9 |
| Configuración (Edit Fields) | `spreadsheetId`, `chatId` |
| Leer tareas (Google Sheets) | Get Rows, pestaña `Tareas`, *Always Output Data* |
| Detectar vencidas (Code) | Ver abajo |
| Enviar aviso (Telegram) | *Chat ID* `{{ $json.chatId }}`, *Text* `{{ $json.texto }}` |

```javascript
const { chatId } = $('Configuración').first().json;
const hoy = $now.toFormat('yyyy-MM-dd');
const vencidas = $input.all().map((i) => i.json)
  .filter((t) => t.id && t.estado !== 'completada' && t.fecha_limite && t.fecha_limite < hoy);
if (vencidas.length === 0) return [];
const lineas = vencidas.map((t) => `- ${t.id} ${t.titulo} (venció ${t.fecha_limite})`);
return [{ json: { chatId, texto: `Tienes ${vencidas.length} tarea(s) vencida(s):\n${lineas.join('\n')}` } }];
```

**Resultado esperado:** con las filas de [tareas.csv](../../templates/google-sheets/tareas.csv), un mensaje con las tareas pendientes de fecha pasada; ningún mensaje si todas están al día.

---

Anterior: [Beginner](../beginner/README.md) | Siguiente: [Advanced](../advanced/README.md) | [Ruta de aprendizaje](../README.md)
