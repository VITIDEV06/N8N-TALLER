# Plantillas de entorno

| Archivo | Uso |
| --- | --- |
| [`../../.env.example`](../../.env.example) | Configuración base del taller (local, sin HTTPS). Cópiala como `.env` en la raíz. |
| [`env.tunnel.example`](env.tunnel.example) | Cambios necesarios cuando expones n8n con un túnel HTTPS para el Telegram Trigger. |

## Cómo usarlas

```bash
cp .env.example .env
# Edita .env y sustituye los valores CAMBIAR
# Si usas un túnel, añade o sustituye las líneas de templates/environment/env.tunnel.example
docker compose up -d
```

## Reglas

- `.env` está en `.gitignore`. Comprueba con `git status` que nunca aparece como archivo para commit.
- Los archivos de esta carpeta no contienen secretos: solo nombres de variables y valores de ejemplo.
- Desde n8n 2.0 los workflows no pueden leer variables de entorno (`N8N_BLOCK_ENV_ACCESS_IN_NODE=true` por defecto). Estas variables configuran **la instancia**, no los workflows. Los valores de cada workflow van en su nodo `Configuración`.

Referencia completa: [docs/installation.md](../../docs/installation.md#variables-de-entorno).
