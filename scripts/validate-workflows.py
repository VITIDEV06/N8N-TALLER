#!/usr/bin/env python3
"""
Validación estática de los workflows de n8n del taller.

Comprueba, sin necesidad de una instancia de n8n:
  - JSON válido.
  - Estructura básica (name, nodes, connections, settings).
  - Nombre del workflow.
  - Existencia de nodos y de al menos un trigger.
  - Identificadores de nodo presentes y únicos; nombres únicos.
  - Campos obligatorios de cada nodo (type, typeVersion, position, parameters).
  - Conexiones: origen y destino existen, tipo e índices correctos.
  - Referencias entre nodos en expresiones y código: $('Nodo') y $node["Nodo"].
  - Ausencia de secretos y de referencias a credenciales personales.
  - Ausencia de datos fijados (pinData) y de datos estáticos.

IMPORTANTE: esto es una validación ESTÁTICA. No demuestra que el workflow se
importe ni se ejecute correctamente en n8n. Ver la sección "Estado de
verificación" del README.

Uso:
  python scripts/validate-workflows.py                 # valida workflows/ y exercises/
  python scripts/validate-workflows.py ruta/a/archivo.json otra/carpeta
  python scripts/validate-workflows.py --strict        # los avisos también fallan

Solo usa la biblioteca estándar de Python (3.9 o superior).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DIRS = ["workflows", "exercises"]

TRIGGER_TYPES = {
    "n8n-nodes-base.manualTrigger",
    "n8n-nodes-base.scheduleTrigger",
    "n8n-nodes-base.webhook",
    "n8n-nodes-base.errorTrigger",
    "n8n-nodes-base.executeWorkflowTrigger",
}
STICKY_TYPE = "n8n-nodes-base.stickyNote"
CONNECTION_TYPE = "main"

# Patrones de secretos frecuentes. Se buscan en todo el contenido del archivo.
SECRET_PATTERNS = {
    "token de bot de Telegram": re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b"),
    "API key de OpenAI": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}"),
    "API key de Groq": re.compile(r"\bgsk_[A-Za-z0-9]{20,}"),
    "API key de Google": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "token de GitHub": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
    "clave privada": re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"),
    "secreto de cliente OAuth de Google": re.compile(r"\bGOCSPX-[A-Za-z0-9_-]{20,}"),
    "token Bearer literal": re.compile(r"Bearer\s+[A-Za-z0-9._-]{30,}"),
}

NODE_REF_PATTERNS = [
    re.compile(r"\$\(\s*'([^']+)'\s*\)"),
    re.compile(r'\$\(\s*"([^"]+)"\s*\)'),
    re.compile(r"\$node\[\s*'([^']+)'\s*\]"),
    re.compile(r'\$node\[\s*"([^"]+)"\s*\]'),
]


@dataclass
class Report:
    path: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    name: str = ""
    node_count: int = 0

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def is_trigger(node_type: str) -> bool:
    return node_type in TRIGGER_TYPES or node_type.endswith("Trigger")


def iter_strings(value):
    """Recorre recursivamente un valor JSON y devuelve todas sus cadenas."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from iter_strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from iter_strings(v)


def validate_nodes(data: dict, rep: Report) -> dict[str, dict]:
    nodes = data.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        rep.error("'nodes' debe ser una lista con al menos un nodo")
        return {}

    by_name: dict[str, dict] = {}
    ids: set[str] = set()
    for i, node in enumerate(nodes):
        where = f"nodo #{i}"
        if not isinstance(node, dict):
            rep.error(f"{where}: no es un objeto")
            continue
        name = node.get("name")
        if not isinstance(name, str) or not name.strip():
            rep.error(f"{where}: falta 'name'")
            continue
        where = f"nodo '{name}'"
        if name in by_name:
            rep.error(f"{where}: nombre duplicado")
        by_name[name] = node

        node_id = node.get("id")
        if not isinstance(node_id, str) or not node_id.strip():
            rep.error(f"{where}: falta el identificador 'id'")
        elif node_id in ids:
            rep.error(f"{where}: identificador duplicado '{node_id}'")
        else:
            ids.add(node_id)

        node_type = node.get("type")
        if not isinstance(node_type, str) or "." not in node_type:
            rep.error(f"{where}: 'type' no válido ({node_type!r})")
        version = node.get("typeVersion")
        if not isinstance(version, (int, float)) or isinstance(version, bool) or version <= 0:
            rep.error(f"{where}: 'typeVersion' debe ser un número positivo")
        pos = node.get("position")
        if not (isinstance(pos, list) and len(pos) == 2 and all(isinstance(p, (int, float)) for p in pos)):
            rep.error(f"{where}: 'position' debe ser [x, y]")
        if not isinstance(node.get("parameters"), dict):
            rep.error(f"{where}: 'parameters' debe ser un objeto")

        creds = node.get("credentials")
        if creds:
            for cred_type, ref in creds.items():
                if isinstance(ref, dict) and ref.get("id"):
                    rep.error(f"{where}: contiene una referencia a una credencial personal ({cred_type}); elimínala antes de publicar")
    return by_name


def validate_connections(data: dict, nodes: dict[str, dict], rep: Report) -> set[str]:
    connected: set[str] = set()
    conns = data.get("connections")
    if not isinstance(conns, dict):
        rep.error("'connections' debe ser un objeto")
        return connected

    for src, outputs in conns.items():
        if src not in nodes:
            rep.error(f"conexión desde un nodo inexistente: '{src}'")
            continue
        if not isinstance(outputs, dict):
            rep.error(f"conexiones de '{src}': formato no válido")
            continue
        for conn_type, branches in outputs.items():
            if not isinstance(branches, list):
                rep.error(f"conexiones de '{src}' ({conn_type}): deben ser una lista de salidas")
                continue
            for out_index, branch in enumerate(branches):
                if branch is None:
                    continue
                if not isinstance(branch, list):
                    rep.error(f"conexiones de '{src}' salida {out_index}: deben ser una lista")
                    continue
                for target in branch:
                    dst = target.get("node") if isinstance(target, dict) else None
                    if dst not in nodes:
                        rep.error(f"'{src}' (salida {out_index}) conecta con un nodo inexistente: '{dst}'")
                        continue
                    if target.get("type") != conn_type:
                        rep.error(f"'{src}' -> '{dst}': el tipo de conexión no coincide ({target.get('type')!r})")
                    idx = target.get("index")
                    if not isinstance(idx, int) or idx < 0:
                        rep.error(f"'{src}' -> '{dst}': índice de entrada no válido ({idx!r})")
                    if conn_type != CONNECTION_TYPE:
                        rep.warn(f"'{src}' -> '{dst}': tipo de conexión no estándar '{conn_type}'")
                    connected.update({src, dst})
    return connected


def validate_references(nodes: dict[str, dict], rep: Report) -> None:
    for name, node in nodes.items():
        for text in iter_strings(node.get("parameters", {})):
            for pattern in NODE_REF_PATTERNS:
                for ref in pattern.findall(text):
                    if ref not in nodes:
                        rep.error(f"nodo '{name}': referencia a un nodo inexistente '{ref}'")


def validate_secrets(raw: str, rep: Report) -> None:
    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(raw):
            rep.error(f"posible secreto detectado: {label}")


def validate_file(path: Path) -> Report:
    rep = Report(path)
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        rep.error("el archivo no está codificado en UTF-8")
        return rep
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        rep.error(f"JSON no válido: {exc}")
        return rep
    if not isinstance(data, dict):
        rep.error("el documento raíz debe ser un objeto JSON")
        return rep

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        rep.error("falta el nombre del workflow ('name')")
    else:
        rep.name = name

    nodes = validate_nodes(data, rep)
    rep.node_count = len(nodes)
    connected = validate_connections(data, nodes, rep)
    validate_references(nodes, rep)
    validate_secrets(raw, rep)

    functional = {n: v for n, v in nodes.items() if v.get("type") != STICKY_TYPE}
    if functional and not any(is_trigger(str(v.get("type", ""))) for v in functional.values()):
        rep.warn("el workflow no tiene ningún nodo trigger")
    if len(functional) > 1:
        for n in functional:
            if n not in connected:
                rep.warn(f"nodo desconectado: '{n}'")

    if not isinstance(data.get("settings"), dict):
        rep.warn("falta el objeto 'settings'")
    if data.get("pinData"):
        rep.warn("contiene datos fijados (pinData); revisa que no incluyan datos personales")
    if data.get("staticData"):
        rep.warn("contiene 'staticData'; elimínalo antes de publicar")
    if data.get("active") is True:
        rep.warn("el workflow está marcado como activo; expórtalo desactivado")
    return rep


def collect(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        target = Path(p)
        if not target.is_absolute():
            target = (Path.cwd() / target) if target.exists() else (REPO_ROOT / target)
        if target.is_file():
            files.append(target)
        elif target.is_dir():
            files.extend(sorted(f for f in target.rglob("*.json") if f.is_file()))
        else:
            print(f"Aviso: no existe la ruta {p}", file=sys.stderr)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description="Validación estática de workflows de n8n.")
    parser.add_argument("paths", nargs="*", help="Archivos o carpetas (por defecto: workflows/ y exercises/)")
    parser.add_argument("--strict", action="store_true", help="tratar los avisos como errores")
    parser.add_argument("--quiet", action="store_true", help="mostrar solo archivos con problemas")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    files = collect(args.paths or DEFAULT_DIRS)
    if not files:
        print("No se encontraron archivos JSON para validar.")
        return 1

    total_errors = total_warnings = 0
    for path in files:
        rep = validate_file(path)
        try:
            shown = path.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            shown = str(path)
        total_errors += len(rep.errors)
        total_warnings += len(rep.warnings)
        failed = bool(rep.errors) or (args.strict and rep.warnings)
        if args.quiet and not rep.errors and not rep.warnings:
            continue
        status = "FALLO" if failed else ("AVISO" if rep.warnings else "OK")
        print(f"[{status:5}] {shown}  ({rep.node_count} nodos) {rep.name}")
        for e in rep.errors:
            print(f"         error: {e}")
        for w in rep.warnings:
            print(f"         aviso: {w}")

    print()
    print(f"Archivos: {len(files)} | Errores: {total_errors} | Avisos: {total_warnings}")
    print("Validación estática: no sustituye a importar y ejecutar el workflow en n8n.")
    if total_errors or (args.strict and total_warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
