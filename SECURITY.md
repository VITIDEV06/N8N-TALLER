# Política de seguridad

Este repositorio es material educativo. Aun así, los workflows trabajan con datos personales (correo, calendario, tareas) y con credenciales de servicios externos, por lo que la seguridad forma parte del contenido del taller.

## Versiones soportadas

| Versión del taller | Versión de n8n de referencia | Soporte |
| --- | --- | --- |
| 1.0.x | 2.48.4 | Activo |

## Cómo reportar una vulnerabilidad

Si encuentras un problema de seguridad **en este repositorio** (por ejemplo, un workflow que filtra datos, una configuración insegura o un secreto publicado por error):

1. **No abras un issue público.**
2. Usa la opción **Report a vulnerability** de la pestaña **Security** del repositorio en GitHub (GitHub Private Vulnerability Reporting).
3. Describe el archivo afectado, el impacto y los pasos para reproducirlo.

Se intentará responder en un plazo de 7 días. Este es un proyecto personal mantenido de forma voluntaria y no ofrece SLA.

Las vulnerabilidades **del propio n8n** deben reportarse a n8n siguiendo su política oficial: <https://github.com/n8n-io/n8n/security/policy>.

## Reglas del repositorio

- Ningún workflow exportado contiene credenciales, tokens, IDs de credenciales ni datos personales.
- Los IDs de hojas de cálculo, chats y etiquetas son marcadores del tipo `REEMPLAZAR_...`.
- El script `scripts/validate-workflows.py` busca patrones de secretos comunes y falla si los encuentra.
- El archivo `.env` está excluido mediante `.gitignore`. Solo se publica `.env.example`.

## Guía de seguridad para estudiantes

La guía completa está en [docs/security.md](docs/security.md). Resumen:

| Tema | Regla principal |
| --- | --- |
| Credenciales | Guárdalas solo en el gestor de credenciales de n8n. Nunca en nodos Code, Set o en el JSON. |
| Variables de entorno | Usa `.env` local, no lo subas a Git y genera `N8N_ENCRYPTION_KEY` aleatoria. |
| Token de Telegram | Trátalo como una contraseña. Si se filtra, revócalo con `/revoke` en BotFather. |
| OAuth de Google | Pide solo los permisos necesarios y revoca el acceso en tu cuenta de Google cuando termines. |
| API keys de IA | Usa límites de gasto en el proveedor y claves dedicadas al taller. |
| Webhooks | Usa rutas no triviales, valida la entrada y añade autenticación si son públicos. |
| Instancias públicas | No expongas el puerto 5678 directamente. Usa HTTPS mediante un proxy inverso o un túnel. |
| Backups | Cifra las copias que incluyan la base de datos o la clave de cifrado. |
| Datos personales | Usa datos ficticios para practicar. No compartas capturas con correos o chats reales. |

## Si publicaste un secreto por error

1. **Revoca el secreto inmediatamente** en el servicio de origen (BotFather, Google Cloud, proveedor de IA).
2. Crea uno nuevo y actualiza la credencial en n8n.
3. Elimina el secreto del historial de Git (por ejemplo con `git filter-repo`). Borrar el archivo en un commit nuevo **no** es suficiente.
4. Considera el secreto comprometido aunque lo hayas borrado: GitHub y terceros pueden haberlo indexado.
