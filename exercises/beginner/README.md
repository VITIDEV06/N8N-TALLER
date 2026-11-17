# Ejercicios — Nivel Beginner

Requisitos: módulos 01 a 03. No necesitas credenciales.

---

## B1 — Ficha de contacto

**Enunciado.** Crea un workflow con **Manual Trigger** y un **Edit Fields** que genere estos campos para un contacto ficticio: `nombre`, `email`, `empresa` y `alta` (fecha de hoy en formato `AAAA-MM-DD`). Añade un **Code** que devuelva `{ resumen: "Nombre (empresa) - email" }`.

<details>
<summary>Pistas</summary>

- La fecha de hoy: `{{ $now.toFormat('yyyy-MM-dd') }}`.
- En el Code, `$input.first().json` contiene los campos del Edit Fields.

</details>

### Solución explicada

| Nodo | Configuración |
| --- | --- |
| Manual Trigger | Sin cambios |
| Edit Fields | `nombre` = `Ana Pérez`, `email` = `ana@example.com`, `empresa` = `Empresa Ficticia`, `alta` = `{{ $now.toFormat('yyyy-MM-dd') }}` |
| Code | Ver abajo |

```javascript
const c = $input.first().json;
return [{ json: { resumen: `${c.nombre} (${c.empresa}) - ${c.email}`, alta: c.alta } }];
```

**Resultado esperado:** `{ "resumen": "Ana Pérez (Empresa Ficticia) - ana@example.com", "alta": "<fecha de hoy>" }`.

---

## B2 — Mensaje según el día de la semana

**Enunciado.** Parte de [02-schedule-trigger.json](../../workflows/01-getting-started/02-schedule-trigger.json). Añade un **Switch** que, según el día de la semana, genere un mensaje distinto:

- Lunes: `Planifica la semana`.
- Viernes: `Revisa lo conseguido`.
- Sábado y domingo: `Descansa`.
- Resto: `Sigue con tus tareas`.

<details>
<summary>Pistas</summary>

- `$now.weekday` devuelve 1 (lunes) a 7 (domingo).
- Usa reglas de tipo *Number* y la salida *Fallback* para el resto.
- Para probar otro día, sustituye temporalmente `$now.weekday` por un número fijo.

</details>

### Solución explicada

1. Switch en modo *Rules*, valor a comparar `{{ $now.weekday }}`:
   - Regla 1: *is equal to* `1`. Salida renombrada `lunes`.
   - Regla 2: *is equal to* `5`. Salida `viernes`.
   - Regla 3: *is greater than or equal to* `6`. Salida `fin de semana`.
   - *Options > Fallback Output*: Extra Output, renombrada `resto`.
2. Un **Edit Fields** por salida con el campo `mensaje`.

**Resultado esperado:** al ejecutar se activa una sola rama, la del día actual, con el mensaje correspondiente.

---

## B3 — Filtrar tareas

**Enunciado.** Con estas tareas de ejemplo (genéralas en un nodo Code):

```javascript
[
  { titulo: 'Enviar informe', prioridad: 'alta', hecha: false },
  { titulo: 'Reservar vuelo', prioridad: 'media', hecha: true },
  { titulo: 'Llamar al dentista', prioridad: 'alta', hecha: false },
  { titulo: 'Ordenar fotos', prioridad: 'baja', hecha: false },
]
```

Quédate solo con las **pendientes de prioridad alta** usando el nodo **Filter** (no el Code) y crea para cada una el campo `linea` con el formato `[ALTA] título`.

<details>
<summary>Pistas</summary>

- El nodo Code debe devolver **un item por tarea**: `return tareas.map((t) => ({ json: t }));`.
- En el Filter, dos condiciones combinadas con **AND**: una de tipo *Boolean* (*is false*) y otra de tipo *String* (*is equal to*).

</details>

### Solución explicada

| Nodo | Configuración |
| --- | --- |
| Tareas de ejemplo (Code) | Devuelve los 4 items |
| Solo pendientes de prioridad alta (Filter) | `{{ $json.hecha }}` *Boolean > is false* **AND** `{{ $json.prioridad }}` *String > is equal to* `alta` |
| Formatear (Edit Fields) | `linea` = `{{ '[ALTA] ' + $json.titulo }}` |

Solución importable: [solutions/b3-filtrar-tareas.json](solutions/b3-filtrar-tareas.json).

**Resultado esperado:** 2 items: `[ALTA] Enviar informe` y `[ALTA] Llamar al dentista`.

**Ampliación:** añade un nodo **Sort** para ordenarlas alfabéticamente por `titulo`.

---

Siguiente nivel: [Intermediate](../intermediate/README.md) | [Ruta de aprendizaje](../README.md)
