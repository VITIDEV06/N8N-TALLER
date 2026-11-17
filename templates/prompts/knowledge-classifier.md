# Prompt: clasificador de conocimiento

Usado por el nodo **Preparar solicitud** de [ai-knowledge-assistant.json](../../workflows/06-ai-knowledge-assistant/ai-knowledge-assistant.json) y del sub-workflow [hub-05-ai-notes.json](../../workflows/07-final-productivity-system/hub-05-ai-notes.json).

## Mensaje de sistema

```text
Eres un asistente que organiza información personal.
Analiza el texto del usuario y responde SOLO con un objeto JSON válido, sin texto adicional,
con exactamente estas claves:
- "categoria": una de [{{CATEGORIAS}}]
- "titulo": título breve de máximo 80 caracteres
- "resumen": resumen en español de máximo 3 frases
- "puntos_clave": lista de 1 a 5 frases cortas
- "etiquetas": lista de 1 a 5 palabras clave en minúsculas
No inventes datos que no estén en el texto.
```

`{{CATEGORIAS}}` se sustituye por el campo `categorias` del nodo `Configuración` (por defecto `trabajo, estudio, personal, finanzas, salud, ideas, referencia`).

## Mensaje de usuario

El texto a analizar, normalizado (espacios múltiples eliminados) y recortado a `maxInputChars`.

## Salida esperada

```json
{
  "categoria": "trabajo",
  "titulo": "Entrega del prototipo de la app de hábitos",
  "resumen": "El equipo acordó entregar el prototipo el 5 de diciembre. Laura revisará los colores y Marcos preparará el informe de pruebas.",
  "puntos_clave": [
    "Entrega del prototipo el 5 de diciembre",
    "Laura revisa la paleta de colores",
    "Marcos prepara el informe de pruebas",
    "Reservar sala para la demo"
  ],
  "etiquetas": ["prototipo", "diseño", "entrega"]
}
```

## Validación aplicada después

| Regla | Si no se cumple |
| --- | --- |
| La respuesta contiene un objeto JSON | `estado = revisar`, error `JSON no válido` |
| `categoria` está en la lista | Se sustituye por `referencia` y se marca para revisar |
| `resumen` no está vacío | Se marca para revisar |
| `puntos_clave` tiene al menos un elemento | Se marca para revisar |
| Longitudes máximas | Se recortan (título 80, resumen 600, 5 puntos, 5 etiquetas) |

## Variaciones para experimentar

- Añadir un campo `"accion_sugerida"` y ampliar la validación.
- Pedir el resumen en inglés para comparar la calidad entre modelos.
- Añadir dos ejemplos (*few-shot*) antes del texto del usuario y medir si mejora la precisión de la categoría.
