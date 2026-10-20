import os
import sys

# Anexa ao console pai no Windows se invocado via terminal (Permite que o .exe funcione com GUI e CLI/MCP)
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.kernel32.AttachConsole(-1)
    except Exception:
        pass
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

import customtkinter as ctk
from PIL import Image
from glass_effect import apply_acrylic_glass
import engine
import presets

def get_resource_path(relative_path: str) -> Path:
    """Obtém o caminho do recurso, funcionando tanto em desenvolvimento quanto compilado com PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).parent / relative_path

# Configuração global de aparência: TEMA CLARO TRANSLÚCIDO
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Design System Oficial: Nyxia Crystal Fluent (DESIGN.md)
SURFACE_BASE = "#faf8ff"
SURFACE_CARD = "#ffffff"
SURFACE_INNER = "#f8fafc"
SURFACE_CONTAINER_LOW = "#f2f3ff"
SURFACE_CONTAINER_HIGH = "#e2e7ff"
BORDER_OUTLINE = "#cbd5e1"
BORDER_LIGHT = "#e2e8f0"
INPUT_WELL = "#f8fafc"

COLOR_PRIMARY = "#004ac6"          # Deep Cobalt Primary
COLOR_PRIMARY_HOVER = "#003ea8"
COLOR_PRIMARY_CONTAINER = "#2563eb"
COLOR_SECONDARY = "#4648d4"        # Indigo / Tech
COLOR_TERTIARY = "#c2410c"         # Terracotta / Hardware Accent
COLOR_TERTIARY_BG = "#fff7ed"

TEXT_ON_SURFACE = "#131b2e"        # Deep Slate (95% Contraste)
TEXT_MUTED = "#64748b"             # Medium Slate
TEXT_VARIANT = "#434655"

STATUS_SAFE = "#059669"            # Emerald Green
STATUS_SAFE_BG = "#ecfdf5"
STATUS_WARN = "#d97706"            # Amber
STATUS_WARN_BG = "#fef3c7"
STATUS_ERROR = "#dc2626"           # Crimson
STATUS_ERROR_BG = "#fee2e2"

USERPROFILE = os.environ.get("USERPROFILE", "")
APPDATA = os.environ.get("APPDATA", "")

NOMAD_SLIDES = [
    {
        "index": "01",
        "tag": "ARQUITETURA SOBERANA",
        "title": "Universal Data Mover & Soberania Cognitiva",
        "subtitle": "A ponte universal para transportar agentes de IA, ambientes de TI e estações de trabalho.",
        "thesis": "Modelos de linguagem e ambientes operacionais vivem no seu disco local. O Data Bridge liberta seu ecossistema sem depender da nuvem.",
        "cards": [
            ("Manifesto Nomad & Soberania Digital", "Independência de telemetria e proteção de memórias de IA sob custódia física e local absoluta."),
            ("Custódia Soberana Ponto a Ponto", "Seus prompts, caches de IDE, scripts de PowerShell e chaves SSH trafegam fisicamente sob seu controle absoluto."),
            ("Catálogo Universal de Presets", "Selecione em 1 clique perfis prontos para Agentes de IA (Antigravity, Claude, Cursor), Técnicos de TI ou Dev Full-Stack."),
            ("Compressão & Preservação Atômica", "Motor LZMA2 com redução de até 85% e fechamento seguro para proteger bancos relacionais SQLite (state.vscdb).")
        ],
        "step": "01 / 04 • ARQUITETURA SOBERANA"
    },
    {
        "index": "02",
        "tag": "REDUÇÃO LÉXICA",
        "title": "Super Compressão LZMA2 Ultra",
        "subtitle": "Arquivos levam séculos, nuvens fecham amanhã: redução radical em Markdown e SQLite.",
        "thesis": "Bancos de dados relacionais locais e notas atômicas em Markdown puro possuem um índice astronômico de redundância léxica estruturada.",
        "cards": [
            ("Alta Eficiência & Redução Léxica", "Redução radical de tamanho através de dicionário estendido de até 64MB sem perda de valor semântico."),
            ("Compressão de Alta Densidade (85%)", "O motor LZMA2 aplica dicionário expandido, transformando gigabytes de histórico em poucos megabytes leves."),
            ("Expurgo Ativo de Ruído", "Exclui com precisão cirúrgica caches efêmeros de Chromium (GPUCache, DawnCache, Code Cache e logs temporários inúteis)."),
            ("Contêiner Autodescritivo (.agpkg)", "Empacotado em contêiner com manifest.json estruturado, auditável e legível por qualquer utilitário universal de arquivos.")
        ],
        "step": "02 / 04 • REDUÇÃO LÉXICA"
    },
    {
        "index": "03",
        "tag": "ATOMICIDADE",
        "title": "Consistência Atômica no Ponto de Origem",
        "subtitle": "Preservação estrita de ponteiros e integridade relacional sem corromper o estado em repouso.",
        "thesis": "Ferramentas como Antigravity, Obsidian e Cursor mantêm ponteiros ativos de gravação em bancos SQLite (state.vscdb) e LevelDB em tempo real.",
        "cards": [
            ("Disciplina Transacional & Zero Locks", "Garantia de que nenhum arquivo em gravação ativa seja copiado pela metade, prevenindo corrupção de ponteiros."),
            ("Proteção Anti-Fissura SQLite", "Copiar arquivos com processos abertos corrompe índices de busca e tabelas relacionais. O Bridge garante consistência no repouso."),
            ("Cessação Cirúrgica de Concorrência", "Verificação assistida de instâncias ativas (antigravity.exe, Cursor.exe, obsidian.exe) antes de qualquer leitura ou gravação."),
            ("Absorção Atômica no Destino", "Ao aportar no notebook receptor, os dados são descarregados exatamente nos nós correspondentes sem falhas de I/O.")
        ],
        "step": "03 / 04 • ATOMICIDADE"
    },
    {
        "index": "04",
        "tag": "TRANSPORTE MODULAR",
        "title": "Catálogo Modular para Técnicos & Engenheiros",
        "subtitle": "Além de assistentes de IA, transporte todo o seu setup de desenvolvimento com facilidade.",
        "thesis": "O mesmo motor que preserva a inteligência dos seus agentes é capaz de empacotar qualquer nó de trabalho da sua máquina.",
        "cards": [
            ("Portabilidade Universal & Workstation Mover", "Capacidade nativa de empacotar memórias de IA, chaves SSH, bancos e nós arbitrários da máquina."),
            ("Anexação Arbitrária ('+')", "Adicione repositórios de projetos, ambientes virtuais, pastas de documentos e configurações de infraestrutura sem restrições."),
            ("Chaves & Credenciais (.ssh)", "Transporte com segurança seus pares de chaves SSH (id_rsa, id_ed25519) e known_hosts para autenticação imediata no destino."),
            ("Presets de Todos os Agentes", "Detecção instantânea para Antigravity, Claude Code, Cursor, Codex, Windsurf, VS Code, DBeaver, Docker e Obsidian Vaults.")
        ],
        "step": "04 / 04 • TRANSPORTE MODULAR"
    }
]

class OnboardingScreen(ctk.CTkFrame):
    """Tela 1: Apresentação Nomad com Padrão Editorial Open Design & Claude Code."""
    def __init__(self, parent, on_finish_callback):
        super().__init__(parent, fg_color="transparent")
        self.on_finish_callback = on_finish_callback
        self.current_idx = 0

        self.card = ctk.CTkFrame(self, fg_color=SURFACE_CARD, corner_radius=18, border_width=1, border_color=BORDER_OUTLINE)
        self.card.pack(fill="both", expand=True, padx=28, pady=(16, 14))

        # Top Bar Editorial
        top_bar = ctk.CTkFrame(self.card, fg_color="transparent")
        top_bar.pack(fill="x", padx=28, pady=(20, 10))

        lbl_brand = ctk.CTkLabel(
            top_bar,
            text="DATA BRIDGE  •  MANIFESTO NOMAD",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=TEXT_MUTED
        )
        lbl_brand.pack(side="left")

        self.lbl_step = ctk.CTkLabel(
            top_bar,
            text="",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=COLOR_PRIMARY
        )
        self.lbl_step.pack(side="right")

        # Corpo do Slide
        body = ctk.CTkFrame(self.card, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=28, pady=8)

        header_row = ctk.CTkFrame(body, fg_color="transparent")
        header_row.pack(fill="x", pady=(0, 8))

        # Badge Monospaçado de Capítulo (Padrão Claude Code / Open Design - Sem Emojis)
        self.index_badge = ctk.CTkFrame(
            header_row,
            fg_color="#eff6ff",
            corner_radius=12,
            border_width=1,
            border_color="#bfdbfe",
            width=54,
            height=54
        )
        self.index_badge.pack_propagate(False)
        self.index_badge.pack(side="left", padx=(0, 16), anchor="n")

        self.lbl_index = ctk.CTkLabel(
            self.index_badge,
            text="01",
            font=ctk.CTkFont(family="Consolas", size=22, weight="bold"),
            text_color=COLOR_PRIMARY
        )
        self.lbl_index.pack(expand=True)

        title_col = ctk.CTkFrame(header_row, fg_color="transparent")
        title_col.pack(side="left", fill="x", expand=True)

        self.lbl_title = ctk.CTkLabel(
            title_col,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=TEXT_ON_SURFACE,
            anchor="w"
        )
        self.lbl_title.pack(fill="x")

        self.lbl_subtitle = ctk.CTkLabel(
            title_col,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=TEXT_VARIANT,
            anchor="w"
        )
        self.lbl_subtitle.pack(fill="x", pady=(3, 0))

        # Standfirst / Tese Editorial
        thesis_frame = ctk.CTkFrame(body, fg_color=SURFACE_CONTAINER_LOW, corner_radius=12, border_width=1, border_color="#e0e7ff")
        thesis_frame.pack(fill="x", pady=(8, 12))

        self.lbl_thesis = ctk.CTkLabel(
            thesis_frame,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12, slant="italic"),
            text_color="#1e293b",
            wraplength=760,
            justify="left",
            anchor="w"
        )
        self.lbl_thesis.pack(fill="x", padx=18, pady=10)

        self.cards_container = ctk.CTkFrame(body, fg_color="transparent")
        self.cards_container.pack(fill="both", expand=True)

        bottom_bar = ctk.CTkFrame(self.card, fg_color="transparent")
        bottom_bar.pack(fill="x", padx=28, pady=(12, 20), side="bottom")

        self.btn_skip = ctk.CTkButton(
            bottom_bar,
            text="Pular Apresentação ➔",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color="transparent",
            hover_color="#e2e8f0",
            text_color=TEXT_MUTED,
            width=180,
            height=36,
            command=self.on_finish_callback
        )
        self.btn_skip.pack(side="left")

        self.dots_frame = ctk.CTkFrame(bottom_bar, fg_color="transparent")
        self.dots_frame.pack(side="left", expand=True)

        self.dot_labels = []
        for d in range(len(NOMAD_SLIDES)):
            dot = ctk.CTkLabel(
                self.dots_frame,
                text="●" if d == 0 else "○",
                font=ctk.CTkFont(size=16),
                text_color=COLOR_PRIMARY if d == 0 else "#94a3b8"
            )
            dot.pack(side="left", padx=5)
            self.dot_labels.append(dot)

        nav_frame = ctk.CTkFrame(bottom_bar, fg_color="transparent")
        nav_frame.pack(side="right")

        self.btn_prev = ctk.CTkButton(
            nav_frame,
            text="‹ Voltar",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color="#e2e8f0",
            hover_color="#cbd5e1",
            text_color=TEXT_ON_SURFACE,
            width=95,
            height=36,
            command=self.prev_slide
        )
        self.btn_prev.pack(side="left", padx=(0, 10))

        self.btn_next = ctk.CTkButton(
            nav_frame,
            text="Avançar ›",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            width=135,
            height=36,
            command=self.next_slide
        )
        self.btn_next.pack(side="left")

        self.update_slide_ui()

    def update_slide_ui(self):
        slide = NOMAD_SLIDES[self.current_idx]
        self.lbl_step.configure(text=slide["step"])
        self.lbl_index.configure(text=slide["index"])
        self.lbl_title.configure(text=slide["title"])
        self.lbl_subtitle.configure(text=slide["subtitle"])
        self.lbl_thesis.configure(text=f'"{slide["thesis"]}"')

        # Renderiza dinamicamente todos os tópicos no padrão editorial Claude Code
        for w in self.cards_container.winfo_children():
            w.destroy()

        for i, (head, desc) in enumerate(slide["cards"]):
            c_frame = ctk.CTkFrame(
                self.cards_container,
                fg_color=INPUT_WELL,
                corner_radius=10,
                border_width=1,
                border_color=BORDER_LIGHT
            )
            c_frame.pack(fill="x", pady=3)

            top_row = ctk.CTkFrame(c_frame, fg_color="transparent")
            top_row.pack(fill="x", padx=16, pady=(7, 2))

            lbl_num = ctk.CTkLabel(
                top_row,
                text=f"{slide['index']}.{i+1}",
                font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
                text_color=COLOR_PRIMARY,
                width=34,
                anchor="w"
            )
            lbl_num.pack(side="left")

            lbl_t = ctk.CTkLabel(
                top_row,
                text=head,
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                text_color=TEXT_ON_SURFACE,
                anchor="w"
            )
            lbl_t.pack(side="left", fill="x", expand=True)

            lbl_d = ctk.CTkLabel(
                c_frame,
                text=desc,
                font=ctk.CTkFont(family="Segoe UI", size=11),
                text_color=TEXT_MUTED,
                anchor="w",
                justify="left",
                wraplength=760
            )
            lbl_d.pack(fill="x", padx=16, pady=(0, 7))

        for i, dot in enumerate(self.dot_labels):
            if i == self.current_idx:
                dot.configure(text="●", text_color=COLOR_PRIMARY)
            else:
                dot.configure(text="○", text_color="#94a3b8")

        if self.current_idx == 0:
            self.btn_prev.configure(state="disabled", fg_color="#f1f5f9", text_color="#cbd5e1")
        else:
            self.btn_prev.configure(state="normal", fg_color="#e2e8f0", text_color=TEXT_ON_SURFACE)

        if self.current_idx == len(NOMAD_SLIDES) - 1:
            self.btn_next.configure(text="INICIAR DATA BRIDGE ➔", fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, width=205)
        else:
            self.btn_next.configure(text="Avançar ›", fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, width=135)

    def next_slide(self):
        if self.current_idx < len(NOMAD_SLIDES) - 1:
            self.current_idx += 1
            self.update_slide_ui()
        else:
            self.on_finish_callback()

    def prev_slide(self):
        if self.current_idx > 0:
            self.current_idx -= 1
            self.update_slide_ui()

class DataBoxWidget:
    """Caixa de Anexação de Dados do Design System Nyxia Crystal Fluent com Verificador de Caminho."""
    def __init__(self, parent, box_id, title, desc, default_path, archive_folder, on_remove_callback, is_custom=False, initial_check=True, category_tag=None):
        self.parent = parent
        self.box_id = box_id
        self.archive_folder = archive_folder
        self.on_remove_callback = on_remove_callback
        self.is_custom = is_custom

        if category_tag:
            self.category_tag = category_tag
        elif is_custom:
            self.category_tag = "CUSTOM"
        else:
            cat_tag_map = {
                "ai_agents": "IA",
                "it_sysadmin": "TI",
                "dev_workstation": "DEV",
                "knowledge_base": "NOTAS"
            }
            p = presets.get_preset_by_id(box_id)
            if p:
                self.category_tag = cat_tag_map.get(p.get("category_id", ""), "MOD")
            else:
                self.category_tag = "NÓ"

        self.var_check = ctk.BooleanVar(value=initial_check)
        self.var_path = ctk.StringVar(value=default_path)

        # Cartão Fluido: 12px corner radius, 1px borda sutil
        self.frame = ctk.CTkFrame(parent, fg_color=SURFACE_CARD, corner_radius=12, border_width=1, border_color=BORDER_OUTLINE)
        self.frame.pack(fill="x", pady=4, padx=2)

        # 1. Linha Superior: Checkbox, Badge de Categoria, Destino no Pacote, Botão Remover
        top_row = ctk.CTkFrame(self.frame, fg_color="transparent")
        top_row.pack(fill="x", padx=14, pady=(10, 2))

        self.chk = ctk.CTkCheckBox(
            top_row,
            text=title,
            variable=self.var_check,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=TEXT_ON_SURFACE,
            fg_color=COLOR_PRIMARY,
            height=22
        )
        self.chk.pack(side="left")

        # Pílula de Categoria (tag)
        self.badge_cat = ctk.CTkLabel(
            top_row,
            text=f"[{self.category_tag}]",
            font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
            fg_color="#f1f5f9",
            text_color="#475569",
            corner_radius=6,
            height=20,
            padx=6
        )
        self.badge_cat.pack(side="left", padx=(8, 6))

        # Indicador de Destino no Pacote
        self.lbl_target = ctk.CTkLabel(
            top_row,
            text=f"Destino: /{self.archive_folder}/",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#0369a1"
        )
        self.lbl_target.pack(side="left", padx=4)

        # Botão Remover (✕ Remover)
        btn_del = ctk.CTkButton(
            top_row,
            text="✕ Remover",
            width=76,
            height=24,
            corner_radius=6,
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            fg_color="#f8fafc",
            hover_color="#fee2e2",
            text_color="#64748b",
            border_width=1,
            border_color=BORDER_LIGHT,
            command=lambda: self.on_remove_callback(self)
        )
        btn_del.pack(side="right")

        # 2. Linha de Descrição
        ctk.CTkLabel(
            self.frame,
            text=desc,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=TEXT_MUTED
        ).pack(anchor="w", padx=14, pady=(0, 4))

        # 3. Linha de Entrada de Caminho & Botão Procurar
        bottom_row = ctk.CTkFrame(self.frame, fg_color="transparent")
        bottom_row.pack(fill="x", padx=14, pady=(0, 4))

        self.entry = ctk.CTkEntry(
            bottom_row,
            textvariable=self.var_path,
            fg_color=INPUT_WELL,
            border_color=BORDER_OUTLINE,
            text_color=TEXT_ON_SURFACE,
            height=34,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        btn_browse = ctk.CTkButton(
            bottom_row,
            text="Procurar...",
            width=88,
            height=34,
            corner_radius=8,
            fg_color="#f1f5f9",
            hover_color="#e2e8f0",
            text_color=TEXT_ON_SURFACE,
            border_width=1,
            border_color=BORDER_OUTLINE,
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            command=self.browse_dir
        )
        btn_browse.pack(side="right")

        # 4. Linha de Feedback: VERIFICADOR DE CAMINHO (Verde Esmeralda ou Terracota)
        feedback_row = ctk.CTkFrame(self.frame, fg_color="transparent")
        feedback_row.pack(fill="x", padx=14, pady=(0, 8))

        # O Verificador com pílula colorida
        self.lbl_path_status = ctk.CTkLabel(
            feedback_row,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            corner_radius=10,
            height=22,
            padx=10
        )
        self.lbl_path_status.pack(side="left")

        # Nota de filtros transparentes
        self.lbl_filter_info = ctk.CTkLabel(
            feedback_row,
            text="Filtros: Caches de Chromium, GPUCache, Crashpad e .lock ignorados",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color="#94a3b8",
            anchor="e"
        )
        self.lbl_filter_info.pack(side="right")

        self.update_path_feedback()
        self.var_path.trace_add("write", lambda *args: self.update_path_feedback())

    def update_path_feedback(self):
        p = self.var_path.get().strip()
        if p and os.path.exists(p):
            # Verde Esmeralda (Válido no disco)
            self.lbl_path_status.configure(
                text="● Válido no disco",
                text_color=STATUS_SAFE,
                fg_color=STATUS_SAFE_BG
            )
            self.entry.configure(border_color="#a7f3d0")
        else:
            # Terracota (Inválido / Não localizado)
            self.lbl_path_status.configure(
                text="● Não localizado",
                text_color=COLOR_TERTIARY,
                fg_color=COLOR_TERTIARY_BG
            )
            self.entry.configure(border_color=BORDER_OUTLINE)

    def browse_dir(self):
        chosen = filedialog.askdirectory()
        if chosen:
            norm = os.path.normpath(chosen)
            self.var_path.set(norm)
            self.update_path_feedback()

    def destroy(self):
        self.frame.destroy()


class MainToolScreen(ctk.CTkFrame):
    """Tela 2: Painel Operacional Data Bridge com Catálogo Lateral Recolhível."""
    def __init__(self, parent, app_controller):
        super().__init__(parent, fg_color="transparent")
        self.app = app_controller
        self.active_category = "Todos"
        self.is_sidebar_collapsed = True

        # 1. Header com Logo Oficial, Título, Badge de Custódia e Botão de Manifesto
        header = ctk.CTkFrame(self, fg_color=SURFACE_CARD, corner_radius=12, border_width=1, border_color=BORDER_OUTLINE)
        header.pack(fill="x", padx=16, pady=(12, 6))

        top_header_row = ctk.CTkFrame(header, fg_color="transparent")
        top_header_row.pack(fill="x", padx=16, pady=12)

        # Ícone do App
        icon_path = get_resource_path("header_icon.png")
        if icon_path.exists():
            try:
                pil_icon = Image.open(str(icon_path))
                self.header_icon_img = ctk.CTkImage(light_image=pil_icon, dark_image=pil_icon, size=(30, 30))
                lbl_icon = ctk.CTkLabel(top_header_row, image=self.header_icon_img, text="")
                lbl_icon.pack(side="left", padx=(0, 10))
            except Exception:
                pass

        title_lbl = ctk.CTkLabel(
            top_header_row,
            text="DATA BRIDGE",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=COLOR_PRIMARY
        )
        title_lbl.pack(side="left")

        # Pílula com a Versão Oficial (Design System Nyxia Crystal Fluent)
        version_pill = ctk.CTkLabel(
            top_header_row,
            text="v1.14",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            fg_color="#e1e0ff",
            text_color="#2f2ebe",
            corner_radius=10,
            height=20,
            padx=8
        )
        version_pill.pack(side="left", padx=(8, 0))

        engine_badge = ctk.CTkLabel(
            top_header_row,
            text="Custódia e Transporte de Dados",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color="#eff6ff",
            text_color=COLOR_PRIMARY,
            corner_radius=6,
            height=24,
            padx=10
        )
        engine_badge.pack(side="left", padx=(10, 0))

        btn_revisit_tour = ctk.CTkButton(
            top_header_row,
            text="📖 Manifesto & Arquitetura",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color="#ffffff",
            hover_color="#eff6ff",
            text_color=COLOR_PRIMARY,
            border_width=1,
            border_color="#bfdbfe",
            height=30,
            corner_radius=8,
            command=self.app.show_onboarding
        )
        btn_revisit_tour.pack(side="right")

        # 2. Abas de Operação Segmentadas
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=SURFACE_CARD,
            segmented_button_fg_color="#e2e8f0",
            segmented_button_selected_color=COLOR_PRIMARY,
            segmented_button_selected_hover_color=COLOR_PRIMARY_HOVER,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_OUTLINE
        )
        self.tabview.pack(fill="both", expand=True, padx=16, pady=(0, 6))

        tab_export = self.tabview.add("  01 / Exportar Pacote de Dados (.agpkg)  ")
        tab_import = self.tabview.add("  02 / Restaurar e Aplicar no Computador  ")

        self.setup_export_tab(tab_export)
        self.setup_import_tab(tab_import)

        # 3. Painel Global de Progresso & Status
        progress_card = ctk.CTkFrame(self, fg_color=SURFACE_CARD, corner_radius=12, border_width=1, border_color=BORDER_OUTLINE)
        progress_card.pack(fill="x", padx=16, pady=(0, 6))

        progress_header_row = ctk.CTkFrame(progress_card, fg_color="transparent")
        progress_header_row.pack(fill="x", padx=16, pady=(6, 2))

        self.lbl_progress = ctk.CTkLabel(
            progress_header_row,
            text="Status: Pronto para operar sob custódia local",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=TEXT_ON_SURFACE
        )
        self.lbl_progress.pack(side="left")

        lbl_custody_status = ctk.CTkLabel(
            progress_header_row,
            text="● CUSTÓDIA 100% LOCAL",
            font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
            text_color=STATUS_SAFE
        )
        lbl_custody_status.pack(side="right")

        self.progress_bar = ctk.CTkProgressBar(
            progress_card,
            fg_color="#e2e8f0",
            progress_color=COLOR_PRIMARY,
            height=8,
            corner_radius=4
        )
        self.progress_bar.set(0.0)
        self.progress_bar.pack(fill="x", padx=16, pady=(0, 4))

        self.lbl_details = ctk.CTkLabel(
            progress_card,
            text="Aguardando comando do operador...",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=TEXT_MUTED
        )
        self.lbl_details.pack(anchor="w", padx=16, pady=(0, 6))

    def setup_export_tab(self, parent):
        """Layout de 2 Colunas com Barra Lateral Recolhível."""
        self.two_col_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.two_col_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # ========================================================
        # COLUNA ESQUERDA: CATÁLOGO LATERAL RECOLHÍVEL
        # ========================================================
        self.sidebar = ctk.CTkFrame(self.two_col_frame, fg_color=SURFACE_INNER, corner_radius=12, border_width=1, border_color=BORDER_OUTLINE, width=300)
        self.sidebar.pack_propagate(False)

        # Cabeçalho da Barra Lateral com Botão Sanduíche e Botão de Recolher
        sidebar_top = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        sidebar_top.pack(fill="x", padx=10, pady=(10, 4))

        btn_hamburger_sidebar = ctk.CTkButton(
            sidebar_top,
            text="☰",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            width=30,
            height=26,
            corner_radius=4,
            fg_color="#eff6ff",
            hover_color="#dbeafe",
            text_color=COLOR_PRIMARY,
            command=self.toggle_sidebar
        )
        btn_hamburger_sidebar.pack(side="left", padx=(0, 6))

        lbl_catalog_title = ctk.CTkLabel(
            sidebar_top,
            text="CATÁLOGO DE MÓDULOS",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=COLOR_PRIMARY
        )
        lbl_catalog_title.pack(side="left")

        self.btn_collapse_catalog = ctk.CTkButton(
            sidebar_top,
            text="◀ Recolher",
            width=76,
            height=26,
            corner_radius=4,
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            fg_color="#e2e8f0",
            hover_color="#cbd5e1",
            text_color=TEXT_ON_SURFACE,
            command=self.toggle_sidebar
        )
        self.btn_collapse_catalog.pack(side="right")

        lbl_catalog_sub = ctk.CTkLabel(
            self.sidebar,
            text="Selecione perfis prontos ou adicione módulos individualmente ao pacote de transporte.",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=TEXT_MUTED,
            wraplength=270,
            justify="left"
        )
        lbl_catalog_sub.pack(anchor="w", padx=12, pady=(0, 8))

        # Seção 1: Perfis Rápidos (1-Clique)
        ctk.CTkLabel(
            self.sidebar,
            text="PERFIS PRONTOS (1-CLIQUE)",
            font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
            text_color=TEXT_VARIANT
        ).pack(anchor="w", padx=12, pady=(4, 4))

        profiles_grid = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        profiles_grid.pack(fill="x", padx=8, pady=(0, 6))

        for prof in presets.PROFILES:
            btn_prof = ctk.CTkButton(
                profiles_grid,
                text=prof["title"],
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                fg_color=SURFACE_CARD,
                hover_color="#eff6ff",
                text_color=TEXT_ON_SURFACE,
                border_width=1,
                border_color=BORDER_OUTLINE,
                corner_radius=6,
                height=28,
                anchor="w",
                command=lambda p=prof: self.apply_profile(p)
            )
            btn_prof.pack(fill="x", pady=2)

        # Seção 2: Filtro por Categorias (Segmented Buttons)
        ctk.CTkLabel(
            self.sidebar,
            text="FILTRAR POR CATEGORIA",
            font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
            text_color=TEXT_VARIANT
        ).pack(anchor="w", padx=12, pady=(6, 4))

        self.category_selector = ctk.CTkSegmentedButton(
            self.sidebar,
            values=["Todos", "Agentes IA", "TI & Infra", "Dev & Terminal", "Conhecimento"],
            command=self.on_category_chip_changed,
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            selected_color=COLOR_PRIMARY,
            selected_hover_color=COLOR_PRIMARY_HOVER,
            corner_radius=6,
            height=28
        )
        self.category_selector.set("Todos")
        self.category_selector.pack(fill="x", padx=8, pady=(0, 6))

        # Seção 3: Lista de Presets Individuais do Catálogo (Scrollable)
        self.catalog_scroll = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        self.catalog_scroll.pack(fill="both", expand=True, padx=4, pady=2)

        self.render_catalog_items()

        # ========================================================
        # BARRA VERTICAL RECOLHIDA (MENU SANDUÍCHE NO LADO ESQUERDO)
        # ========================================================
        self.collapsed_catalog_rail = ctk.CTkFrame(
            self.two_col_frame,
            fg_color=SURFACE_INNER,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_OUTLINE,
            width=46
        )
        self.collapsed_catalog_rail.pack_propagate(False)
        self.collapsed_catalog_rail.pack(side="left", fill="y", padx=(0, 6), pady=0)

        self.btn_rail_hamburger = ctk.CTkButton(
            self.collapsed_catalog_rail,
            text="☰",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            width=36,
            height=36,
            corner_radius=6,
            fg_color=SURFACE_CARD,
            hover_color="#eff6ff",
            text_color=COLOR_PRIMARY,
            border_width=1,
            border_color=BORDER_OUTLINE,
            command=self.toggle_sidebar
        )
        self.btn_rail_hamburger.pack(padx=4, pady=8)

        # ========================================================
        # COLUNA DIREITA: ÁREA CENTRAL DE CAMINHOS & EXECUÇÃO
        # ========================================================
        self.main_content = ctk.CTkFrame(self.two_col_frame, fg_color="transparent")
        self.main_content.pack(side="right", fill="both", expand=True, padx=0, pady=0)

        # Barra Superior de Ações: APENAS UM BOTÃO (Adicionar Caminho)
        actions_bar = ctk.CTkFrame(self.main_content, fg_color=SURFACE_INNER, corner_radius=10, border_width=1, border_color=BORDER_OUTLINE)
        actions_bar.pack(fill="x", pady=(0, 6))

        self.lbl_active_count = ctk.CTkLabel(
            actions_bar,
            text="Nenhum caminho adicionado",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=TEXT_ON_SURFACE
        )
        self.lbl_active_count.pack(side="left", padx=14, pady=8)

        # Mantido estritamente SOMENTE UM BOTÃO conforme solicitado pelo operador
        btn_add_custom = ctk.CTkButton(
            actions_bar,
            text="+ Adicionar Caminho",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            corner_radius=8,
            height=32,
            command=self.app.prompt_add_custom_folder
        )
        btn_add_custom.pack(side="right", padx=10, pady=6)

        # Container Rolável para as Caixas de Dados
        self.boxes_scroll = ctk.CTkScrollableFrame(self.main_content, fg_color="transparent")
        self.boxes_scroll.pack(fill="both", expand=True, pady=(0, 6))

        self.boxes_container = ctk.CTkFrame(self.boxes_scroll, fg_color="transparent")
        self.boxes_container.pack(fill="x", pady=2)

        # Estado Vazio Estilizado segundo o Stitch Mockup
        self.empty_state_frame = ctk.CTkFrame(self.boxes_scroll, fg_color=SURFACE_CARD, corner_radius=12, border_width=1, border_color=BORDER_OUTLINE)
        self.empty_state_frame.pack(fill="both", expand=True, padx=8, pady=16)

        # Badge Superior do Mockup
        ctk.CTkLabel(
            self.empty_state_frame,
            text="◈ SOBERANIA LOCAL • WORKSTATION ORIGEM",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            fg_color="#eff6ff",
            text_color=COLOR_PRIMARY,
            corner_radius=6,
            height=22,
            padx=10
        ).pack(anchor="center", pady=(24, 8))

        ctk.CTkLabel(
            self.empty_state_frame,
            text="Nenhum Módulo Selecionado para Transporte",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=TEXT_ON_SURFACE
        ).pack(anchor="center")

        ctk.CTkLabel(
            self.empty_state_frame,
            text="Monte seu pacote de dados escolhendo um perfil pronto abaixo,\nselecionando itens no Catálogo à esquerda (☰) ou adicionando qualquer pasta do disco.",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=TEXT_MUTED,
            justify="center"
        ).pack(anchor="center", pady=(6, 18))

        # 3 Cartões de Ação Rápida
        empty_cards_row = ctk.CTkFrame(self.empty_state_frame, fg_color="transparent")
        empty_cards_row.pack(anchor="center", fill="x", padx=30, pady=(0, 16))

        # Card 1: Agentes de IA
        c1 = ctk.CTkFrame(empty_cards_row, fg_color=SURFACE_INNER, corner_radius=10, border_width=1, border_color=BORDER_LIGHT)
        c1.pack(side="left", fill="both", expand=True, padx=6, pady=4)

        ctk.CTkLabel(c1, text="Agentes de IA", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color=COLOR_PRIMARY).pack(anchor="w", padx=12, pady=(10, 2))
        ctk.CTkLabel(c1, text="Antigravity (.gemini) • Claude Code • Cursor • Windsurf • Obsidian", font=ctk.CTkFont(family="Segoe UI", size=10), text_color=TEXT_MUTED, wraplength=170, justify="left").pack(anchor="w", padx=12, pady=(0, 10))
        btn_c1 = ctk.CTkButton(
            c1,
            text="Carregar Perfil",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color="#eff6ff",
            hover_color="#dbeafe",
            text_color=COLOR_PRIMARY,
            border_width=1,
            border_color="#bfdbfe",
            height=28,
            corner_radius=6,
            command=lambda: self.apply_profile(presets.PROFILES[0])
        )
        btn_c1.pack(fill="x", padx=12, pady=(0, 10))

        # Card 2: TI & Infraestrutura
        c2 = ctk.CTkFrame(empty_cards_row, fg_color=SURFACE_INNER, corner_radius=10, border_width=1, border_color=BORDER_LIGHT)
        c2.pack(side="left", fill="both", expand=True, padx=6, pady=4)

        ctk.CTkLabel(c2, text="TI & Infraestrutura", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color=COLOR_PRIMARY).pack(anchor="w", padx=12, pady=(10, 2))
        ctk.CTkLabel(c2, text="Chaves SSH (.ssh) • PowerShell • Docker • DBeaver • WinSCP", font=ctk.CTkFont(family="Segoe UI", size=10), text_color=TEXT_MUTED, wraplength=170, justify="left").pack(anchor="w", padx=12, pady=(0, 10))
        btn_c2 = ctk.CTkButton(
            c2,
            text="Carregar Perfil",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color="#eff6ff",
            hover_color="#dbeafe",
            text_color=COLOR_PRIMARY,
            border_width=1,
            border_color="#bfdbfe",
            height=28,
            corner_radius=6,
            command=lambda: self.apply_profile(presets.PROFILES[1])
        )
        btn_c2.pack(fill="x", padx=12, pady=(0, 10))

        # Card 3: Pasta Customizada
        c3 = ctk.CTkFrame(empty_cards_row, fg_color=SURFACE_INNER, corner_radius=10, border_width=1, border_color=BORDER_LIGHT)
        c3.pack(side="left", fill="both", expand=True, padx=6, pady=4)

        ctk.CTkLabel(c3, text="Pasta Customizada", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color=COLOR_PRIMARY).pack(anchor="w", padx=12, pady=(10, 2))
        ctk.CTkLabel(c3, text="Adicionar qualquer diretório de projeto, repositório ou banco local", font=ctk.CTkFont(family="Segoe UI", size=10), text_color=TEXT_MUTED, wraplength=170, justify="left").pack(anchor="w", padx=12, pady=(0, 10))
        btn_c3 = ctk.CTkButton(
            c3,
            text="Adicionar Caminho",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            height=28,
            corner_radius=6,
            command=self.app.prompt_add_custom_folder
        )
        btn_c3.pack(fill="x", padx=12, pady=(0, 10))

        ctk.CTkLabel(
            self.empty_state_frame,
            text="Garantia de Custódia: Zero telemetria e zero dependência de nuvem. Operação 100% local no disco.",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color="#94a3b8"
        ).pack(anchor="center", pady=(6, 20))

        # Painel de Diretrizes de Transporte & Compactação
        bottom_controls = ctk.CTkFrame(self.main_content, fg_color=SURFACE_INNER, corner_radius=12, border_width=1, border_color=BORDER_OUTLINE)
        bottom_controls.pack(fill="x", pady=(0, 0))

        ctk.CTkLabel(
            bottom_controls,
            text="DIRETRIZES DE TRANSPORTE & COMPACTAÇÃO",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#475569"
        ).pack(anchor="w", padx=14, pady=(8, 2))

        opts_row = ctk.CTkFrame(bottom_controls, fg_color="transparent")
        opts_row.pack(fill="x", padx=14, pady=(2, 4))

        rb_lzma = ctk.CTkRadioButton(
            opts_row,
            text="Super Compressão (LZMA2 Ultra) • Redução de até 85% (Recomendado)",
            variable=self.app.compress_mode,
            value="lzma",
            fg_color=COLOR_PRIMARY,
            text_color=TEXT_ON_SURFACE,
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold")
        )
        rb_lzma.pack(side="left", padx=(0, 20), pady=2)

        rb_zip = ctk.CTkRadioButton(
            opts_row,
            text="Modo Rápido (ZIP / Deflate)",
            variable=self.app.compress_mode,
            value="deflate",
            fg_color=COLOR_PRIMARY,
            text_color=TEXT_ON_SURFACE,
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold")
        )
        rb_zip.pack(side="left", pady=2)

        sw_kill = ctk.CTkSwitch(
            bottom_controls,
            text="Isolamento seguro de processos de IDE antes da leitura (Preserva integridade SQLite state.vscdb)",
            variable=self.app.force_kill_proc,
            progress_color=COLOR_PRIMARY,
            text_color=TEXT_MUTED,
            font=ctk.CTkFont(family="Segoe UI", size=11)
        )
        sw_kill.pack(anchor="w", padx=14, pady=(2, 8))

        self.btn_export = ctk.CTkButton(
            bottom_controls,
            text="GERAR PACOTE DE TRANSPORTE (.agpkg)",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            height=44,
            corner_radius=10,
            command=self.app.start_export_thread
        )
        self.btn_export.pack(fill="x", padx=10, pady=(0, 10))

        # Atualiza contagem inicial
        self.update_active_count()

    def toggle_sidebar(self):
        """Alterna a visibilidade da barra lateral do Catálogo via Menu Sanduíche."""
        if not self.is_sidebar_collapsed:
            self.sidebar.pack_forget()
            self.collapsed_catalog_rail.pack(side="left", fill="y", padx=(0, 6), pady=0)
            self.is_sidebar_collapsed = True
        else:
            self.collapsed_catalog_rail.pack_forget()
            self.sidebar.pack(side="left", fill="y", padx=(0, 6), pady=0)
            self.is_sidebar_collapsed = False

    def render_catalog_items(self):
        """Renderiza os itens do catálogo na barra lateral com feedback de estado ativo."""
        for w in self.catalog_scroll.winfo_children():
            w.destroy()

        cat_map = {
            "Todos": "all",
            "Agentes IA": "ai_agents",
            "TI & Infra": "it_sysadmin",
            "Dev & Terminal": "dev_workstation",
            "Conhecimento": "knowledge_base"
        }
        selected_cat_id = cat_map.get(self.active_category, "all")

        catalog = presets.get_catalog()
        active_ids = {box.box_id for box in self.app.data_boxes}

        for p_info in catalog:
            if selected_cat_id != "all" and p_info.get("category_id") != selected_cat_id:
                continue

            is_already_added = p_info["id"] in active_ids

            item_card = ctk.CTkFrame(
                self.catalog_scroll,
                fg_color=SURFACE_CARD,
                corner_radius=8,
                border_width=1,
                border_color="#93c5fd" if is_already_added else BORDER_LIGHT
            )
            item_card.pack(fill="x", pady=2, padx=2)

            top_i = ctk.CTkFrame(item_card, fg_color="transparent")
            top_i.pack(fill="x", padx=10, pady=6)

            short_title = p_info["title"].split("•")[0].strip()
            title_col = ctk.CTkFrame(top_i, fg_color="transparent")
            title_col.pack(side="left", fill="x", expand=True, padx=(2, 6))

            title_lbl = ctk.CTkLabel(
                title_col,
                text=short_title,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color=COLOR_PRIMARY if is_already_added else TEXT_ON_SURFACE,
                anchor="w"
            )
            title_lbl.pack(anchor="w")

            target_lbl = ctk.CTkLabel(
                title_col,
                text=f"Pasta: /{p_info['archive_folder']}/",
                font=ctk.CTkFont(family="Consolas", size=9),
                text_color="#64748b",
                anchor="w"
            )
            target_lbl.pack(anchor="w")

            if is_already_added:
                btn_status = ctk.CTkButton(
                    top_i,
                    text="✓ No Pacote",
                    width=78,
                    height=24,
                    corner_radius=6,
                    font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
                    fg_color=STATUS_SAFE_BG,
                    hover_color="#d1fae5",
                    text_color=STATUS_SAFE,
                    command=lambda p=p_info: self.remove_preset_from_selection(p)
                )
                btn_status.pack(side="right")
            else:
                btn_add = ctk.CTkButton(
                    top_i,
                    text="+ Adicionar",
                    width=78,
                    height=24,
                    corner_radius=6,
                    font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
                    fg_color="#eff6ff",
                    hover_color="#dbeafe",
                    text_color=COLOR_PRIMARY,
                    command=lambda p=p_info: self.add_preset_to_selection(p)
                )
                btn_add.pack(side="right")

    def on_category_chip_changed(self, choice):
        self.active_category = choice
        self.render_catalog_items()

    def remove_preset_from_selection(self, p_info):
        """Remove o módulo selecionado das caixas ativas."""
        for box in list(self.app.data_boxes):
            if box.box_id == p_info["id"]:
                self.app.remove_data_box(box)
                break
        self.render_catalog_items()

    def add_preset_to_selection(self, p_info):
        """Adiciona um preset individual do catálogo à área central de caixas de caminhos."""
        for box in self.app.data_boxes:
            if box.box_id == p_info["id"]:
                box.var_check.set(True)
                self.render_catalog_items()
                return

        self.app.add_data_box(
            container=self.boxes_container,
            box_id=p_info["id"],
            title=p_info["title"],
            desc=p_info["desc"],
            default_path=p_info["default_path"],
            archive_folder=p_info["archive_folder"],
            is_custom=False,
            initial_check=True
        )
        self.update_active_count()
        self.render_catalog_items()

    def apply_profile(self, profile):
        """Aplica um perfil pronto, preenchendo as caixas correspondentes."""
        self.clear_all_boxes()
        target_ids = profile.get("ids", [])
        catalog = presets.get_catalog()

        for p_id in target_ids:
            for p_info in catalog:
                if p_info["id"] == p_id:
                    self.app.add_data_box(
                        container=self.boxes_container,
                        box_id=p_info["id"],
                        title=p_info["title"],
                        desc=p_info["desc"],
                        default_path=p_info["default_path"],
                        archive_folder=p_info["archive_folder"],
                        is_custom=False,
                        initial_check=p_info["detected"]
                    )
                    break
        self.update_active_count()
        self.render_catalog_items()

    def clear_all_boxes(self):
        """Limpa todas as caixas de anexação."""
        for box in list(self.app.data_boxes):
            self.app.remove_data_box(box)
        self.update_active_count()
        self.render_catalog_items()

    def update_active_count(self):
        """Atualiza o contador e a visibilidade do estado vazio."""
        count = len(self.app.data_boxes)
        if count == 0:
            self.lbl_active_count.configure(text="Nenhum caminho adicionado")
            self.empty_state_frame.pack(fill="both", expand=True, padx=8, pady=16)
            self.boxes_container.pack_forget()
        elif count == 1:
            self.lbl_active_count.configure(text="1 caminho pronto para transporte")
            self.empty_state_frame.pack_forget()
            self.boxes_container.pack(fill="x", pady=2)
        else:
            self.lbl_active_count.configure(text=f"{count} caminhos prontos para transporte")
            self.empty_state_frame.pack_forget()
            self.boxes_container.pack(fill="x", pady=2)

    def setup_import_tab(self, parent):
        """Aba de Importação e Restauração com Inspetor de Manifesto."""
        scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=4, pady=4)

        info_box = ctk.CTkFrame(scroll, fg_color=SURFACE_INNER, corner_radius=12, border_width=1, border_color=BORDER_OUTLINE)
        info_box.pack(fill="x", pady=6, padx=4)

        ctk.CTkLabel(
            info_box,
            text="RESTAURAÇÃO E APLICAÇÃO DE DADOS NO NOTEBOOK",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=COLOR_PRIMARY
        ).pack(anchor="w", padx=14, pady=(10, 3))

        ctk.CTkLabel(
            info_box,
            text="Selecione o arquivo de pacote (.agpkg) gerado no desktop. O Data Bridge lerá o manifesto interno e distribuirá cada módulo diretamente nos seus locais originais no Windows.",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=TEXT_MUTED,
            justify="left"
        ).pack(anchor="w", padx=14, pady=(0, 10))

        pkg_card = ctk.CTkFrame(scroll, fg_color=SURFACE_CARD, corner_radius=12, border_width=1, border_color=BORDER_OUTLINE)
        pkg_card.pack(fill="x", pady=8, padx=4)

        ctk.CTkLabel(
            pkg_card,
            text="Arquivo de Pacote (.agpkg / .7z / .zip):",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=TEXT_ON_SURFACE
        ).pack(anchor="w", padx=14, pady=(10, 4))

        row_pkg = ctk.CTkFrame(pkg_card, fg_color="transparent")
        row_pkg.pack(fill="x", padx=14, pady=(0, 12))

        entry_pkg = ctk.CTkEntry(
            row_pkg,
            textvariable=self.app.package_import_path,
            fg_color=INPUT_WELL,
            border_color=BORDER_OUTLINE,
            text_color=TEXT_ON_SURFACE,
            height=34,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        entry_pkg.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_browse_pkg = ctk.CTkButton(
            row_pkg,
            text="Procurar Pacote...",
            width=135,
            height=34,
            corner_radius=8,
            fg_color="#f1f5f9",
            hover_color="#e2e8f0",
            text_color=TEXT_ON_SURFACE,
            border_width=1,
            border_color=BORDER_OUTLINE,
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            command=self.app.browse_package_file
        )
        btn_browse_pkg.pack(side="right")

        self.inspect_frame = ctk.CTkFrame(scroll, fg_color=SURFACE_INNER, corner_radius=12, border_width=1, border_color=BORDER_OUTLINE)
        self.inspect_frame.pack(fill="x", pady=8, padx=4)

        ctk.CTkLabel(
            self.inspect_frame,
            text="INSPETOR DO PACOTE DE DADOS",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#475569"
        ).pack(anchor="w", padx=14, pady=(10, 2))

        self.lbl_inspect_title = ctk.CTkLabel(
            self.inspect_frame,
            text="○ Nenhum pacote carregado. Selecione um arquivo .agpkg para inspecionar os módulos e integridade.",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=TEXT_MUTED
        )
        self.lbl_inspect_title.pack(anchor="w", padx=14, pady=(0, 6))

        self.inspect_details = ctk.CTkLabel(
            self.inspect_frame,
            text="",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=TEXT_MUTED,
            justify="left"
        )
        self.inspect_details.pack(anchor="w", padx=14, pady=(0, 12))

        self.btn_import = ctk.CTkButton(
            scroll,
            text="RESTAURAR E APLICAR DADOS NESTE COMPUTADOR",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=STATUS_SAFE,
            hover_color="#047857",
            height=44,
            corner_radius=10,
            command=self.app.start_import_thread
        )
        self.btn_import.pack(fill="x", padx=4, pady=(12, 10))

class NyxiaCoreBridgeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Data Bridge • Custódia e Transporte de Dados")
        self.geometry("1020x900")
        self.minsize(940, 820)
        self.configure(fg_color=SURFACE_BASE)

        # Configura ícone da janela (Compatível com Windows e Linux Ubuntu)
        ico_path = get_resource_path("app_icon.ico")
        png_path = get_resource_path("app_icon.png")
        if sys.platform == "win32" and ico_path.exists():
            try:
                self.iconbitmap(str(ico_path))
            except Exception:
                pass
        elif png_path.exists():
            try:
                from PIL import ImageTk
                self._app_icon_tk = ImageTk.PhotoImage(file=str(png_path))
                self.iconphoto(False, self._app_icon_tk)
            except Exception:
                pass

        self.data_boxes = []
        self.custom_box_counter = 0

        self.compress_mode = ctk.StringVar(value="lzma")
        self.force_kill_proc = ctk.BooleanVar(value=True)

        self.package_import_path = ctk.StringVar(value="")
        self.import_manifest = None
        self.is_running = False

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        # Rodapé fixo universal com Logo da Nyxia
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.pack(fill="x", side="bottom", pady=(0, 10))

        logo_path = get_resource_path("nyxia_logo.png")
        if logo_path.exists():
            try:
                pil_img = Image.open(str(logo_path))
                self.nyxia_ctk_img = ctk.CTkImage(
                    light_image=pil_img,
                    dark_image=pil_img,
                    size=(pil_img.width, pil_img.height)
                )
                lbl_nyxia_logo = ctk.CTkLabel(
                    self.footer_frame,
                    image=self.nyxia_ctk_img,
                    text=""
                )
                lbl_nyxia_logo.pack(anchor="center", pady=(0, 2))
            except Exception:
                lbl_nyxia_logo = ctk.CTkLabel(
                    self.footer_frame,
                    text="NYXIA SYSTEMS • SOLUÇÕES EM IA",
                    font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                    text_color=COLOR_PRIMARY
                )
                lbl_nyxia_logo.pack(anchor="center")
        else:
            lbl_nyxia_logo = ctk.CTkLabel(
                self.footer_frame,
                text="NYXIA SYSTEMS • SOLUÇÕES EM IA",
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                text_color=COLOR_PRIMARY
            )
            lbl_nyxia_logo.pack(anchor="center")

        lbl_nyxia_sub = ctk.CTkLabel(
            self.footer_frame,
            text="Custódia e Transporte de Dados • Antigravity & Estações de Trabalho",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=TEXT_MUTED
        )
        lbl_nyxia_sub.pack(anchor="center")

        self.main_tool_screen = None
        self.onboarding_screen = OnboardingScreen(self.container, on_finish_callback=self.show_main_tool)
        
        self.show_onboarding()
        self.after(150, lambda: apply_acrylic_glass(self, dark=False, alpha=0.94))

    def show_onboarding(self):
        if self.main_tool_screen:
            self.main_tool_screen.pack_forget()
        self.onboarding_screen.pack(fill="both", expand=True)

    def show_main_tool(self):
        self.onboarding_screen.pack_forget()
        if not self.main_tool_screen:
            self.main_tool_screen = MainToolScreen(self.container, self)
        self.main_tool_screen.pack(fill="both", expand=True)

    def add_data_box(self, container, box_id, title, desc, default_path, archive_folder, is_custom=False, initial_check=True):
        box = DataBoxWidget(
            parent=container,
            box_id=box_id,
            title=title,
            desc=desc,
            default_path=default_path,
            archive_folder=archive_folder,
            on_remove_callback=self.remove_data_box,
            is_custom=is_custom,
            initial_check=initial_check
        )
        self.data_boxes.append(box)
        if self.main_tool_screen:
            self.main_tool_screen.update_active_count()
            self.main_tool_screen.render_catalog_items()
        return box

    def remove_data_box(self, box_instance):
        if box_instance in self.data_boxes:
            self.data_boxes.remove(box_instance)
            box_instance.destroy()
        if self.main_tool_screen:
            self.main_tool_screen.update_active_count()
            self.main_tool_screen.render_catalog_items()

    def prompt_add_custom_folder(self):
        if not self.main_tool_screen:
            return
        chosen = filedialog.askdirectory()
        if chosen:
            norm = os.path.normpath(chosen)
            folder_name = os.path.basename(norm) or "Pasta"
            self.custom_box_counter += 1
            box_id = f"custom_{self.custom_box_counter}"
            self.add_data_box(
                container=self.main_tool_screen.boxes_container,
                box_id=box_id,
                title=f"Custom • {folder_name}",
                desc=f"Diretório pessoal: {norm}",
                default_path=norm,
                archive_folder=f"custom_{folder_name}_{self.custom_box_counter}",
                is_custom=True,
                initial_check=True
            )

    def browse_package_file(self):
        chosen = filedialog.askopenfilename(
            filetypes=[("Pacotes Data Bridge", "*.agpkg;*.7z;*.zip"), ("Todos os Arquivos", "*.*")]
        )
        if chosen:
            self.package_import_path.set(os.path.normpath(chosen))
            self.inspect_package(chosen)

    def inspect_package(self, pkg_path):
        if not self.main_tool_screen:
            return
        try:
            manifest = engine.read_manifest(pkg_path)
            self.import_manifest = manifest
            modules = manifest.get("modules", {})

            lines = [
                f"Gerado em: {manifest.get('created_at', 'Desconhecido')}",
                f"Modo: {manifest.get('compression_mode', '').upper()}",
                f"Tamanho Descomprimido: {manifest.get('total_uncompressed_bytes', 0) / (1024*1024):.2f} MB ({manifest.get('total_files', 0)} arquivos)",
                "\nMódulos Contidos no Pacote:"
            ]
            for m_key, m_data in modules.items():
                lines.append(f" • {m_key}: {m_data.get('total_files', 0)} arquivos ({m_data.get('total_bytes', 0)/(1024*1024):.2f} MB)")

            self.main_tool_screen.lbl_inspect_title.configure(text="● Manifesto Válido (Versão 3.2)", text_color=STATUS_SAFE)
            self.main_tool_screen.inspect_details.configure(text="\n".join(lines))
        except Exception as e:
            self.main_tool_screen.lbl_inspect_title.configure(text="▲ Pacote Inválido ou Corrompido", text_color=STATUS_WARN)
            self.main_tool_screen.inspect_details.configure(text=str(e))

    def update_progress_ui(self, fraction, current_file, processed_bytes, total_bytes):
        if not self.main_tool_screen:
            return
        mb_proc = processed_bytes / (1024 * 1024)
        mb_tot = total_bytes / (1024 * 1024)
        pct = int(fraction * 100)

        self.main_tool_screen.progress_bar.set(fraction)
        self.main_tool_screen.lbl_progress.configure(text=f"PROCESSING: {pct}% ({mb_proc:.1f} MB / {mb_tot:.1f} MB)")

        if len(current_file) > 65:
            display_file = current_file[:30] + "..." + current_file[-30:]
        else:
            display_file = current_file
        self.main_tool_screen.lbl_details.configure(text=f"Stream Node: {display_file}")

    def start_export_thread(self):
        if self.is_running or not self.main_tool_screen:
            return

        targets = {}
        procs_to_check = set()

        for box in self.data_boxes:
            if box.var_check.get() and box.var_path.get():
                p = Path(box.var_path.get())
                if p.exists():
                    targets[box.box_id] = {
                        "source_path": str(p),
                        "archive_folder": box.archive_folder
                    }
                    for p_cat in presets.PRESETS_CATALOG:
                        if p_cat["id"] == box.box_id:
                            for pr in p_cat.get("processes", []):
                                procs_to_check.add(pr)

        if not targets:
            messagebox.showwarning("Aviso", "Selecione ao menos uma caixa de dados ativa com caminho existente antes de exportar.")
            return

        mode = self.compress_mode.get()
        save_file = filedialog.asksaveasfilename(
            defaultextension=".agpkg",
            filetypes=[("Pacote Data Bridge", "*.agpkg"), ("Arquivo 7-Zip", "*.7z"), ("Arquivo Zip", "*.zip")]
        )
        if not save_file:
            return

        self.is_running = True
        self.main_tool_screen.btn_export.configure(state="disabled", text="COMPACTANDO DADOS & MEMÓRIAS...")
        self.main_tool_screen.progress_bar.set(0.0)

        threading.Thread(target=self._run_export_worker, args=(targets, save_file, mode, list(procs_to_check)), daemon=True).start()

    def _run_export_worker(self, targets, save_file, mode, procs_to_check):
        try:
            if self.force_kill_proc.get() and procs_to_check:
                running = engine.check_process_running(procs_to_check)
                if running:
                    self.main_tool_screen.lbl_progress.configure(text="Quiescing active instances for atomic SQLite lock...")
                    engine.kill_processes(procs_to_check)

            self.main_tool_screen.lbl_progress.configure(text="Mapping directory nodes and calculating payload footprint...")
            engine.compress_package(
                targets=targets,
                output_filepath=save_file,
                compression_mode=mode,
                progress_callback=lambda fr, f, pb, tb: self.after(0, self.update_progress_ui, fr, f, pb, tb)
            )

            self.after(0, lambda: self._on_export_success(save_file))
        except Exception as e:
            self.after(0, lambda: self._on_export_error(str(e)))

    def _on_export_success(self, save_file):
        self.is_running = False
        self.main_tool_screen.btn_export.configure(state="normal", text="GERAR PACOTE DE TRANSPORTE (.agpkg)")
        self.progress_bar.set(1.0)
        self.main_tool_screen.lbl_progress.configure(text="● Exportação Concluída com Sucesso!", text_color=STATUS_SAFE)
        self.main_tool_screen.lbl_details.configure(text=f"Archive generated: {save_file}")

        open_folder = messagebox.askyesno(
            "Sucesso",
            f"Pacote de dados criado com sucesso!\n\nSalvo em:\n{save_file}\n\nDeseja abrir a pasta onde o arquivo foi salvo?"
        )
        if open_folder:
            if sys.platform == "win32":
                os.system(f'explorer /select,"{os.path.normpath(save_file)}"')
            elif sys.platform.startswith("linux"):
                folder = os.path.dirname(os.path.normpath(save_file)) or "."
                os.system(f'xdg-open "{folder}" &')
            elif sys.platform == "darwin":
                os.system(f'open -R "{save_file}"')

    def _on_export_error(self, err_msg):
        self.is_running = False
        self.main_tool_screen.btn_export.configure(state="normal", text="GERAR PACOTE DE TRANSPORTE (.agpkg)")
        self.lbl_progress.configure(text="▲ Falha na Exportação do Pacote", text_color=STATUS_WARN)
        self.lbl_details.configure(text=err_msg)
        messagebox.showerror("Erro na Exportação", f"Não foi possível concluir o backup:\n\n{err_msg}")

    def start_import_thread(self):
        if self.is_running or not self.main_tool_screen:
            return

        pkg_path = self.package_import_path.get()
        if not pkg_path or not Path(pkg_path).exists():
            messagebox.showwarning("Aviso", "Selecione um arquivo de pacote (.agpkg) válido.")
            return

        confirm = messagebox.askyesno(
            "Confirmar Restauração",
            "Atenção: A restauração irá restaurar e mesclar os dados locais pelos contidos no pacote.\n"
            "Recomendamos que seus assistentes de IA, terminais e editores estejam fechados.\n\nDeseja prosseguir?"
        )
        if not confirm:
            return

        self.is_running = True
        self.main_tool_screen.btn_import.configure(state="disabled", text="RESTAURANDO DADOS NO DISCO...")
        self.main_tool_screen.progress_bar.set(0.0)

        threading.Thread(target=self._run_import_worker, args=(pkg_path,), daemon=True).start()

    def _run_import_worker(self, pkg_path):
        try:
            procs = ["antigravity.exe", "Cursor.exe", "Obsidian.exe", "Windsurf.exe", "Code.exe", "dbeaver.exe", "winscp.exe"]
            engine.kill_processes(procs)

            manifest = engine.read_manifest(pkg_path)
            modules = manifest.get("modules", {})

            destinations = {}
            catalog_map = {p["archive_folder"]: p["default_path"] for p in presets.PRESETS_CATALOG}

            for mod_key, mod_info in modules.items():
                arc_folder = mod_info.get("archive_folder", mod_key)
                if arc_folder in catalog_map:
                    destinations[arc_folder] = catalog_map[arc_folder]
                else:
                    orig_path = mod_info.get("source_path", "")
                    folder_name = os.path.basename(orig_path) or "RestoredFolder"
                    destinations[arc_folder] = str(Path(USERPROFILE) / "NyxiaRestored" / folder_name)

            engine.decompress_package(
                package_path=pkg_path,
                destinations=destinations,
                progress_callback=lambda fr, f, pb, tb: self.after(0, self.update_progress_ui, fr, f, pb, tb)
            )

            self.after(0, self._on_import_success)
        except Exception as e:
            self.after(0, lambda: self._on_import_error(str(e)))

    def _on_import_success(self):
        self.is_running = False
        self.main_tool_screen.btn_import.configure(state="normal", text="RESTAURAR E APLICAR DADOS NESTE COMPUTADOR")
        self.progress_bar.set(1.0)
        self.main_tool_screen.lbl_progress.configure(text="● Restauração Concluída com Sucesso!", text_color=STATUS_SAFE)
        self.main_tool_screen.lbl_details.configure(text="Todos os agentes, memórias e arquivos foram restaurados com sucesso.")

        messagebox.showinfo(
            "Sucesso",
            "A migração foi concluída com êxito!\n\nSeus assistentes, configurações de TI e dados transportados estão prontos para uso no seu notebook."
        )

    def _on_import_error(self, err_msg):
        self.is_running = False
        self.main_tool_screen.btn_import.configure(state="normal", text="RESTAURAR E APLICAR DADOS NESTE COMPUTADOR")
        self.lbl_progress.configure(text="▲ Falha na Restauração do Pacote", text_color=STATUS_WARN)
        self.lbl_details.configure(text=err_msg)
        messagebox.showerror("Erro na Importação", f"Ocorreu um erro ao restaurar os dados:\n\n{err_msg}")

if __name__ == "__main__":
    # Se argumentos de linha de comando foram passados, despacha para a CLI ou MCP (utilizável por agentes de IA)
    if len(sys.argv) > 1 and sys.argv[1] in ("--cli", "-c", "cli", "list", "export", "inspect", "restore", "mcp", "--help", "-h"):
        import cli
        sys.exit(cli.main() or 0)
    else:
        app = NyxiaCoreBridgeApp()
        app.mainloop()
