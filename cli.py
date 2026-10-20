#!/usr/bin/env python3
"""
Data Bridge - Interface de Linha de Comando (CLI) para Agentes de IA & SysAdmins.
Permite listar, inspecionar, exportar e restaurar estados cognitivos e configurações de forma determinística via terminal.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Garante saída em UTF-8 no terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).parent))
import engine
import presets

def cmd_list(args):
    catalog = presets.get_catalog()
    if args.detected:
        catalog = [c for c in catalog if c["detected"]]

    if args.json:
        payload = {
            "status": "success",
            "total_modules": len(catalog),
            "modules": catalog,
            "profiles": presets.PROFILES,
            "categories": presets.CATEGORIES
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    print("=" * 68)
    print("  DATA BRIDGE - CATÁLOGO DE MÓDULOS DISPONÍVEIS")
    print("=" * 68)
    print(f"\n[ PERFIS PRONTOS (1-CLIQUE) ]")
    for prof in presets.PROFILES:
        print(f"  • {prof['id']:<26} -> {prof['title']} ({len(prof.get('ids', []))} módulos)")

    print(f"\n[ MÓDULOS INDIVIDUAIS ]")
    print(f"  {'STATUS':<12} {'ID DO MÓDULO':<24} {'PASTA NO PACOTE':<22} {'CAMINHO DEFAULT'}")
    print("  " + "-" * 75)
    for p in catalog:
        status = "[PRESENTE]" if p["detected"] else "[AUSENTE]"
        print(f"  {status:<12} {p['id']:<24} {p['archive_folder']:<22} {p['default_path']}")
    print("\n" + "=" * 68)
    return 0

def cmd_export(args):
    target_ids = set()
    if args.profile:
        found_profile = False
        for prof in presets.PROFILES:
            if prof["id"] == args.profile:
                target_ids.update(prof.get("ids", []))
                found_profile = True
                break
        if not found_profile:
            err = f"Perfil '{args.profile}' não encontrado. Use 'nyxia-bridge list' para ver os IDs válidos."
            if args.json:
                print(json.dumps({"status": "error", "message": err}, ensure_ascii=False))
            else:
                print(f"Erro: {err}", file=sys.stderr)
            return 1

    if args.modules:
        for m in args.modules.split(","):
            m = m.strip()
            if m:
                target_ids.add(m)

    catalog = presets.get_catalog()
    targets = {}
    procs_to_check = set()

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

    if args.paths:
        for item in args.paths:
            if ":" in item:
                src, folder = item.split(":", 1)
            elif "=" in item:
                src, folder = item.split("=", 1)
            else:
                src, folder = item, Path(item).name or "custom"
            p_src = Path(src)
            if p_src.exists():
                targets[f"custom_{folder}"] = {
                    "source_path": str(p_src),
                    "archive_folder": folder
                }

    if not targets:
        err = "Nenhum dos módulos ou caminhos indicados foi localizado no disco deste computador."
        if args.json:
            print(json.dumps({"status": "error", "message": err}, ensure_ascii=False))
        else:
            print(f"Erro: {err}", file=sys.stderr)
        return 1

    out_file = args.output
    if not out_file:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_file = f"nyxia_pacote_{ts}.agpkg"
    out_file = str(Path(out_file).resolve())

    if not args.no_kill and procs_to_check:
        running = engine.check_process_running(list(procs_to_check))
        if running:
            if not args.json:
                print(f"[Aviso] Encerrando {len(running)} processos concorrentes para integridade de SQLite...")
            engine.kill_processes(list(procs_to_check))

    if not args.json:
        print(f"Compactando {len(targets)} módulos com algoritmo {args.mode.upper()}...")

    start_time = datetime.now()
    engine.compress_package(
        targets=targets,
        output_filepath=out_file,
        compression_mode=args.mode
    )
    elapsed = (datetime.now() - start_time).total_seconds()
    fsize = Path(out_file).stat().st_size

    if args.json:
        payload = {
            "status": "success",
            "output_file": out_file,
            "size_bytes": fsize,
            "size_mb": round(fsize / (1024 * 1024), 2),
            "compression_mode": args.mode,
            "elapsed_seconds": round(elapsed, 2),
            "modules_packaged": list(targets.keys())
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print("\n" + "=" * 68)
        print("  PACOTE DE TRANSPORTE GERADO COM SUCESSO!")
        print("=" * 68)
        print(f"  Arquivo: {out_file}")
        print(f"  Tamanho: {fsize / (1024*1024):.2f} MB")
        print(f"  Módulos: {len(targets)} incluídos")
        print(f"  Tempo:   {elapsed:.2f}s")
        print("=" * 68)
    return 0

def cmd_inspect(args):
    pkg_path = str(Path(args.package_path).resolve())
    if not Path(pkg_path).exists():
        err = f"Arquivo de pacote não encontrado: {pkg_path}"
        if args.json:
            print(json.dumps({"status": "error", "message": err}, ensure_ascii=False))
        else:
            print(f"Erro: {err}", file=sys.stderr)
        return 1

    manifest = engine.read_manifest(pkg_path)
    fsize = Path(pkg_path).stat().st_size

    if args.json:
        payload = {
            "status": "success",
            "package_path": pkg_path,
            "file_size_bytes": fsize,
            "file_size_mb": round(fsize / (1024 * 1024), 2),
            "manifest": manifest
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    print("=" * 68)
    print("  DATA BRIDGE - INSPETOR DE PACOTE")
    print("=" * 68)
    print(f"  Arquivo:       {pkg_path}")
    print(f"  Tamanho Disco: {fsize / (1024*1024):.2f} MB")
    print(f"  Gerado em:     {manifest.get('created_at', 'Desconhecido')}")
    print(f"  Algoritmo:     {manifest.get('compression_mode', '').upper()}")
    print(f"  Volumetria:    {manifest.get('total_uncompressed_bytes', 0)/(1024*1024):.2f} MB ({manifest.get('total_files', 0)} arquivos)")
    print("\n  Módulos Contidos:")
    for k, v in manifest.get("modules", {}).items():
        print(f"    • {k:<25} -> {v.get('total_files', 0)} arquivos ({v.get('total_bytes', 0)/(1024*1024):.2f} MB)")
    print("=" * 68)
    return 0

def cmd_restore(args):
    pkg_path = str(Path(args.package_path).resolve())
    if not Path(pkg_path).exists():
        err = f"Arquivo de pacote não encontrado: {pkg_path}"
        if args.json:
            print(json.dumps({"status": "error", "message": err}, ensure_ascii=False))
        else:
            print(f"Erro: {err}", file=sys.stderr)
        return 1

    manifest = engine.read_manifest(pkg_path)
    modules = manifest.get("modules", {})
    catalog_map = {p["archive_folder"]: p["default_path"] for p in presets.PRESETS_CATALOG}
    destinations = {}

    for mod_key, mod_info in modules.items():
        arc_folder = mod_info.get("archive_folder", mod_key)
        if args.dest:
            destinations[arc_folder] = str(Path(args.dest) / arc_folder)
        elif arc_folder in catalog_map:
            destinations[arc_folder] = catalog_map[arc_folder]
        else:
            orig_path = mod_info.get("source_path", "")
            folder_name = os.path.basename(orig_path) or "RestoredFolder"
            destinations[arc_folder] = str(Path.home() / "NyxiaRestored" / folder_name)

    if not args.json:
        print(f"Restaurando {len(destinations)} módulos...")

    engine.decompress_package(
        package_path=pkg_path,
        destinations=destinations
    )

    if args.json:
        payload = {
            "status": "success",
            "package_path": pkg_path,
            "restored_modules": list(destinations.keys()),
            "destinations": destinations
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print("\n" + "=" * 68)
        print("  RESTAURAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 68)
        for k, v in destinations.items():
            print(f"    • {k:<20} -> {v}")
        print("=" * 68)
    return 0

def cmd_mcp(args):
    import mcp_server
    mcp_server.run_mcp_server()
    return 0

def main():
    parser = argparse.ArgumentParser(
        prog="nyxia-bridge",
        description="Data Bridge - Custódia e Transporte de Dados para Humanos e Agentes de IA (Windows & Linux Ubuntu)"
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Comandos disponíveis")

    # Subcomando: list
    p_list = subparsers.add_parser("list", help="Lista todos os módulos e perfis disponíveis")
    p_list.add_argument("--json", action="store_true", help="Saída estruturada em formato JSON para Agentes de IA")
    p_list.add_argument("--detected", action="store_true", help="Filtra apenas módulos presentes no disco atual")

    # Subcomando: export
    p_export = subparsers.add_parser("export", help="Empacota módulos de dados e cria o contêiner .agpkg")
    p_export.add_argument("-p", "--profile", help="ID do perfil rápido (ex: profile_ai_nomad, profile_it_sysadmin)")
    p_export.add_argument("-m", "--modules", help="Lista separada por vírgula de IDs de módulos (ex: antigravity_gemini,claude_code)")
    p_export.add_argument("--paths", action="append", help="Caminhos adicionais no formato 'caminho=pasta' ou 'caminho:pasta'")
    p_export.add_argument("-o", "--output", help="Caminho do arquivo .agpkg de saída")
    p_export.add_argument("--mode", choices=["lzma", "deflate"], default="lzma", help="Modo de compressão (lzma ou deflate)")
    p_export.add_argument("--no-kill", action="store_true", help="Não encerrar processos de IDE concorrentes")
    p_export.add_argument("--json", action="store_true", help="Saída estruturada em JSON para Agentes de IA")

    # Subcomando: inspect
    p_inspect = subparsers.add_parser("inspect", help="Inspeciona os metadados de um pacote .agpkg sem descompactar")
    p_inspect.add_argument("package_path", help="Caminho do arquivo de pacote (.agpkg)")
    p_inspect.add_argument("--json", action="store_true", help="Saída estruturada em JSON para Agentes de IA")

    # Subcomando: restore
    p_restore = subparsers.add_parser("restore", help="Restaura os dados contidos no pacote neste computador")
    p_restore.add_argument("package_path", help="Caminho do arquivo de pacote (.agpkg)")
    p_restore.add_argument("--dest", help="Diretório raiz customizado de destino opcional")
    p_restore.add_argument("--json", action="store_true", help="Saída estruturada em JSON para Agentes de IA")

    # Subcomando: mcp
    p_mcp = subparsers.add_parser("mcp", help="Inicia o servidor MCP (Model Context Protocol) via stdio para Agentes de IA")

    args, unknown = parser.parse_known_args()

    if args.subcommand == "list":
        return cmd_list(args)
    elif args.subcommand == "export":
        return cmd_export(args)
    elif args.subcommand == "inspect":
        return cmd_inspect(args)
    elif args.subcommand == "restore":
        return cmd_restore(args)
    elif args.subcommand == "mcp":
        return cmd_mcp(args)
    else:
        parser.print_help()
        return 0

if __name__ == "__main__":
    sys.exit(main() or 0)
