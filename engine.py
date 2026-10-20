import os
import sys
import json
import shutil
import hashlib
import zipfile
import py7zr
import psutil
from pathlib import Path
from datetime import datetime

# Diretórios e extensões que nunca devem ser incluídos em backups (lixo de cache / temporários)
BLACKLIST_DIRS = {
    "Cache", "GPUCache", "Code Cache", "DawnCache", "DawnWebGPUCache",
    "Crashpad", "logs", "logs_old", "temp", "tmp", "session_cache",
    ".git", "__pycache__", "node_modules", ".pytest_cache"
}

BLACKLIST_EXTENSIONS = {
    ".lock", ".tmp", ".log", ".dmp"
}

def is_blacklisted(rel_path_str: str) -> bool:
    """Verifica se parte do caminho relativo contém uma pasta ou arquivo ignorável."""
    parts = Path(rel_path_str).parts
    for part in parts:
        if part in BLACKLIST_DIRS:
            return True
    ext = os.path.splitext(rel_path_str)[1].lower()
    if ext in BLACKLIST_EXTENSIONS:
        return True
    return False

def _normalize_proc_names(process_names: list) -> set:
    """Normaliza nomes de processos para compatibilidade Windows e Linux (com ou sem .exe)."""
    names = set()
    for n in process_names:
        nl = n.lower()
        names.add(nl)
        if nl.endswith(".exe"):
            names.add(nl[:-4])
    return names

def check_process_running(process_names: list) -> list:
    """Verifica se processos com os nomes especificados estão ativos (Windows & Linux)."""
    running = []
    targets = _normalize_proc_names(process_names)
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pname = proc.info.get('name')
            if pname:
                pl = pname.lower()
                pl_base = pl[:-4] if pl.endswith(".exe") else pl
                if pl in targets or pl_base in targets:
                    running.append((proc.info['pid'], pname))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return running

def kill_processes(process_names: list) -> int:
    """Encerra com segurança processos em execução (Windows & Linux)."""
    killed = 0
    targets = _normalize_proc_names(process_names)
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pname = proc.info.get('name')
            if pname:
                pl = pname.lower()
                pl_base = pl[:-4] if pl.endswith(".exe") else pl
                if pl in targets or pl_base in targets:
                    proc.terminate()
                    killed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return killed

def calculate_folder_stats(folder_path: Path):
    """Calcula total de arquivos elegíveis e contagem total de bytes para cálculo suave da barra."""
    total_files = 0
    total_bytes = 0
    if not folder_path.exists():
        return total_files, total_bytes

    for root, dirs, files in os.walk(folder_path):
        # Remove diretórios na blacklist antes de descer
        dirs[:] = [d for d in dirs if d not in BLACKLIST_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in BLACKLIST_EXTENSIONS:
                continue
            fp = Path(root) / f
            try:
                total_bytes += fp.stat().st_size
                total_files += 1
            except Exception:
                pass
    return total_files, total_bytes

def compress_package(
    targets: dict,
    output_filepath: str,
    compression_mode: str = "lzma",  # "lzma" (Super) ou "deflate" (Rápido)
    progress_callback = None,
    cancel_flag = None
):
    """
    Empacota múltiplos diretórios mapeados em um único contêiner (.agpkg / .7z / .zip)
    gerando o manifest.json internamente.
    """
    total_bytes_all = 0
    total_files_all = 0
    module_stats = {}

    for mod_key, mod_info in targets.items():
        src_dir = Path(mod_info["source_path"])
        f_count, b_count = calculate_folder_stats(src_dir)
        total_files_all += f_count
        total_bytes_all += b_count
        module_stats[mod_key] = {
            "source_path": str(src_dir),
            "archive_folder": mod_info["archive_folder"],
            "total_files": f_count,
            "total_bytes": b_count
        }

    manifest = {
        "generator": "NyxiaDataBridge",
        "version": "1.14.0",
        "created_at": datetime.now().isoformat(),
        "compression_mode": compression_mode,
        "total_uncompressed_bytes": total_bytes_all,
        "total_files": total_files_all,
        "modules": module_stats
    }

    processed_bytes = 0
    out_path = Path(output_filepath)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Modo LZMA2 / 7z (Super Compressão de alta densidade)
    if compression_mode == "lzma":
        filters = [{'id': py7zr.FILTER_LZMA2, 'preset': 7}]
        with py7zr.SevenZipFile(output_filepath, 'w', filters=filters) as archive:
            # Escreve manifest como temporário
            manifest_json_str = json.dumps(manifest, indent=2)
            manifest_bytes = manifest_json_str.encode('utf-8')
            manifest_tmp = out_path.parent / "__manifest_tmp.json"
            with open(manifest_tmp, "wb") as f_m:
                f_m.write(manifest_bytes)
            archive.write(manifest_tmp, arcname="manifest.json")
            if manifest_tmp.exists():
                manifest_tmp.unlink()

            for mod_key, mod_info in targets.items():
                src_path = Path(mod_info["source_path"])
                arc_folder = mod_info["archive_folder"]
                if not src_path.exists():
                    continue

                for root, dirs, files in os.walk(src_path):
                    if cancel_flag and cancel_flag():
                        raise InterruptedError("Operação cancelada pelo usuário.")
                    dirs[:] = [d for d in dirs if d not in BLACKLIST_DIRS]
                    for f in files:
                        if cancel_flag and cancel_flag():
                            raise InterruptedError("Operação cancelada pelo usuário.")
                        ext = os.path.splitext(f)[1].lower()
                        if ext in BLACKLIST_EXTENSIONS:
                            continue
                        f_full = Path(root) / f
                        rel_file = f_full.relative_to(src_path)
                        arc_name = str(Path(arc_folder) / rel_file).replace("\\", "/")

                        try:
                            f_size = f_full.stat().st_size
                            archive.write(f_full, arcname=arc_name)
                            processed_bytes += f_size
                            if progress_callback:
                                frac = processed_bytes / total_bytes_all if total_bytes_all > 0 else 1.0
                                progress_callback(frac, str(rel_file), processed_bytes, total_bytes_all)
                        except Exception as e:
                            # Ignora arquivos travados ou voláteis
                            pass

    # 2. Modo DEFLATE / ZIP (Rápido e padrão)
    else:
        with zipfile.ZipFile(output_filepath, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
            zipf.writestr("manifest.json", json.dumps(manifest, indent=2))
            for mod_key, mod_info in targets.items():
                src_path = Path(mod_info["source_path"])
                arc_folder = mod_info["archive_folder"]
                if not src_path.exists():
                    continue

                for root, dirs, files in os.walk(src_path):
                    if cancel_flag and cancel_flag():
                        raise InterruptedError("Operação cancelada pelo usuário.")
                    dirs[:] = [d for d in dirs if d not in BLACKLIST_DIRS]
                    for f in files:
                        if cancel_flag and cancel_flag():
                            raise InterruptedError("Operação cancelada pelo usuário.")
                        ext = os.path.splitext(f)[1].lower()
                        if ext in BLACKLIST_EXTENSIONS:
                            continue
                        f_full = Path(root) / f
                        rel_file = f_full.relative_to(src_path)
                        arc_name = str(Path(arc_folder) / rel_file).replace("\\", "/")

                        try:
                            f_size = f_full.stat().st_size
                            zipf.write(f_full, arcname=arc_name)
                            processed_bytes += f_size
                            if progress_callback:
                                frac = processed_bytes / total_bytes_all if total_bytes_all > 0 else 1.0
                                progress_callback(frac, str(rel_file), processed_bytes, total_bytes_all)
                        except Exception:
                            pass

    return manifest

def read_manifest(package_path: str) -> dict:
    """Lê e retorna o manifest.json de um arquivo .agpkg / .7z / .zip."""
    import tempfile
    pkg = Path(package_path)
    if not pkg.exists():
        raise FileNotFoundError(f"Arquivo de pacote não encontrado: {package_path}")

    # Tenta ler como 7z
    if py7zr.is_7zfile(str(pkg)):
        with py7zr.SevenZipFile(str(pkg), 'r') as archive:
            if "manifest.json" in archive.getnames():
                with tempfile.TemporaryDirectory() as tmpdir:
                    archive.extract(targets=["manifest.json"], path=tmpdir)
                    mf = Path(tmpdir) / "manifest.json"
                    if mf.exists():
                        with open(mf, "r", encoding="utf-8") as f:
                            return json.load(f)
    # Tenta ler como ZIP
    elif zipfile.is_zipfile(str(pkg)):
        with zipfile.ZipFile(str(pkg), 'r') as zipf:
            if "manifest.json" in zipf.namelist():
                content = zipf.read("manifest.json").decode('utf-8')
                return json.loads(content)
    raise ValueError("Formato de pacote inválido ou manifest.json ausente.")

def decompress_package(
    package_path: str,
    destinations: dict,
    progress_callback = None,
    cancel_flag = None
):
    """
    Restaura os arquivos do contêiner para os diretórios mapeados no destino.
    destinations formato: { 'arc_folder_name': Path_Destino }
    """
    pkg = Path(package_path)
    manifest = read_manifest(str(pkg))
    total_uncompressed = manifest.get("total_uncompressed_bytes", 1)

    restored_bytes = 0

    if py7zr.is_7zfile(str(pkg)):
        with py7zr.SevenZipFile(str(pkg), 'r') as archive:
            # Lista membros
            members = archive.list()
            for member in members:
                if cancel_flag and cancel_flag():
                    raise InterruptedError("Operação cancelada pelo usuário.")
                if member.is_directory or member.filename == "manifest.json":
                    continue

                # Identifica qual arc_folder
                parts = Path(member.filename).parts
                if not parts:
                    continue
                top_folder = parts[0]

                if top_folder in destinations:
                    dest_root = Path(destinations[top_folder])
                    rel_subpath = Path(*parts[1:])
                    out_file = dest_root / rel_subpath
                    out_file.parent.mkdir(parents=True, exist_ok=True)

                    # Extrai arquivo individual
                    file_dict = archive.read([member.filename])
                    if member.filename in file_dict:
                        with open(out_file, 'wb') as dst:
                            shutil.copyfileobj(file_dict[member.filename], dst)

                    restored_bytes += member.uncompressed
                    if progress_callback:
                        frac = restored_bytes / total_uncompressed if total_uncompressed > 0 else 1.0
                        progress_callback(frac, str(rel_subpath), restored_bytes, total_uncompressed)

    elif zipfile.is_zipfile(str(pkg)):
        with zipfile.ZipFile(str(pkg), 'r') as zipf:
            for info in zipf.infolist():
                if cancel_flag and cancel_flag():
                    raise InterruptedError("Operação cancelada pelo usuário.")
                if info.is_dir() or info.filename == "manifest.json":
                    continue

                parts = Path(info.filename).parts
                if not parts:
                    continue
                top_folder = parts[0]

                if top_folder in destinations:
                    dest_root = Path(destinations[top_folder])
                    rel_subpath = Path(*parts[1:])
                    out_file = dest_root / rel_subpath
                    out_file.parent.mkdir(parents=True, exist_ok=True)

                    with zipf.open(info.filename) as src, open(out_file, 'wb') as dst:
                        shutil.copyfileobj(src, dst)

                    restored_bytes += info.file_size
                    if progress_callback:
                        frac = restored_bytes / total_uncompressed if total_uncompressed > 0 else 1.0
                        progress_callback(frac, str(rel_subpath), restored_bytes, total_uncompressed)

    return True
