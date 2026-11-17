# Datos de prueba

Todos los datos de esta carpeta son **ficticios**. Los dominios usan `example.com` (reservado para documentación) o nombres inventados como `empresa-ficticia.com`.

| Archivo | Formato | Uso |
| --- | --- | --- |
| [emails.json](emails.json) | Salida simplificada del Gmail Trigger | Proyecto C. Los usa el workflow [email-classifier-test.json](../../workflows/04-email-organizer/email-classifier-test.json). Incluye el resultado esperado de cada correo. |
| [calendar-events.json](calendar-events.json) | Salida del nodo Google Calendar | Proyecto B. Referencia para crear eventos de prueba o fijar datos. |
| [telegram-messages.json](telegram-messages.json) | Update de la Bot API de Telegram | Proyectos A, D y final. Mensajes para fijar en el Telegram Trigger y lista de comandos para probar. |
| [knowledge-inputs.json](knowledge-inputs.json) | Cuerpo del webhook del Proyecto E | Textos para clasificar con IA y su categoría esperada. |

## Cómo usar datos fijados (pin data) en n8n

Permite probar un workflow sin depender del servicio externo:

1. Ejecuta el nodo una vez o abre su panel de salida.
2. Pulsa **Edit Output** (icono de lápiz en la salida).
3. Pega un objeto del archivo JSON (por ejemplo, uno de `mensajes` de `telegram-messages.json`).
4. Guarda: la salida queda fijada (icono de chincheta).
5. Ejecuta el workflow con **Execute workflow**: el nodo fijado no llama al servicio.

> [!WARNING]
> Elimina los datos fijados antes de exportar un workflow para compartirlo, sobre todo si contienen datos reales.

Las plantillas de las tablas de Google Sheets están en [../google-sheets/](../google-sheets/).
