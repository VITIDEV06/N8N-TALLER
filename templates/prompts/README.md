# Plantillas de prompts

Instrucciones (*prompts*) para los modelos de lenguaje usados en el taller. Están separadas del código para que puedas estudiarlas, compararlas y adaptarlas.

| Archivo | Usado en | Salida esperada |
| --- | --- | --- |
| [knowledge-classifier.md](knowledge-classifier.md) | Proyecto E y `/nota` del proyecto final (nodo **Preparar solicitud**) | JSON con categoría, título, resumen, puntos clave y etiquetas |
| [daily-summary-writer.md](daily-summary-writer.md) | Mejora opcional del Proyecto B | Texto breve y motivador a partir del resumen diario |
| [task-extractor.md](task-extractor.md) | Reto avanzado A3 | JSON con tareas detectadas en un texto libre |

## Buenas prácticas aplicadas

1. **Rol y objetivo claros** en la primera línea.
2. **Formato de salida explícito** (JSON con claves exactas) para poder validarlo con código.
3. **Lista cerrada de valores** cuando sea posible (categorías), y validación posterior en n8n.
4. **Prohibición de inventar** datos que no estén en el texto.
5. **Temperatura baja** (`0.2`) para respuestas más estables.
6. **Validar siempre la salida**: un modelo puede devolver texto adicional, bloques de código Markdown o JSON incompleto. El nodo **Validar respuesta** del Proyecto E muestra cómo hacerlo.

## Variables

Las plantillas usan marcadores entre llaves dobles con mayúsculas, por ejemplo `{{CATEGORIAS}}`. En los workflows esos valores se insertan desde el nodo Code; no son expresiones de n8n.
