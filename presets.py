import sys
import os
from pathlib import Path

HOME = Path.home()
USERPROFILE = os.environ.get("USERPROFILE") or str(HOME)
APPDATA = os.environ.get("APPDATA") or (str(HOME / ".config") if sys.platform != "win32" else str(HOME / "AppData" / "Roaming"))
LOCALAPPDATA = os.environ.get("LOCALAPPDATA") or (str(HOME / ".local" / "share") if sys.platform != "win32" else str(HOME / "AppData" / "Local"))
PROGRAMDATA = os.environ.get("PROGRAMDATA") or ("/etc" if sys.platform != "win32" else "C:\\ProgramData")

def _get_shell_profile_path():
    if sys.platform == "win32":
        p1 = Path(USERPROFILE) / "Documents" / "WindowsPowerShell"
        if p1.exists():
            return str(p1)
        return str(Path(USERPROFILE) / "Documents" / "PowerShell")
    else:
        p_pwsh = Path(APPDATA) / "powershell"
        if p_pwsh.exists():
            return str(p_pwsh)
        p_bash = Path(USERPROFILE) / ".bashrc"
        if p_bash.exists():
            return str(p_bash)
        return str(Path(USERPROFILE) / ".zshrc")

def _get_terminal_path():
    if sys.platform == "win32":
        return str(Path(LOCALAPPDATA) / "Packages" / "Microsoft.WindowsTerminal_8wekyb3d8bbwe" / "LocalState")
    else:
        p1 = Path(APPDATA) / "ptyxis"
        if p1.exists():
            return str(p1)
        return str(Path(USERPROFILE) / ".bashrc")

def _get_obsidian_path():
    p1 = Path(USERPROFILE) / "Documents" / "Obsidian Vault"
    if p1.exists():
        return str(p1)
    p2 = Path(HOME) / "Obsidian"
    if p2.exists():
        return str(p2)
    return str(p1)

# Categorias Globais de Módulos
CATEGORIES = [
    {"id": "all", "label": "Todos", "tag": "TODOS"},
    {"id": "ai_agents", "label": "Agentes IA", "tag": "IA"},
    {"id": "it_sysadmin", "label": "TI & Infra", "tag": "TI"},
    {"id": "dev_workstation", "label": "Dev & Terminal", "tag": "DEV"},
    {"id": "knowledge_base", "label": "Conhecimento", "tag": "NOTAS"}
]

# Catálogo Abrangente de Presets para Agentes, Técnicos de TI e Desenvolvedores
PRESETS_CATALOG = [
    # ------------------ 1. AGENTES DE IA & COGNIÇÃO ------------------
    {
        "id": "antigravity_gemini",
        "title": "Antigravity • Cérebro, Brain & Skills (.gemini)",
        "desc": "Histórico profundo de sessões, brain/, transcrições, skills ativas e MCP connectors.",
        "category_id": "ai_agents",
        "category_label": "Agentes de IA",
        "default_path": str(Path(USERPROFILE) / ".gemini"),
        "archive_folder": "antigravity_gemini",
        "processes": ["antigravity.exe"]
    },
    {
        "id": "antigravity_user",
        "title": "Antigravity • Estado de IDE & Preferências (AppData)",
        "desc": "Tabelas de estado state.vscdb, snippets, storage.json e preferências de layout.",
        "category_id": "ai_agents",
        "category_label": "Agentes de IA",
        "default_path": str(Path(APPDATA) / "antigravity" / "User"),
        "archive_folder": "antigravity_user",
        "processes": ["antigravity.exe"]
    },
    {
        "id": "claude_code",
        "title": "Claude Code • Histórico CLI & MCP Servers (.claude)",
        "desc": "Sessões profundas de terminal, credenciais locais, comandos aprendidos e servidores MCP.",
        "category_id": "ai_agents",
        "category_label": "Agentes de IA",
        "default_path": str(Path(USERPROFILE) / ".claude"),
        "archive_folder": "claude_code",
        "processes": ["claude.exe", "node.exe"]
    },
    {
        "id": "cursor_config",
        "title": "Cursor AI • Regras Globais & Telemetria (.cursor)",
        "desc": "Regras de projeto globais, context memory e configurações gerais do Cursor.",
        "category_id": "ai_agents",
        "category_label": "Agentes de IA",
        "default_path": str(Path(USERPROFILE) / ".cursor"),
        "archive_folder": "cursor_config",
        "processes": ["Cursor.exe"]
    },
    {
        "id": "cursor_storage",
        "title": "Cursor AI • Workspaces, Prompts & state.vscdb",
        "desc": "Banco SQLite do composer, histórico de prompts gerados e extensões ativas.",
        "category_id": "ai_agents",
        "category_label": "Agentes de IA",
        "default_path": str(Path(APPDATA) / "Cursor" / "User"),
        "archive_folder": "cursor_storage",
        "processes": ["Cursor.exe"]
    },
    {
        "id": "windsurf_codeium",
        "title": "Windsurf • Memória Cascades & Contexto (.codeium)",
        "desc": "Árvores de contexto profundo do assistente Cascade e perfis de raciocínio.",
        "category_id": "ai_agents",
        "category_label": "Agentes de IA",
        "default_path": str(Path(USERPROFILE) / ".codeium"),
        "archive_folder": "windsurf_codeium",
        "processes": ["Windsurf.exe"]
    },
    {
        "id": "windsurf_user",
        "title": "Windsurf • Estado de Workspaces (AppData)",
        "desc": "Preferências do editor Windsurf, state.vscdb e extensões instaladas.",
        "category_id": "ai_agents",
        "category_label": "Agentes de IA",
        "default_path": str(Path(APPDATA) / "Windsurf" / "User"),
        "archive_folder": "windsurf_user",
        "processes": ["Windsurf.exe"]
    },
    {
        "id": "openai_codex",
        "title": "OpenAI / Codex • Tokens & Configurações Locais (.codex)",
        "desc": "Autenticação local, caches de execuções de código e logs de ferramentas OpenAI.",
        "category_id": "ai_agents",
        "category_label": "Agentes de IA",
        "default_path": str(Path(USERPROFILE) / ".codex"),
        "archive_folder": "openai_codex",
        "processes": []
    },

    # ------------------ 2. TÉCNICO DE TI & SYSADMIN ------------------
    {
        "id": "ssh_keys",
        "title": "Chaves de Autenticação • SSH (.ssh)",
        "desc": "Pares de chaves públicas/privadas (id_rsa, id_ed25519), config e known_hosts de servidores.",
        "category_id": "it_sysadmin",
        "category_label": "Técnico de TI",
        "default_path": str(Path(USERPROFILE) / ".ssh"),
        "archive_folder": "ssh_keys",
        "processes": []
    },
    {
        "id": "powershell_profiles",
        "title": "PowerShell • Perfis, Scripts & Módulos",
        "desc": "Scripts de automação de infraestrutura, perfis (profile.ps1) e módulos customizados.",
        "category_id": "it_sysadmin",
        "category_label": "Técnico de TI",
        "default_path": _get_shell_profile_path(),
        "archive_folder": "powershell_profiles",
        "processes": ["powershell.exe", "pwsh.exe"]
    },
    {
        "id": "docker_configs",
        "title": "Docker Desktop • Configurações & Contexts (.docker)",
        "desc": "Configurações de daemon local, contextos remotos, credenciais e arquivos config.json.",
        "category_id": "it_sysadmin",
        "category_label": "Técnico de TI",
        "default_path": str(Path(USERPROFILE) / ".docker"),
        "archive_folder": "docker_configs",
        "processes": ["Docker Desktop.exe"]
    },
    {
        "id": "dbeaver_connections",
        "title": "DBeaver • Conexões de Banco de Dados & Scripts",
        "desc": "Credenciais salvas de bancos (PostgreSQL, MySQL, Oracle), conexões e scripts SQL.",
        "category_id": "it_sysadmin",
        "category_label": "Técnico de TI",
        "default_path": str(Path(APPDATA) / "DBeaverData"),
        "archive_folder": "dbeaver_connections",
        "processes": ["dbeaver.exe"]
    },
    {
        "id": "winscp_sessions",
        "title": "WinSCP / PuTTY • Sessões & Conexões SFTP",
        "desc": "Diretório de preferências, marcadores de servidores e sessões salvas.",
        "category_id": "it_sysadmin",
        "category_label": "Técnico de TI",
        "default_path": str(Path(APPDATA) / "WinSCP"),
        "archive_folder": "winscp_sessions",
        "processes": ["winscp.exe"]
    },
    {
        "id": "postman_collections",
        "title": "Postman • Coleções Locais & Variáveis de API",
        "desc": "Dados offline do Postman, ambientes salvos e coleções locais de requisição.",
        "category_id": "it_sysadmin",
        "category_label": "Técnico de TI",
        "default_path": str(Path(APPDATA) / "Postman"),
        "archive_folder": "postman_collections",
        "processes": ["Postman.exe"]
    },
    {
        "id": "wireguard_vpn",
        "title": "WireGuard • Configurações de Túneis VPN (.conf)",
        "desc": "Perfis de VPN e chaves de acesso para túneis de infraestrutura corporativa.",
        "category_id": "it_sysadmin",
        "category_label": "Técnico de TI",
        "default_path": str(Path(LOCALAPPDATA) / "WireGuard"),
        "archive_folder": "wireguard_vpn",
        "processes": ["wireguard.exe"]
    },

    # ------------------ 3. DEV WORKSTATION & TERMINAIS ------------------
    {
        "id": "vscode_user",
        "title": "VS Code • Configurações, Snippets & Keybindings",
        "desc": "settings.json, atalhos de teclado, snippets e estado completo do workspace.",
        "category_id": "dev_workstation",
        "category_label": "Dev Setup",
        "default_path": str(Path(APPDATA) / "Code" / "User"),
        "archive_folder": "vscode_user",
        "processes": ["Code.exe"]
    },
    {
        "id": "windows_terminal",
        "title": "Windows Terminal • Perfis, Cores & Schemas",
        "desc": "settings.json do Terminal do Windows com perfis SSH, WSL e comandos rápidos.",
        "category_id": "dev_workstation",
        "category_label": "Dev Setup",
        "default_path": _get_terminal_path(),
        "archive_folder": "windows_terminal",
        "processes": ["WindowsTerminal.exe"]
    },
    {
        "id": "git_global_config",
        "title": "Git Global • Aliases, Identidades & Configs",
        "desc": "Arquivo .gitconfig do usuário com credenciais, aliases de comando e regras globais.",
        "category_id": "dev_workstation",
        "category_label": "Dev Setup",
        "default_path": str(Path(USERPROFILE) / ".gitconfig"),
        "archive_folder": "git_global_config",
        "processes": []
    },

    # ------------------ 4. BASES DE CONHECIMENTO ------------------
    {
        "id": "obsidian_vault",
        "title": "Obsidian • Cofre de Conhecimento (Markdown & Links)",
        "desc": "Notas permanentes em Markdown, links bidirecionais, templates e plugins .obsidian.",
        "category_id": "knowledge_base",
        "category_label": "Conhecimento",
        "default_path": _get_obsidian_path(),
        "archive_folder": "obsidian_vault",
        "processes": ["Obsidian.exe"]
    },
    {
        "id": "logseq_graphs",
        "title": "Logseq • Grafos & Diários Locais",
        "desc": "Bases de conhecimento estruturadas outliner em Markdown/Org-mode locais.",
        "category_id": "knowledge_base",
        "category_label": "Conhecimento",
        "default_path": str(Path(USERPROFILE) / "Documents" / "Logseq"),
        "archive_folder": "logseq_graphs",
        "processes": ["Logseq.exe"]
    }
]

# Perfis Rápidos (Presets em Lote com 1 Clique)
PROFILES = [
    {
        "id": "profile_ai_nomad",
        "title": "Perfil Agentes de IA",
        "desc": "Antigravity + Claude Code + Cursor + Windsurf + Obsidian",
        "ids": ["antigravity_gemini", "antigravity_user", "claude_code", "cursor_config", "cursor_storage", "obsidian_vault"]
    },
    {
        "id": "profile_it_sysadmin",
        "title": "Perfil TI & Infraestrutura",
        "desc": "Chaves SSH + PowerShell + Docker + DBeaver + WinSCP + Postman",
        "ids": ["ssh_keys", "powershell_profiles", "docker_configs", "dbeaver_connections", "winscp_sessions", "postman_collections"]
    },
    {
        "id": "profile_full_workstation",
        "title": "Perfil Estação Completa",
        "desc": "Todos os Agentes + VS Code + Chaves SSH + Git + Terminal + Obsidian",
        "ids": ["antigravity_gemini", "antigravity_user", "claude_code", "cursor_config", "vscode_user", "ssh_keys", "git_global_config", "windows_terminal", "obsidian_vault"]
    },
    {
        "id": "profile_minimal",
        "title": "Perfil Essencial",
        "desc": "Antigravity (.gemini) + Chaves SSH + Obsidian Vault",
        "ids": ["antigravity_gemini", "ssh_keys", "obsidian_vault"]
    }
]

def get_catalog():
    """Retorna o catálogo de presets com verificação se o caminho existe no sistema atual."""
    catalog = []
    for p in PRESETS_CATALOG:
        item = dict(p)
        item["detected"] = Path(p["default_path"]).exists()
        catalog.append(item)
    return catalog

def get_preset_by_id(preset_id):
    """Busca um preset específico pelo ID."""
    for p in PRESETS_CATALOG:
        if p["id"] == preset_id:
            item = dict(p)
            item["detected"] = Path(p["default_path"]).exists()
            return item
    return None
