# Guía de contribución

Gracias por querer mejorar el **n8n Productivity Workshop**. Este proyecto es material educativo, así que cada contribución se evalúa con una pregunta: *¿ayuda a que alguien sin experiencia aprenda mejor?*

## Índice

- [Formas de contribuir](#formas-de-contribuir)
- [Antes de empezar](#antes-de-empezar)
- [Flujo de trabajo con Git](#flujo-de-trabajo-con-git)
- [Añadir o modificar un workflow](#añadir-o-modificar-un-workflow)
- [Corregir o ampliar documentación](#corregir-o-ampliar-documentación)
- [Proponer ejercicios](#proponer-ejercicios)
- [Reportar errores](#reportar-errores)
- [Estilo de escritura](#estilo-de-escritura)
- [Licencia de las contribuciones](#licencia-de-las-contribuciones)

## Formas de contribuir

| Tipo | Cómo |
| --- | --- |
| Reportar un error | Abre un issue con la plantilla **Reporte de error**. |
| Proponer un workflow o ejercicio | Abre un issue con la plantilla **Propuesta de contenido** antes de escribirlo. |
| Corregir una errata | Pull request directo, sin issue previo. |
| Mejorar una explicación | Pull request indicando qué parte resultaba confusa. |
| Probar el taller con otra versión de n8n | Issue o PR actualizando la tabla de compatibilidad del README. |

## Antes de empezar

1. Lee el [Código de conducta](CODE_OF_CONDUCT.md).
2. Revisa los issues abiertos para evitar trabajo duplicado.
3. Para cambios grandes (un módulo nuevo, una reestructuración), abre primero un issue para acordar el enfoque.

## Flujo de trabajo con Git

```bash
# 1. Haz un fork en GitHub y clónalo
git clone https://github.com/<tu-usuario>/n8n-productivity-workshop.git
cd n8n-productivity-workshop

# 2. Crea una rama descriptiva
git checkout -b docs/mejorar-guia-telegram

# 3. Haz tus cambios y valida los workflows
python scripts/validate-workflows.py

# 4. Commit con un mensaje claro
git commit -m "docs: aclarar configuración del webhook de Telegram"

# 5. Sube la rama y abre un pull request
git push origin docs/mejorar-guia-telegram
```

Prefijos de commit recomendados: `docs:`, `workflow:`, `exercise:`, `fix:`, `chore:`, `ci:`.

## Añadir o modificar un workflow

Cada workflow debe cumplir estas reglas. El pull request se revisará contra esta lista.

1. **Exportado desde n8n**, no escrito a mano desde cero. Usa *Download* en el editor o `n8n export:workflow`.
2. **Sin credenciales**: elimina el bloque `credentials` de cada nodo o deja solo el nombre genérico sin `id` real.
3. **Sin datos personales**: sustituye IDs de hojas, chats, correos y etiquetas por marcadores `REEMPLAZAR_...`.
4. **Sin `pinData`** con datos reales y sin `staticData`.
5. **Nombres de nodos en español** y descriptivos (`Validar mensaje`, no `Code1`).
6. **Nodo de configuración**: si el workflow necesita valores del usuario, agrúpalos en un nodo *Edit Fields* llamado `Configuración`.
7. **Notas adhesivas** (*Sticky Notes*) que expliquen las secciones principales.
8. **README.md propio** en la carpeta del workflow siguiendo la estructura de los existentes (objetivo, dificultad, diagrama, requisitos, configuración nodo por nodo, datos de prueba, resultado esperado, errores frecuentes, mejoras y seguridad).
9. **Validación**: `python scripts/validate-workflows.py` debe terminar sin errores.
10. **Estado de verificación honesto**: indica en el README si el workflow se ha validado de forma estática, importado, ejecutado o probado con la integración real.

## Corregir o ampliar documentación

- Usa enlaces relativos para los archivos del repositorio.
- Comprueba que los enlaces funcionan en la vista previa de GitHub.
- Los diagramas se escriben en Mermaid dentro del Markdown.
- No añadas capturas de pantalla con datos reales. Si añades capturas, colócalas en `assets/screenshots/` y usa datos ficticios.

## Proponer ejercicios

Un ejercicio debe incluir:

- Nivel (`beginner`, `intermediate`, `advanced`).
- Objetivo de aprendizaje.
- Enunciado.
- Pistas opcionales.
- Solución explicada.
- Resultado esperado comprobable.

Colócalo en el archivo del nivel correspondiente dentro de `exercises/`.

## Reportar errores

Incluye siempre:

- Versión de n8n (menú *Settings > About n8n* o `docker compose exec n8n n8n --version`).
- Método de instalación (Docker Compose del taller, npm, n8n Cloud).
- Workflow o documento afectado.
- Pasos para reproducir, resultado esperado y resultado obtenido.
- Mensaje de error **sin** tokens, correos ni datos personales.

## Estilo de escritura

- Español neutro, en segunda persona (*"abre el nodo"*).
- Nombres técnicos en su forma original: *Workflow*, *Trigger*, *Webhook*, *Code node*.
- Frases cortas, un paso por línea en las instrucciones.
- Sin emojis.
- Advertencias con el formato de GitHub: `> [!WARNING]`, `> [!NOTE]`, `> [!TIP]`.

## Licencia de las contribuciones

Al enviar una contribución aceptas que:

- El código (workflows, scripts, configuración) se publica bajo [MIT](LICENSE).
- La documentación y el material educativo se publican bajo [CC BY 4.0](LICENSE-DOCS).
