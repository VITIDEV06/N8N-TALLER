# Glosario

Términos usados en el taller. Los nombres de nodos y opciones se mantienen en inglés, tal como aparecen en la interfaz de n8n.

| Término | Definición |
| --- | --- |
| **Always Output Data** | Opción de un nodo que devuelve un item vacío cuando no hay resultados, para que el flujo continúe. |
| **API** | Interfaz que permite a un programa comunicarse con otro servicio mediante peticiones. |
| **API REST** | API que usa métodos HTTP (`GET`, `POST`, `PUT`, `DELETE`) sobre URLs que representan recursos. |
| **Append** | Añadir filas al final (Google Sheets) o unir todos los items de varias entradas (Merge). |
| **Bearer token** | Token enviado en el header `Authorization: Bearer <token>` para autenticarse en una API. |
| **chat_id** | Identificador numérico de un chat de Telegram. Necesario para enviar mensajes. |
| **Code (nodo)** | Nodo que ejecuta JavaScript sobre los items. En n8n 2.x se ejecuta en *task runners* aislados. |
| **Configuración (nodo)** | Convención del taller: nodo Edit Fields al inicio de cada workflow con IDs y opciones no secretas. |
| **Credencial** | Datos de autenticación guardados y cifrados por n8n, referenciados por los nodos. |
| **Cron** | Sintaxis para expresar horarios (`0 7 * * 1-5` = laborables a las 07:00). |
| **Docker Compose** | Herramienta que arranca varios contenedores definidos en `docker-compose.yml`. |
| **Edit Fields (Set)** | Nodo que crea, modifica o elimina campos de los items sin código. |
| **Error workflow** | Workflow con un Error Trigger que n8n ejecuta cuando falla otro workflow publicado. |
| **Execute Once** | Opción que ejecuta un nodo una sola vez aunque reciba varios items. |
| **Execute Workflow** | Nodo que llama a otro workflow (sub-workflow) y, opcionalmente, espera su resultado. |
| **Execute Workflow Trigger** | Trigger de un sub-workflow: se activa cuando otro workflow lo llama. |
| **Ejecución** | Cada vez que un workflow se ejecuta. Se registra en la pestaña *Executions*. |
| **Expresión** | Código JavaScript entre `{{ }}` dentro de un parámetro, evaluado para cada item. |
| **Fallback output** | Salida extra de un Switch para los items que no cumplen ninguna regla. |
| **Header Auth** | Tipo de credencial genérica que envía un header con un valor secreto. |
| **HTTP Request** | Nodo para llamar a cualquier API HTTP. |
| **Item** | Unidad de datos que viaja entre nodos: un objeto con clave `json` (y opcionalmente `binary`). |
| **JSON** | Formato de texto para datos estructurados. Los workflows de n8n se exportan en JSON. |
| **Luxon** | Librería de fechas disponible en n8n como `DateTime` y `$now`. |
| **Merge** | Nodo que combina los items de varias ramas. |
| **Modo simulado** | Convención del taller (`useMockModel = true`): reglas que imitan la respuesta de un modelo de IA sin llamarlo. |
| **N8N_ENCRYPTION_KEY** | Clave con la que n8n cifra las credenciales. Si se pierde, las credenciales no se pueden recuperar. |
| **Nodo** | Paso de un workflow: un trigger, una acción, una transformación o una decisión. |
| **OAuth2** | Protocolo para autorizar a una aplicación (n8n) a acceder a tu cuenta sin compartir tu contraseña. |
| **Pin data** | Fijar datos de salida en un nodo para no repetir llamadas externas al probar. |
| **Polling (sondeo)** | Trigger que consulta un servicio periódicamente (Gmail Trigger cada 5 minutos). |
| **Prompt** | Instrucciones y texto que se envían a un modelo de lenguaje. |
| **Prompt injection** | Intento de manipular un modelo incluyendo instrucciones dentro del texto que procesa. |
| **Publicar** | En n8n 2.x, activar un workflow para que sus triggers funcionen en producción (antes «Activate»). |
| **Resource locator** | Campo de n8n que permite elegir un recurso de una lista, por URL o por ID. |
| **Retry On Fail** | Opción que reintenta un nodo cuando falla. |
| **Router** | Workflow que decide qué sub-workflow atiende cada petición (proyecto final). |
| **Service Account** | Cuenta técnica de Google que se autentica con una clave JSON, sin usuario humano. |
| **Sub-workflow** | Workflow llamado desde otro con Execute Workflow. |
| **Switch** | Nodo que envía cada item a una de varias salidas según reglas. |
| **Task runner** | Proceso aislado donde n8n 2.x ejecuta el código de los nodos Code. |
| **Trigger** | Primer nodo de un workflow: decide cuándo se ejecuta. |
| **Túnel** | Servicio (Cloudflare Tunnel, ngrok) que da una URL HTTPS pública a un n8n local. |
| **Webhook** | URL que inicia un workflow al recibir una petición HTTP. |
| **WEBHOOK_URL** | Variable de entorno con la URL pública de n8n, usada para registrar webhooks externos. |
| **Workflow** | Conjunto de nodos conectados que automatiza un proceso. |
