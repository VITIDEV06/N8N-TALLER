# Prompt: redactor del resumen diario (mejora opcional)

El Proyecto B construye el resumen con código, sin IA. Este prompt sirve para la mejora opcional de reescribirlo con un tono más natural.

## Cómo integrarlo

Entre **Construir resumen** y **Enviar resumen** añade:

1. Un nodo **HTTP Request** igual que *Llamar al modelo* del Proyecto E, con este cuerpo:

```json
{
  "model": "llama3.2",
  "temperature": 0.4,
  "messages": [
    { "role": "system", "content": "<mensaje de sistema de abajo>" },
    { "role": "user", "content": "{{ $json.respuesta }}" }
  ]
}
```

2. Un nodo **Edit Fields** que copie `choices[0].message.content` en `respuesta` y mantenga `chatId`.

## Mensaje de sistema

```text
Eres un asistente de productividad personal.
Recibirás un resumen del día con agenda, huecos libres y tareas.
Reescríbelo en español como un mensaje breve para Telegram:
- Máximo 12 líneas, en texto plano, sin Markdown ni emojis.
- Empieza con una frase que resuma el día.
- Mantén TODAS las horas, títulos e IDs de tareas exactamente como aparecen.
- Sugiere en una sola frase en qué hueco libre hacer la tarea más urgente.
- No añadas eventos ni tareas que no estén en el texto.
```

## Riesgo a controlar

Un modelo puede alterar horas o títulos. Si usas esta mejora, conserva el resumen original como respaldo: envía el texto del modelo solo si contiene todos los IDs `T-...` del original (compruébalo en un nodo Code).
