import math
from PIL import Image, ImageDraw, ImageFilter

def create_nyxia_data_bridge_icon(size=512):
    # Imagem RGBA de alta fidelidade
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    pad = int(size * 0.06)
    r = int(size * 0.22)
    
    # 1. Base Squircle com Efeito de Vidro e Sombra Suave
    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle(
        [pad + 4, pad + 10, size - pad + 4, size - pad + 10],
        radius=r,
        fill=(15, 23, 42, 45)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=int(size * 0.035)))
    img = Image.alpha_composite(shadow, img)
    draw = ImageDraw.Draw(img)

    # 2. Superfície Crystalline Glass (Gradiente radial simulado)
    for i in range(pad, pad + 40):
        alpha_val = int(255 * (1 - (i - pad) / 40.0 * 0.08))
    
    # Preenchimento em gradiente vertical de vidro translúcido
    base_card = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(base_card)
    
    # Simula gradiente vertical
    for y in range(pad, size - pad):
        factor = (y - pad) / (size - 2 * pad)
        # De #faf8ff (quase branco/gelo) para #eaedff (suave tom cristal fluído)
        red = int(250 - factor * 16)
        green = int(248 - factor * 12)
        blue = int(255 - factor * 2)
        b_draw.line([(pad, y), (size - pad, y)], fill=(red, green, blue, 248))
    
    # Cria máscara com cantos arredondados
    mask = Image.new("L", (size, size), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle([pad, pad, size - pad, size - pad], radius=r, fill=255)
    
    # Borda de vidro perimetral polida
    card_cut = Image.composite(base_card, Image.new("RGBA", (size, size), (0, 0, 0, 0)), mask)
    img = Image.alpha_composite(img, card_cut)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([pad, pad, size - pad, size - pad], radius=r, outline=(203, 213, 225, 220), width=max(2, int(size * 0.008)))
    
    # 3. Desenho Central: O Nômade Neural Bridge (Símbolo de Ponte de Dados & Conexão Cognitiva)
    center_x = size / 2.0
    center_y = size / 2.0
    scale = size * 0.58
    
    # Pontos da Ponte Neural ("N" estilizado com nós interligados e fitas de transmissão)
    # Nós de Origem (Desktop) e Destino (Notebook/Cloudless)
    p1 = (center_x - scale * 0.32, center_y + scale * 0.28)  # Nó inferior esquerdo
    p2 = (center_x - scale * 0.32, center_y - scale * 0.16)  # Nó superior esquerdo
    p3 = (center_x - scale * 0.10, center_y + scale * 0.08)  # Ponto de inflexão bridge 1
    p4 = (center_x + scale * 0.10, center_y - scale * 0.08)  # Ponto de inflexão bridge 2
    p5 = (center_x + scale * 0.32, center_y + scale * 0.16)  # Nó inferior direito
    p6 = (center_x + scale * 0.32, center_y - scale * 0.28)  # Nó superior direito

    # Traçado das vigas da ponte de dados (Glow suave)
    glow_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow_layer)
    
    beam_w = int(size * 0.048)
    
    # Feixes de conexão com cores do Design System:
    # Segmento 1: Terracota Nyxia (#c2410c)
    g_draw.line([p1, p2], fill=(194, 65, 12, 160), width=beam_w + 6)
    g_draw.line([p2, p3], fill=(194, 65, 12, 160), width=beam_w + 6)
    # Segmento Ponte: Transição para Cobalto (#2563eb / #004ac6)
    g_draw.line([p3, p4], fill=(70, 72, 212, 180), width=beam_w + 8)
    # Segmento 2: Cobalto Primário (#004ac6)
    g_draw.line([p4, p5], fill=(0, 74, 198, 160), width=beam_w + 6)
    g_draw.line([p5, p6], fill=(0, 74, 198, 160), width=beam_w + 6)
    # Linha diagonal de ponte contínua (N-Loop infinito)
    g_draw.line([p2, p5], fill=(99, 102, 241, 140), width=int(beam_w * 0.8) + 6)

    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=int(size * 0.018)))
    img = Image.alpha_composite(img, glow_layer)
    draw = ImageDraw.Draw(img)

    # Traçado nítido da Ponte
    draw.line([p1, p2], fill=(194, 65, 12, 255), width=beam_w)
    draw.line([p2, p3], fill=(194, 65, 12, 255), width=beam_w)
    draw.line([p3, p4], fill=(70, 72, 212, 255), width=beam_w + 2)
    draw.line([p4, p5], fill=(0, 74, 198, 255), width=beam_w)
    draw.line([p5, p6], fill=(0, 74, 198, 255), width=beam_w)
    draw.line([p2, p5], fill=(99, 102, 241, 220), width=int(beam_w * 0.75))

    # Nós Esféricos / Células de Memória com brilho especular
    node_rad = int(size * 0.052)
    nodes = [
        (p1, (194, 65, 12)),
        (p2, (217, 85, 25)),
        (p3, (99, 102, 241)),
        (p4, (70, 72, 212)),
        (p5, (0, 74, 198)),
        (p6, (37, 99, 235))
    ]

    for pt, col in nodes:
        # Círculo externo
        draw.ellipse(
            [pt[0] - node_rad, pt[1] - node_rad, pt[0] + node_rad, pt[1] + node_rad],
            fill=col + (255,),
            outline=(255, 255, 255, 230),
            width=max(2, int(size * 0.008))
        )
        # Brilho de reflexo de vidro (especular)
        hl_rad = int(node_rad * 0.38)
        draw.ellipse(
            [pt[0] - node_rad * 0.45, pt[1] - node_rad * 0.45, pt[0] - node_rad * 0.45 + hl_rad, pt[1] - node_rad * 0.45 + hl_rad],
            fill=(255, 255, 255, 210)
        )

    # Partículas de dados fluindo na ponte (Data Stream)
    particle_rad = int(size * 0.016)
    particles = [
        ((center_x - scale * 0.22, center_y + scale * 0.06), (255, 255, 255)),
        ((center_x, center_y), (255, 255, 255)),
        ((center_x + scale * 0.22, center_y - scale * 0.06), (255, 255, 255)),
    ]
    for pt, col in particles:
        draw.ellipse(
            [pt[0] - particle_rad, pt[1] - particle_rad, pt[0] + particle_rad, pt[1] + particle_rad],
            fill=col + (255,)
        )

    return img

def main():
    print("Gerando icones do Nyxia Data Bridge...")
    icon_512 = create_nyxia_data_bridge_icon(512)
    icon_512.save("app_icon.png", format="PNG")
    print(" - app_icon.png gerado com sucesso (512x512)")

    # Gera versao de icone para header (40x40 e 64x64)
    icon_64 = icon_512.resize((64, 64), Image.Resampling.LANCZOS)
    icon_64.save("header_icon.png", format="PNG")
    print(" - header_icon.png gerado com sucesso (64x64)")

    # Gera arquivo de icone nativo do Windows .ico (multi-resolucao)
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    icon_512.save("app_icon.ico", format="ICO", sizes=icon_sizes)
    print(" - app_icon.ico gerado com sucesso (multi-layer Windows icon)")

if __name__ == "__main__":
    main()
