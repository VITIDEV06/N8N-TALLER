# Preguntas frecuentes

## Sobre el taller

**¿Necesito saber programar?**
No para los módulos 01 a 03. A partir del módulo 04 se usa algo de JavaScript en expresiones y nodos Code; todo el código está explicado y comentado.

**¿Cuánto cuesta?**
El taller y n8n en tu equipo son gratuitos. Telegram, Google Sheets, Google Calendar y Gmail son gratuitos para uso personal. La IA es opcional: Ollama es gratuito y local; los proveedores en la nube pueden cobrar.

**¿Es un curso oficial de n8n?**
No. Es un proyecto educativo independiente, sin afiliación con n8n GmbH. Consulta la sección de licencias del [README](../README.md#licencia).

**¿En qué versión de n8n se ha probado?**
En n8n 2.48.4. Las versiones 1.x no son compatibles con todos los workflows (cambios en los nodos y en la publicación de workflows).

**¿Qué está verificado y qué no?**
Consulta la sección [Estado de verificación](../README.md#estado-de-verificación) del README: distingue entre validación estática, importación, ejecución con servicios simulados e integración real.

## Instalación

**¿Puedo usar n8n Cloud en lugar de Docker?**
Sí. Los workflows se importan igual. Omite el módulo 02 y el túnel: n8n Cloud ya tiene una URL HTTPS pública. Revisa los límites de tu plan.

**¿Puedo instalarlo con npm en lugar de Docker?**
Sí (`npx n8n`, requiere Node.js 24 o superior), pero el taller documenta Docker Compose porque fija la versión, aísla dependencias y facilita las copias de seguridad.

**¿Por qué PostgreSQL y no SQLite?**
SQLite funciona para pruebas, pero PostgreSQL es más robusto con varias ejecuciones simultáneas y se respalda fácilmente con `pg_dump`.

**¿Puedo exponer mi n8n a Internet de forma permanente?**
Solo con HTTPS, usuario con contraseña robusta, actualizaciones al día y, preferiblemente, un proxy inverso. Lee [docs/security.md](security.md). Para el taller basta un túnel temporal.

## Workflows

**¿Por qué cada workflow tiene un nodo `Configuración`?**
Porque n8n 2.x bloquea por defecto el acceso a variables de entorno desde los nodos. Un nodo al principio con los IDs (no secretos) permite cambiarlos en un solo lugar.

**¿Por qué los workflows importados no tienen credenciales?**
Por seguridad: el repositorio nunca incluye credenciales. Debes crearlas en tu instancia y asignarlas tras importar ([docs/credentials.md](credentials.md)).

**¿Puedo usar Excel, Notion o Airtable en lugar de Google Sheets?**
Sí, n8n tiene nodos para todos ellos. Tendrás que sustituir los nodos de Google Sheets y adaptar los nombres de columnas. La lógica de los nodos Code no cambia.

**¿Puedo usar WhatsApp, Slack o Discord en lugar de Telegram?**
Sí para enviar mensajes. Recibir comandos requiere un trigger específico de cada plataforma; la lógica de interpretación de comandos es reutilizable.

**¿Por qué el proyecto de IA usa HTTP Request y no los nodos de IA de n8n?**
Para que funcione igual con cualquier proveedor compatible con OpenAI y se vea exactamente qué se envía. Los nodos de IA de n8n son una alternativa válida; ver [la guía de IA](../guides/ai-provider-setup.md#por-qué-http-request-y-no-los-nodos-de-ia-de-n8n).

## Datos y privacidad

**¿Dónde se guardan mis datos?**
En tu instancia de n8n (PostgreSQL local) y en los servicios que conectes (tu Google Sheets, tu Telegram). El taller no envía datos a ningún otro sitio. Si activas IA en la nube, el texto procesado se envía a ese proveedor.

**¿Puedo compartir mis workflows exportados?**
Sí, pero revísalos antes: aunque no incluyen credenciales, pueden contener IDs de hojas, `chat_id` o datos fijados (*pin data*). Ejecuta `python scripts/validate-workflows.py` para detectar los casos más comunes.

## Contribuir

**¿Cómo propongo un ejercicio o corrijo un error?**
Sigue [CONTRIBUTING.md](../CONTRIBUTING.md). Las propuestas de contenido tienen su propia plantilla de issue.
