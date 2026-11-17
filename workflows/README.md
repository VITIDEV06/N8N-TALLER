# Catálogo de workflows

Todos los archivos `.json` de esta carpeta se pueden importar directamente en n8n 2.x (menú `...` > **Import from File...**). No contienen credenciales ni datos personales: después de importarlos debes asignar tus credenciales y rellenar el nodo `Configuración`.

## Estado de verificación

| Nivel | Significado |
| --- | --- |
| **Validación estática** | El JSON pasa `scripts/validate-workflows.py` y el validador de parámetros de `@n8n/workflow-sdk` de n8n 2.48.4. |
| **Importación comprobada** | Importado con `n8n import:workflow` en n8n 2.48.4. |
| **Ejecución comprobada** | Ejecutado con `n8n execute` en n8n 2.48.4 (el webhook 03, publicado y llamado con `curl`). Si el workflow usa servicios externos, se ejecutó sustituyendo esos nodos por nodos Code con datos ficticios (*integraciones simuladas*): se comprueba la lógica, no la conexión real. |
| **Integración real comprobada** | Probado contra el servicio real (Telegram, Google, IA). **Ningún workflow tiene aún este nivel**: requiere tus propias credenciales. |

## 01 — Primeros pasos (sin credenciales)

| Archivo | Enseña | Módulo | Verificación |
| --- | --- | --- | --- |
| [01-hello-world.json](01-getting-started/01-hello-world.json) | Manual Trigger, Edit Fields, Code | 01 | Ejecución comprobada |
| [02-schedule-trigger.json](01-getting-started/02-schedule-trigger.json) | Schedule Trigger, fechas | 03 | Ejecución comprobada |
| [03-webhook-basics.json](01-getting-started/03-webhook-basics.json) | Webhook, validación, Respond to Webhook | 03 | Ejecución comprobada (publicado y probado con peticiones HTTP reales) |
| [04-http-request-api.json](01-getting-started/04-http-request-api.json) | HTTP Request, IF, Merge | 03 | Ejecución comprobada (API pública real) |
| [05-logic-switch-merge-loop.json](01-getting-started/05-logic-switch-merge-loop.json) | Switch, Merge, Loop Over Items | 03 | Ejecución comprobada |
| [06-error-handling.json](01-getting-started/06-error-handling.json) | Retry, error output, Stop and Error | 03 | Ejecución comprobada |
| [07-google-sheets-connection-test.json](01-getting-started/07-google-sheets-connection-test.json) | Primera conexión con Google Sheets | 05 | Importación comprobada |
| [08-error-workflow.json](01-getting-started/08-error-workflow.json) | Error Trigger | 03 | Importación comprobada |
| [09-data-expressions.json](01-getting-started/09-data-expressions.json) | JSON, arrays, expresiones, Luxon, validación | 04 | Ejecución comprobada |

Documentación: [01-getting-started/README.md](01-getting-started/README.md).

## Proyectos de productividad

| Proyecto | Archivos | Servicios | Verificación |
| --- | --- | --- | --- |
| [A. Personal Task Manager](02-task-manager/README.md) | `task-manager.json` | Telegram, Google Sheets | Ejecución comprobada con integraciones simuladas |
| [B. Daily Productivity Assistant](03-daily-assistant/README.md) | `daily-assistant.json` | Google Calendar, Google Sheets, Telegram | Ejecución comprobada con integraciones simuladas |
| [C. Smart Email Organizer](04-email-organizer/README.md) | `email-organizer.json`, `email-classifier-test.json` | Gmail, Google Sheets | Ejecución comprobada con integraciones simuladas; el clasificador de prueba se ejecuta sin credenciales |
| [D. Habit Tracker](05-habit-tracker/README.md) | `habit-tracker-bot.json`, `habit-weekly-summary.json` | Telegram, Google Sheets | Ejecución comprobada con integraciones simuladas |
| [E. AI Knowledge Assistant](06-ai-knowledge-assistant/README.md) | `ai-knowledge-assistant.json` | IA compatible con OpenAI (opcional), Google Sheets | Ejecución comprobada en modo simulado y con respuestas de modelo simuladas |
| [Proyecto final: Personal Productivity Hub](07-final-productivity-system/README.md) | 7 workflows `hub-*.json` | Todos los anteriores | Ejecución comprobada con integraciones simuladas, cada workflow por separado |

## Reglas comunes

- Cada workflow tiene notas adhesivas (*Sticky Notes*) que explican qué configurar.
- Los valores personales están en el nodo **Configuración** con el prefijo `REEMPLAZAR_`.
- Los nodos que necesitan credencial aparecen con un aviso tras importar.
- Los nombres de nodos están en español y las expresiones dependen de ellos: si renombras un nodo desde el editor, n8n actualiza las referencias; si editas el JSON a mano, debes hacerlo tú.
