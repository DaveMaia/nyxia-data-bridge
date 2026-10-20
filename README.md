# ✦ Nyxia Data Bridge

> **Custódia e Transporte de Dados** • Antigravity, Claude Code, Cursor, Windsurf, Ambientes de TI e Estações de Trabalho.

Ferramenta soberana e independente de nuvem para empacotar, transportar e restabelecer memórias cognitivas de assistentes de IA, credenciais e configurações de infraestrutura entre computadores físicos (Desktop ↔ Notebook).

---

## 🚀 1. Executável Standalone (.EXE) no Windows

O executável standalone do **Nyxia Data Bridge** já está compilado e pronto para uso direto (sem necessidade de instalar Python):

- **Caminho do Executável**: `dist/NyxiaDataBridge.exe`
- **Ícone Integrado**: Ícone oficial do aplicativo embutido no `.exe`.
- **Modo Híbrido**: 
  - Se você der **dois cliques no arquivo** pelo Windows Explorer: abre a **Interface Gráfica Completa** (Nyxia Crystal Fluent).
  - Se você invocar pelo **Terminal (PowerShell / CMD)** com argumentos: opera como ferramenta **CLI / MCP** rápida para automações.

### Como Recompilar o .exe a qualquer momento:
Basta executar o script:
```cmd
build.bat
```

---

## 🐧 2. Como Usar no Linux Ubuntu

O Nyxia Data Bridge é 100% multiplataforma e possui suporte nativo ao Linux Ubuntu:

### Instalação no Ubuntu:
```bash
# 1. Dar permissão de execução
chmod +x build_linux.sh

# 2. Executar script de configuração automática (instala python3-tk e dependências)
./build_linux.sh
```

### Executar a Interface Gráfica no Linux:
```bash
python3 app.py
```

### Caminhos Nativos no Linux Reconhecidos Automaticamente:
- **Antigravity**: `~/.gemini` e `~/.config/antigravity/User`
- **Claude Code**: `~/.claude`
- **Cursor AI**: `~/.cursor` e `~/.config/Cursor/User`
- **Windsurf**: `~/.codeium` e `~/.config/Windsurf/User`
- **Chaves SSH**: `~/.ssh`
- **Git Global**: `~/.gitconfig`
- **Docker**: `~/.docker`
- **DBeaver**: `~/.local/share/DBeaverData` ou `~/.config/DBeaverData`
- **Terminal & Shell**: `~/.bashrc`, `~/.zshrc` e perfis de shell
- **Obsidian & Logseq**: `~/Documents/Obsidian Vault` e `~/Documents/Logseq`

---

## 🤖 3. Como Agentes de IA Podem Usar o Nyxia Data Bridge

Agentes de IA (como **Antigravity**, **Claude Code**, **Cursor**, ou scripts autônomos) podem interagir com a ferramenta de 3 formas:

### A) Via Linha de Comando Estruturada (CLI com `--json`)
O binário `.exe` ou script Python responde instantaneamente em JSON para consumo de agentes:

```bash
# Listar todos os módulos e perfis disponíveis:
NyxiaDataBridge.exe list --json
# ou no Linux:
python3 cli.py list --json

# Exportar perfil de Agentes de IA em 1 comando:
NyxiaDataBridge.exe export --profile profile_ai_nomad -o backup_ia.agpkg --json

# Exportar módulos específicos:
NyxiaDataBridge.exe export --modules antigravity_gemini,claude_code -o snapshot.agpkg --json

# Inspecionar pacote sem descompactar:
NyxiaDataBridge.exe inspect backup_ia.agpkg --json

# Restaurar pacote de dados:
NyxiaDataBridge.exe restore backup_ia.agpkg --json
```

### B) Via Servidor MCP (Model Context Protocol) Nativo
O Nyxia Data Bridge possui um servidor MCP embutido sobre `stdio` (JSON-RPC 2.0).

#### Ferramentas MCP Disponíveis para os Agentes:
1. `nyxia_list_modules`: Lista módulos reconhecidos no computador e se estão presentes no disco.
2. `nyxia_export_package`: Cria o pacote `.agpkg` com compressão LZMA2 e isolamento de processos.
3. `nyxia_inspect_package`: Lê o manifesto interno e lista o conteúdo.
4. `nyxia_restore_package`: Restaura os dados nos caminhos de destino.

#### Como Configurar no Claude Code / Cursor / Antigravity (`mcpServers`):
```json
{
  "mcpServers": {
    "nyxia-bridge": {
      "command": "C:\\Users\\David\\.gemini\\antigravity\\scratch\\nyxia-core-bridge\\dist\\NyxiaDataBridge.exe",
      "args": ["mcp"]
    }
  }
}
```
*(No Linux, substitua o `command` por `python3` e `args` por `["/caminho/para/nyxia-core-bridge/mcp_server.py"]`)*

### C) Via SDK Python (`nyxia_bridge.py`)
Qualquer script em Python executado por um agente pode importar a biblioteca diretamente:

```python
import nyxia_bridge

# 1. Listar módulos detectados
mods = nyxia_bridge.list_modules(only_detected=True)

# 2. Exportar pacote
resultado = nyxia_bridge.export_package(
    profile="profile_ai_nomad",
    output_path="meu_cerebro.agpkg",
    compression_mode="lzma"
)

# 3. Inspecionar pacote
manifesto = nyxia_bridge.inspect_package("meu_cerebro.agpkg")

# 4. Restaurar
nyxia_bridge.restore_package("meu_cerebro.agpkg")
```

---

## 🔒 Garantias de Segurança & Custódia Física
- **Zero Telemetria**: Nenhum dado ou byte trafega pela internet.
- **Proteção SQLite**: Quiesce seguro de instâncias ativas de editores antes da leitura para preservar tabelas relacionais (`state.vscdb`).
- **Expurgo Inteligente de Ruído**: Exclusão cirúrgica de caches efêmeros de Chromium (`GPUCache`, `DawnCache`, `Crashpad`, `.lock`).
