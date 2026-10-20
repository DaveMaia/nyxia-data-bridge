# ✦ Nyxia Data Bridge

> **Custódia e Transporte de Dados** • Antigravity, Claude Code, Cursor, Windsurf, Ambientes de TI e Estações de Trabalho.

Ferramenta soberana e independente de nuvem para empacotar, transportar e restabelecer memórias cognitivas de assistentes de IA, credenciais e configurações de infraestrutura entre computadores físicos (Desktop ↔ Notebook).

---

## 💡 A Origem: Por que esta ferramenta existe?

Hoje aconteceu uma daquelas situações que todo desenvolvedor moderno conhece bem: precisei sair da bancada de trabalho e levar o trabalho para a rua no notebook.

No meu computador desktop, meu ambiente de IA (**Antigravity**) é praticamente uma extensão do meu cérebro: dezenas de **skills customizadas**, dezenas de servidores **MCP** configurados milimetricamente, bancos relacionais de memória, atalhos de terminal e fluxos que foram lapidados ao longo de semanas de trabalho intenso. No desktop, o agente resolve problemas complexos quase por telepatia.

Quando liguei o notebook fora de casa e abri o editor... **o vazio absoluto**.

Nenhuma skill instalada. Nenhum MCP conectado. Sem histórico, sem variáveis de ambiente, sem memórias contextuais. O assistente que no desktop agia como um arquiteto de software sênior havia se transformado instantaneamente em um estagiário com amnésia profunda. Eu estava no meio de uma demanda urgente, completamente na mão, encarando a perspectiva de gastar horas caçando pastas ocultas no sistema operacional (`~/.gemini`, `~/.claude`, AppData, arquivos `.vscdb` corrompidos) e reconfigurando arquivos JSON na base da tentativa e erro.

Foi ali que a ficha caiu: **por que a nossa infraestrutura de IA não viaja com a gente no bolso, sob nossa custódia física?**

Se você já sincroniza código pelo Git e anotações por markdown, por que o "estado mental", as skills e a calibragem dos seus agentes de IA continuam acorrentados a uma única máquina?

Ao invés de gastar a tarde remendando pastas na mão, resolvi canalizar a frustração e criar o **Nyxia Data Bridge**: uma ponte soberana, offline e de alta velocidade que empacota o ecossistema cognitivo inteiro em um arquivo único compactado (LZMA2 Ultra), pronto para ser plugado em qualquer notebook — seja Windows ou Ubuntu — e restabelecido em menos de 10 segundos.

---

### 🎒 O que veio depois: O conceito de "Dados Viajantes" (ou Dados Aventureiros)

Assim que o protótipo funcionou para o Antigravity, veio o segundo estalo, ainda maior:  
*“Espera aí... por que parar nas IAs? Isso aqui pode carregar qualquer pedaço do meu mundo digital de um canto a outro.”*

Pensei neles como **Dados Viajantes** — ou **Dados Aventureiros**. 

Seus dados não foram feitos para viver aprisionados no disco rígido de uma máquina fixa na bancada, e muito menos como reféns de nuvens proprietárias que exigem login constante, cobram assinaturas perpétuas e passam um aspirador de telemetria em cada arquivo seu. 

O desenvolvedor moderno não carrega só código no Git: carrega chaves SSH que abrem servidores pelo mundo, dezenas de conexões complexas no DBeaver, cofres de ideias no Obsidian, sessões do Docker, automações no terminal e prompts de comando. Esses dados têm que ter a liberdade de viajar com você — seja num pen drive espetado no chaveiro, num SSD portátil ou num snapshot seguro. Eles saem do Windows, aterrissam no Ubuntu, viajam entre computadores diferentes e continuam sendo **seus**, com integridade matemática e custódia física imediata.

Então fui com tudo nessa direção: expandi a ferramenta para suportar qualquer caminho arbitrário (`+ Adicionar Caminho`), módulos dinâmicos para ferramentas de TI e controle total para o operador.

---

### 🌐 Construindo uma Infraestrutura Livre da Nuvem (Participe!)

O **Nyxia Data Bridge** é um manifesto em forma de código por uma computação **Local-First, Soberana e Descentralizada**. A nuvem tem seu valor, mas sua estação de trabalho, suas memórias de inteligência artificial e suas ferramentas essenciais não deveriam depender de conexão com internet ou da boa vontade de servidores corporativos para funcionar.

Se você também acredita que o poder computacional deve pertencer a quem o opera:
- **Adicione novos módulos**: Tem ferramentas de IA, terminais, IDEs ou bancos que você usa no seu dia a dia? Submeta um PR com novos presets em `presets.py`.
- **Aprimore a compatibilidade**: Ajude a lapidar o comportamento no Linux, WSL, FreeBSD e macOS.
- **Traga novas ideias**: Criptografia de ponta, integrações com novos agentes e empacotadores portáteis.

Faça um fork, teste, use no seu dia a dia e **ajude a construir uma infraestrutura verdadeiramente livre da nuvem.**

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
