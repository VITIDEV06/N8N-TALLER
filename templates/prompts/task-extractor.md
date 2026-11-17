# Prompt: extractor de tareas (reto avanzado A3)

Convierte un texto libre (por ejemplo, notas de una reunión) en tareas listas para guardar en la pestaña `Tareas`.

## Mensaje de sistema

```text
Extrae las tareas accionables del texto del usuario.
Responde SOLO con JSON válido con esta forma:
{"tareas": [{"titulo": "...", "prioridad": "alta|media|baja", "fecha_limite": "AAAA-MM-DD o vacío"}]}
Reglas:
- Un título por tarea, en infinitivo, máximo 100 caracteres.
- Prioridad "alta" solo si el texto indica urgencia o una fecha en los próximos 3 días.
- fecha_limite solo si aparece una fecha explícita; si no, cadena vacía.
- Si no hay tareas, devuelve {"tareas": []}.
- Hoy es {{HOY}}.
```

`{{HOY}}` se sustituye por `$now.toFormat('yyyy-MM-dd')` para que el modelo pueda interpretar fechas relativas.

## Ejemplo

Entrada:

```text
Mañana hay que enviar el presupuesto al cliente. También deberíamos revisar el contrato antes del 10 de diciembre y, cuando se pueda, actualizar la web.
```

Salida esperada (si hoy es 2026-11-17):

```json
{
  "tareas": [
    { "titulo": "Enviar el presupuesto al cliente", "prioridad": "alta", "fecha_limite": "2026-11-18" },
    { "titulo": "Revisar el contrato", "prioridad": "media", "fecha_limite": "2026-12-10" },
    { "titulo": "Actualizar la web", "prioridad": "baja", "fecha_limite": "" }
  ]
}
```

## Validación recomendada

Reutiliza la lógica de `crearTarea` del Proyecto A: título entre 3 y 200 caracteres, prioridad en la lista, fecha ISO válida y no pasada. Descarta las tareas que no la cumplan e infórmalo en la respuesta.
