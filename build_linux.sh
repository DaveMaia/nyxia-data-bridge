#!/usr/bin/env bash
# ============================================================
# DATA BRIDGE - SCRIPT DE INSTALAÇÃO E EXECUÇÃO NO UBUNTU
# ============================================================
set -e

echo "=== Data Bridge: Verificando ambiente Linux Ubuntu ==="

# 1. Dependências do sistema (Python, Tkinter)
if command -v apt-get &> /dev/null; then
    echo "[1/3] Instalando python3-tk e dependências do sistema..."
    sudo apt-get update -qq
    sudo apt-get install -y python3 python3-tk python3-pip python3-venv liblzma-dev
fi

# 2. Instalação de dependências Python
echo "[2/3] Instalando bibliotecas Python do Data Bridge..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# 3. Permissões de execução nos scripts
chmod +x app.py cli.py mcp_server.py

echo "=== Instalação Concluída com Sucesso! ==="
echo ""
echo "Como usar no Linux Ubuntu:"
echo "  1. Abrir Interface Gráfica:"
echo "     python3 app.py"
echo ""
echo "  2. Usar via Linha de Comando (CLI para humanos ou scripts):"
echo "     python3 cli.py list --json"
echo "     python3 cli.py export --profile profile_ai_nomad -o backup.agpkg"
echo "     python3 cli.py inspect backup.agpkg --json"
echo "     python3 cli.py restore backup.agpkg"
echo ""
echo "  3. Usar com Agentes de IA via MCP (Model Context Protocol):"
echo "     python3 mcp_server.py"
echo "============================================================"
