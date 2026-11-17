# Guía de integración: Google Sheets

Google Sheets es la "base de datos" del taller: tareas, hábitos, registros de correo y notas de conocimiento se guardan en una hoja de cálculo que puedes abrir y editar a mano. Google Sheets es gratuito con una cuenta de Google personal.

## Índice

- [Qué hace](#qué-hace)
- [Qué necesitamos](#qué-necesitamos)
- [Preparar la hoja de cálculo del taller](#preparar-la-hoja-de-cálculo-del-taller)
- [OAuth2 frente a Service Account](#oauth2-frente-a-service-account)
- [Opción A: credencial OAuth2](#opción-a-credencial-oauth2)
- [Opción B: credencial Service Account](#opción-b-credencial-service-account)
- [Conectar la hoja en los workflows](#conectar-la-hoja-en-los-workflows)
- [Probar la conexión](#probar-la-conexión)
- [Errores frecuentes](#errores-frecuentes)
- [Consideraciones de seguridad](#consideraciones-de-seguridad)

## Qué hace

```mermaid
flowchart LR
    W["Workflow n8n"] -->|"append / read / update"| GS["Nodo Google Sheets"]
    GS -->|"Sheets API v4"| H[("Hoja: Productivity Workshop")]
    H --- P1["Pestaña Tareas"]
    H --- P2["Pestaña Habitos"]
    H --- P3["Pestaña RegistroHabitos"]
    H --- P4["Pestaña RegistroCorreos"]
    H --- P5["Pestaña Conocimiento"]
```

| Operación del nodo | Uso en el taller |
| --- | --- |
| **Append Row** | Crear tareas, registrar hábitos, guardar notas y correos clasificados. |
| **Get Row(s)** | Consultar tareas, hábitos y registros. |
| **Update Row** | Cambiar el estado de una tarea usando la columna `id` como clave. |

## Qué necesitamos

- Una cuenta de Google.
- Un proyecto en Google Cloud Console (gratuito) con **Google Sheets API** y **Google Drive API** habilitadas.
- Una credencial en n8n (OAuth2 o Service Account).

## Preparar la hoja de cálculo del taller

1. Crea una hoja nueva en <https://sheets.new> y llámala `Productivity Workshop`.
2. Crea estas pestañas con estos nombres exactos (sin tildes, para evitar errores de escritura en las expresiones):

| Pestaña | Plantilla CSV con la fila de encabezados y datos de ejemplo |
| --- | --- |
| `Tareas` | [templates/google-sheets/tareas.csv](../templates/google-sheets/tareas.csv) |
| `Habitos` | [templates/google-sheets/habitos.csv](../templates/google-sheets/habitos.csv) |
| `RegistroHabitos` | [templates/google-sheets/registro-habitos.csv](../templates/google-sheets/registro-habitos.csv) |
| `RegistroCorreos` | [templates/google-sheets/registro-correos.csv](../templates/google-sheets/registro-correos.csv) |
| `Conocimiento` | [templates/google-sheets/conocimiento.csv](../templates/google-sheets/conocimiento.csv) |

3. Para cada pestaña: **Archivo > Importar > Subir**, elige el CSV y selecciona **Reemplazar hoja actual**. Así la primera fila contendrá los encabezados que esperan los workflows.
4. Copia el **ID de la hoja** desde la URL:

```text
https://docs.google.com/spreadsheets/d/1AbCdEfGhIjKlMnOpQrStUvWxYz0123456789/edit#gid=0
                                       └──────────── ID de la hoja ────────────┘
```

Este ID se pega en el nodo `Configuración` de cada workflow (campo `spreadsheetId`).

> [!TIP]
> Si no quieres los datos de ejemplo, borra todas las filas excepto la primera (encabezados) después de importar.

## OAuth2 frente a Service Account

| Aspecto | OAuth2 | Service Account |
| --- | --- | --- |
| Quién accede | Tú, con tu cuenta de Google | Una cuenta técnica (`...@...iam.gserviceaccount.com`) |
| Alcance | Todas las hojas a las que tienes acceso | Solo las hojas que compartas explícitamente con ella |
| Configuración | Pantalla de consentimiento + cliente OAuth | Crear cuenta + clave JSON + compartir la hoja |
| Caducidad | En modo *Testing*, el token caduca a los 7 días | No caduca mientras la clave exista |
| Uso recomendado en el taller | Gmail y Calendar (obligatorio) y Sheets | Sheets, si quieres limitar el acceso |
| Nodos compatibles en n8n | Todos los de Google | Sheets, Drive, Docs y otros; **no** Calendar; Gmail solo con delegación de dominio (no recomendado) |

Recomendación del taller: **usa OAuth2 para todo** si es tu primera vez (una sola configuración sirve para Sheets, Calendar y Gmail). Usa Service Account para Sheets si prefieres que n8n solo vea la hoja del taller.

## Opción A: credencial OAuth2

La configuración del proyecto de Google Cloud y del cliente OAuth es común a Sheets, Calendar y Gmail.

### 1. Crear el proyecto y habilitar APIs

1. Abre <https://console.cloud.google.com/> y crea un proyecto llamado `n8n-workshop`.
2. Ve a **APIs & Services > Library** y habilita:
   - **Google Sheets API**
   - **Google Drive API** (necesaria para listar y abrir hojas)
   - **Google Calendar API** (Proyecto B)
   - **Gmail API** (Proyecto C)

### 2. Configurar la pantalla de consentimiento

1. **APIs & Services > OAuth consent screen > Get started**.
2. Nombre de la app: `n8n Workshop`. Correo de soporte: el tuyo.
3. **Audience: External**. La app queda en modo **Testing**.
4. Introduce tu correo de contacto, acepta la política y pulsa **Create**.
5. En **Audience > Test users**, añade tu propia dirección de Gmail.

### 3. Crear el cliente OAuth

1. En n8n, crea una credencial **Google Sheets OAuth2 API** y copia el valor de **OAuth Redirect URL**. En local será `http://localhost:5678/rest/oauth2-credential/callback`.
2. En Google Cloud: **APIs & Services > Credentials > Create credentials > OAuth client ID**.
3. **Application type: Web application**.
4. En **Authorized redirect URIs** pega la URL copiada de n8n, exactamente igual.
5. Pulsa **Create** y copia **Client ID** y **Client Secret**.

### 4. Completar la credencial en n8n

1. Pega **Client ID** y **Client Secret** en la credencial.
2. Pulsa **Sign in with Google** y elige tu cuenta.
3. Google mostrará *"Google hasn't verified this app"*: es normal en modo Testing. Pulsa **Continue**.
4. Acepta los permisos y guarda la credencial con el nombre `Google Sheets - Taller`.

> [!NOTE]
> Puedes reutilizar el mismo Client ID y Client Secret para las credenciales de Google Calendar y Gmail. Cada credencial pedirá sus propios permisos.

## Opción B: credencial Service Account

1. En Google Cloud: **IAM & Admin > Service Accounts > Create service account**. Nombre: `n8n-sheets`.
2. No necesitas asignarle roles de proyecto. Pulsa **Done**.
3. Abre la cuenta creada > **Keys > Add key > Create new key > JSON**. Se descarga un archivo JSON.
4. En n8n crea una credencial **Google Service Account API**:
   - **Service Account Email**: el campo `client_email` del JSON.
   - **Private Key**: el campo `private_key` del JSON, incluyendo `-----BEGIN PRIVATE KEY-----` y `-----END PRIVATE KEY-----`.
5. Abre tu hoja `Productivity Workshop` > **Compartir** > pega el `client_email` > rol **Editor**.
6. En cada nodo Google Sheets, cambia **Authentication** a *Service Account* y selecciona la credencial.
7. **Borra el archivo JSON descargado** cuando hayas copiado los datos, o guárdalo en un gestor de secretos.

## Conectar la hoja en los workflows

Todos los workflows que usan Sheets tienen un nodo `Configuración` al inicio:

```json
{
  "spreadsheetId": "REEMPLAZAR_CON_EL_ID_DE_TU_HOJA"
}
```

1. Abre el nodo `Configuración` y sustituye el valor por el ID de tu hoja.
2. Abre cada nodo Google Sheets y selecciona tu credencial en **Credential to connect with**.
3. Los nodos ya apuntan a la pestaña correcta por nombre (`Tareas`, `Habitos`...).

## Probar la conexión

1. Importa [workflows/01-getting-started/07-google-sheets-connection-test.json](../workflows/01-getting-started/07-google-sheets-connection-test.json).
2. Configura el ID de la hoja y la credencial.
3. Pulsa **Execute workflow**. El nodo debe devolver las filas de la pestaña `Tareas`.

## Errores frecuentes

| Error | Causa | Solución |
| --- | --- | --- |
| `The caller does not have permission` | La Service Account no tiene acceso a la hoja | Comparte la hoja con el `client_email`. |
| `Requested entity was not found` | ID de hoja incorrecto | Copia de nuevo el ID desde la URL. |
| `Unable to parse range: Tareas` | La pestaña no existe o tiene otro nombre | Revisa mayúsculas y espacios en el nombre de la pestaña. |
| `Google Drive API has not been used in project` | Drive API no habilitada | Habilítala en Google Cloud. |
| `redirect_uri_mismatch` | La URL de redirección no coincide | Copia la URL de n8n exacta, con `http`/`https` y puerto. |
| `access_denied` | Tu cuenta no es usuario de prueba | Añádela en **Audience > Test users**. |
| La credencial deja de funcionar tras una semana | Token caducado en modo Testing | Abre la credencial y pulsa **Sign in with Google** de nuevo. |
| Se crean columnas nuevas o datos desplazados | Los encabezados no coinciden con los del CSV | Importa de nuevo la plantilla CSV. |

## Consideraciones de seguridad

- Usa una hoja dedicada al taller, no hojas con datos reales de trabajo.
- Con Service Account, comparte solo esa hoja.
- El JSON de la Service Account es un secreto equivalente a una contraseña.
- Revoca el acceso OAuth al terminar: <https://myaccount.google.com/permissions>.

Referencias oficiales:

- Nodo Google Sheets: <https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googlesheets/>
- Credenciales de Google en n8n: <https://docs.n8n.io/integrations/builtin/credentials/google/>
- Google Sheets API: <https://developers.google.com/workspace/sheets/api/guides/concepts>
