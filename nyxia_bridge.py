#!/usr/bin/env python3
"""
Data Bridge - Python SDK para Desenvolvedores e Agentes de IA
API limpa e tipada para orquestração de custódia e transporte de dados.
"""

from pathlib import Path
from typing import List, Dict, Optional, Any
import mcp_server

def list_modules(only_detected: bool = False) -> Dict[str, Any]:
    """Lista todos os módulos reconhecidos pelo sistema."""
    return mcp_server.handle_list_modules({"only_detected": only_detected})

def export_package(
    profile: Optional[str] = None,
    modules: Optional[List[str]] = None,
    custom_paths: Optional[Dict[str, str]] = None,
    output_path: Optional[str] = None,
    compression_mode: str = "lzma",
    quiesce_processes: bool = True
) -> Dict[str, Any]:
    """Empacota e exporta módulos de dados em contêiner soberano .agpkg."""
    args = {
        "profile": profile,
        "modules": modules or [],
        "custom_paths": custom_paths or {},
        "output_path": output_path,
        "compression_mode": compression_mode,
        "quiesce_processes": quiesce_processes
    }
    return mcp_server.handle_export_package(args)

def inspect_package(package_path: str) -> Dict[str, Any]:
    """Inspeciona o manifesto e metadados de um pacote .agpkg sem descompactar."""
    return mcp_server.handle_inspect_package({"package_path": package_path})

def restore_package(
    package_path: str,
    dest_root: Optional[str] = None
) -> Dict[str, Any]:
    """Restaura os dados contidos em um pacote .agpkg no sistema atual."""
    return mcp_server.handle_restore_package({
        "package_path": package_path,
        "dest_root": dest_root
    })
