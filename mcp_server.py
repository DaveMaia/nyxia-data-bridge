#!/usr/bin/env python3
"""
Data Bridge - Model Context Protocol (MCP) Server
Permite que Agentes de IA (Claude Code, Antigravity, Cursor, etc.)
interajam diretamente com o motor de transporte e custódia de dados via protocolo MCP stdio.
"""

import sys
import os
import json
import logging
from pathlib import Path
from datetime import datetime

# Configura logger em stderr para não poluir o stdout do protocolo JSON-RPC
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("nyxia_mcp")

# Adiciona diretório atual ao path
sys.path.insert(0, str(Path(__file__).parent))
import engine
import presets

SERVER_INFO = {
    "name": "nyxia-data-bridge",
    "version": "1.14.0"
}

TOOLS = [
    {
        "name": "nyxia_list_modules",
        "description": "Lista todos os módulos de estado cognitivo (Antigravity, Claude Code, Cursor, Windsurf, SSH, Docker, Obsidian, etc.) reconhecidos nesta máquina e se estão presentes no disco.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "only_detected": {
                    "type": "boolean",
                    "description": "Se verdadeiro, lista apenas os módulos que existem fisicamente no disco deste computador."
                }
            }
        }
    },
    {
        "name": "nyxia_export_package",
        "description": "Empacota e exporta módulos de IA ou perfis da estação de trabalho em um contêiner soberano .agpkg com integridade atômica e super compressão LZMA2.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "profile": {
                    "type": "string",
                    "description": "ID do perfil rápido (ex: profile_ai_nomad, profile_it_sysadmin, profile_full_workstation, profile_minimal)."
                },
                "modules": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Lista explícita de IDs de módulos a empacotar (ex: ['antigravity_gemini', 'claude_code', 'ssh_keys'])."
                },
                "custom_paths": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                    "description": "Mapeamento opcional de caminhos adicionais { 'caminho_no_disco': 'pasta_no_pacote' }."
                },
                "output_path": {
                    "type": "string",
                    "description": "Caminho de saída para salvar o arquivo .agpkg. Se omitido, salva na pasta atual com timestamp."
                },
                "compression_mode": {
                    "type": "string",
                    "enum": ["lzma", "deflate"],
                    "default": "lzma",
                    "description": "Algoritmo de compressão: 'lzma' (Super Compressão até 85%) ou 'deflate' (Modo Rápido)."
                },
                "quiesce_processes": {
                    "type": "boolean",
                    "default": True,
                    "description": "Se verdadeiro, encerra com segurança processos de IDE ativos para proteger bancos SQLite (state.vscdb)."
                }
            }
        }
    },
    {
        "name": "nyxia_inspect_package",
        "description": "Inspeciona os metadados e o manifesto interno de um pacote (.agpkg, .7z ou .zip) sem descompactar.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "package_path": {
                    "type": "string",
                    "description": "Caminho do arquivo de pacote (.agpkg) a ser inspecionado."
                }
            },
            "required": ["package_path"]
        }
    },
    {
        "name": "nyxia_restore_package",
        "description": "Restaura o estado cognitivo e os diretórios contidos em um contêiner .agpkg diretamente nos caminhos correspondentes do sistema operacional.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "package_path": {
                    "type": "string",
                    "description": "Caminho do pacote (.agpkg) a restaurar."
                },
                "dest_root": {
                    "type": "string",
                    "description": "Diretório raiz customizado de destino opcional. Se omitido, restaura nos locais originais da máquina."
                }
            },
            "required": ["package_path"]
        }
    }
]

def handle_list_modules(arguments: dict) -> dict:
    only_detected = arguments.get("only_detected", False)
    catalog = presets.get_catalog()
    if only_detected:
        catalog = [c for c in catalog if c["detected"]]

    return {
        "status": "success",
        "total_count": len(catalog),
        "modules": catalog,
        "profiles": presets.PROFILES,
        "categories": presets.CATEGORIES
    }

def handle_export_package(arguments: dict) -> dict:
    profile_id = arguments.get("profile")
    module_ids = arguments.get("modules", [])
    custom_paths = arguments.get("custom_paths", {})
    mode = arguments.get("compression_mode", "lzma")
    quiesce = arguments.get("quiesce_processes", True)

    target_ids = set(module_ids)
    if profile_id:
        for p in presets.PROFILES:
            if p["id"] == profile_id:
                target_ids.update(p.get("ids", []))
                break

    targets = {}
    procs_to_check = set()
    catalog = presets.get_catalog()

    for p_info in catalog:
        if p_info["id"] in target_ids:
            p_path = Path(p_info["default_path"])
            if p_path.exists():
                targets[p_info["id"]] = {
                    "source_path": str(p_path),
                    "archive_folder": p_info["archive_folder"]
                }
                for pr in p_info.get("processes", []):
                    procs_to_check.add(pr)

    for c_path, arc_folder in custom_paths.items():
        cp = Path(c_path)
        if cp.exists():
            cid = f"custom_{arc_folder}"
            targets[cid] = {
                "source_path": str(cp),
                "archive_folder": arc_folder
            }

    if not targets:
        return {
            "status": "error",
            "message": "Nenhum diretório válido ou existente no disco foi localizado com base nos parâmetros informados."
        }

    out_file = arguments.get("output_path")
    if not out_file:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_file = str(Path.cwd() / f"nyxia_pacote_{ts}.agpkg")

    if quiesce and procs_to_check:
        running = engine.check_process_running(list(procs_to_check))
        if running:
            engine.kill_processes(list(procs_to_check))

    engine.compress_package(
        targets=targets,
        output_filepath=out_file,
        compression_mode=mode
    )

    file_size_bytes = Path(out_file).stat().st_size
    return {
        "status": "success",
        "output_file": out_file,
        "size_bytes": file_size_bytes,
        "size_mb": round(file_size_bytes / (1024 * 1024), 2),
        "compression_mode": mode,
        "packaged_modules": list(targets.keys())
    }

def handle_inspect_package(arguments: dict) -> dict:
    pkg_path = arguments.get("package_path")
    if not pkg_path or not Path(pkg_path).exists():
        return {"status": "error", "message": f"Arquivo não encontrado: {pkg_path}"}

    manifest = engine.read_manifest(pkg_path)
    return {
        "status": "success",
        "package_path": pkg_path,
        "file_size_bytes": Path(pkg_path).stat().st_size,
        "manifest": manifest
    }

def handle_restore_package(arguments: dict) -> dict:
    pkg_path = arguments.get("package_path")
    if not pkg_path or not Path(pkg_path).exists():
        return {"status": "error", "message": f"Arquivo não encontrado: {pkg_path}"}

    dest_root = arguments.get("dest_root")
    manifest = engine.read_manifest(pkg_path)
    modules = manifest.get("modules", {})

    destinations = {}
    catalog_map = {p["archive_folder"]: p["default_path"] for p in presets.PRESETS_CATALOG}

    for mod_key, mod_info in modules.items():
        arc_folder = mod_info.get("archive_folder", mod_key)
        if dest_root:
            destinations[arc_folder] = str(Path(dest_root) / arc_folder)
        elif arc_folder in catalog_map:
            destinations[arc_folder] = catalog_map[arc_folder]
        else:
            orig_path = mod_info.get("source_path", "")
            folder_name = os.path.basename(orig_path) or "RestoredFolder"
            destinations[arc_folder] = str(Path.home() / "NyxiaRestored" / folder_name)

    engine.decompress_package(
        package_path=pkg_path,
        destinations=destinations
    )

    return {
        "status": "success",
        "package_path": pkg_path,
        "restored_destinations": destinations
    }

def execute_tool(name: str, arguments: dict) -> dict:
    if name == "nyxia_list_modules":
        return handle_list_modules(arguments)
    elif name == "nyxia_export_package":
        return handle_export_package(arguments)
    elif name == "nyxia_inspect_package":
        return handle_inspect_package(arguments)
    elif name == "nyxia_restore_package":
        return handle_restore_package(arguments)
    else:
        raise ValueError(f"Ferramenta desconhecida: {name}")

def run_mcp_server():
    """Loop principal de escuta JSON-RPC 2.0 via stdio para Agentes de IA."""
    logger.info("Iniciando Data Bridge MCP Server no modo stdio...")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
            except json.JSONDecodeError as je:
                logger.error(f"Erro ao decodificar JSON: {je}")
                continue

            req_id = request.get("id")
            method = request.get("method")
            params = request.get("params", {})

            # Tratamento de métodos MCP
            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": SERVER_INFO
                    }
                }
            elif method == "notifications/initialized":
                # Notificação de inicialização (sem resposta exigida)
                continue
            elif method == "ping":
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {}
                }
            elif method == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": TOOLS
                    }
                }
            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                try:
                    result_data = execute_tool(tool_name, tool_args)
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(result_data, indent=2, ensure_ascii=False)
                                }
                            ]
                        }
                    }
                except Exception as ex:
                    logger.exception(f"Erro na execução da ferramenta {tool_name}")
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {
                            "code": -32000,
                            "message": str(ex)
                        }
                    }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32601,
                        "message": f"Método não implementado: {method}"
                    }
                }

            sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            sys.stdout.flush()

        except Exception as e:
            logger.exception(f"Exceção no loop do servidor MCP: {e}")

if __name__ == "__main__":
    run_mcp_server()
