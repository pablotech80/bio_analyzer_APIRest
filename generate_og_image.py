#!/usr/bin/env python3
"""
Script para generar imagen Open Graph automáticamente
Genera: og-image-cbf360.jpg (1200x630px)
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Configuración
OUTPUT_PATH = "app/static/images/og-image-cbf360.jpg"
LOGO_PATH = "app/static/images/logo2-coachbodyfit360.png"
WIDTH = 1200
HEIGHT = 630

# Colores - Diseño claro y visible
COLOR_BG_START = (231, 76, 60)     # #E74C3C (Rojo vibrante)
COLOR_BG_END = (192, 57, 43)       # #C0392B (Rojo oscuro)
COLOR_WHITE = (255, 255, 255)      # #FFFFFF
COLOR_BLACK = (0, 0, 0)            # #000000
COLOR_LIGHT = (255, 255, 255)      # #FFFFFF

def create_gradient_background(width, height, color_start, color_end):
    """Crea un fondo con gradiente diagonal."""
    base = Image.new('RGB', (width, height), color_start)
    top = Image.new('RGB', (width, height), color_end)
    mask = Image.new('L', (width, height))
    mask_data = []
    
    for y in range(height):
        for x in range(width):
            # Gradiente diagonal
            distance = ((x / width) + (y / height)) / 2
            mask_data.append(int(255 * distance))
    
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def add_logo(image, logo_path, size=220):
    """Añade el logo centrado con fondo blanco circular."""
    try:
        logo = Image.open(logo_path).convert("RGBA")
        logo.thumbnail((size, size), Image.Resampling.LANCZOS)
        
        # Crear círculo blanco de fondo
        circle_size = size + 40
        circle = Image.new('RGBA', (circle_size, circle_size), (0, 0, 0, 0))
        draw_circle = ImageDraw.Draw(circle)
        draw_circle.ellipse([0, 0, circle_size, circle_size], fill=(255, 255, 255, 255))
        
        # Centrar logo en el círculo
        logo_offset = ((circle_size - logo.width) // 2, (circle_size - logo.height) // 2)
        circle.paste(logo, logo_offset, logo)
        
        # Centrar círculo en la imagen
        x = (WIDTH - circle_size) // 2
        y = 80
        
        # Pegar círculo con logo
        image.paste(circle, (x, y), circle)
        print(f"✓ Logo añadido: {logo.width}x{logo.height}px con fondo circular blanco")
    except Exception as e:
        print(f"⚠ No se pudo cargar el logo: {e}")
        print("  Continuando sin logo...")

def add_text(draw, text, y_position, font_size, color, font_weight="regular"):
    """Añade texto centrado."""
    try:
        # Intentar usar fuentes del sistema (macOS)
        font_paths = {
            "bold": "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "regular": "/System/Library/Fonts/Supplemental/Arial.ttf",
        }
        
        font_path = font_paths.get(font_weight, font_paths["regular"])
        
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
        else:
            # Fallback a fuente por defecto
            font = ImageFont.load_default()
            print(f"⚠ Usando fuente por defecto para: {text}")
    except:
        font = ImageFont.load_default()
        print(f"⚠ Usando fuente por defecto para: {text}")
    
    # Calcular posición centrada
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (WIDTH - text_width) // 2
    
    # Dibujar texto con sombra para mejor legibilidad
    # Sombra
    draw.text((x + 2, y_position + 2), text, font=font, fill=(0, 0, 0, 128))
    # Texto principal
    draw.text((x, y_position), text, font=font, fill=color)
    
    print(f"✓ Texto añadido: '{text}' en Y={y_position}")

def generate_og_image():
    """Genera la imagen Open Graph completa."""
    print("\n" + "="*70)
    print("Generando imagen Open Graph - CoachBodyFit360".center(70))
    print("="*70 + "\n")
    
    # 1. Crear fondo con gradiente
    print("1. Creando fondo con gradiente...")
    image = create_gradient_background(WIDTH, HEIGHT, COLOR_BG_START, COLOR_BG_END)
    print(f"✓ Fondo creado: {WIDTH}x{HEIGHT}px")
    
    # 2. Añadir logo
    print("\n2. Añadiendo logo...")
    if os.path.exists(LOGO_PATH):
        add_logo(image, LOGO_PATH, size=220)
    else:
        print(f"⚠ Logo no encontrado en: {LOGO_PATH}")
        print("  Continuando sin logo...")
    
    # 3. Añadir textos
    print("\n3. Añadiendo textos...")
    draw = ImageDraw.Draw(image)
    
    # Título principal (más abajo por el logo con círculo)
    add_text(draw, "Entrenador Personal + IA", 380, 52, COLOR_WHITE, "bold")
    
    # Subtítulo
    add_text(draw, "Análisis Biométrico Gratis", 460, 36, COLOR_WHITE, "regular")
    
    # Footer con checks
    add_text(draw, "✓ 90seg  ✓ Sin tarjeta  ✓ 100% Gratis", 530, 28, COLOR_WHITE, "bold")
    
    # 4. Guardar imagen
    print("\n4. Guardando imagen...")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    image.save(OUTPUT_PATH, "JPEG", quality=85, optimize=True)
    
    # Verificar tamaño del archivo
    file_size = os.path.getsize(OUTPUT_PATH) / 1024  # KB
    print(f"✓ Imagen guardada: {OUTPUT_PATH}")
    print(f"✓ Tamaño: {file_size:.1f} KB")
    
    if file_size > 300:
        print(f"⚠ Advertencia: Imagen > 300KB. Considera comprimir en https://tinypng.com/")
    
    print("\n" + "="*70)
    print("✓ IMAGEN OPEN GRAPH GENERADA EXITOSAMENTE".center(70))
    print("="*70 + "\n")
    print(f"Ubicación: {os.path.abspath(OUTPUT_PATH)}")
    print(f"Dimensiones: {WIDTH}x{HEIGHT}px")
    print(f"Tamaño: {file_size:.1f} KB")
    print("\nPróximo paso: Generar favicons en https://realfavicongenerator.net/")

if __name__ == "__main__":
    try:
        generate_og_image()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nAsegúrate de tener instalado Pillow:")
        print("  pip install Pillow")
