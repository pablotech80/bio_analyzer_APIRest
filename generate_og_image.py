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

# Colores
COLOR_BG_START = (26, 26, 26)      # #1A1A1A
COLOR_BG_END = (44, 62, 80)        # #2C3E50
COLOR_WHITE = (255, 255, 255)      # #FFFFFF
COLOR_GRAY = (189, 195, 199)       # #BDC3C7
COLOR_GREEN = (39, 174, 96)        # #27AE60

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

def add_logo(image, logo_path, size=250):
    """Añade el logo centrado."""
    try:
        logo = Image.open(logo_path).convert("RGBA")
        logo.thumbnail((size, size), Image.Resampling.LANCZOS)
        
        # Centrar horizontalmente, Y=150
        x = (WIDTH - logo.width) // 2
        y = 150
        
        # Crear capa para el logo con transparencia
        image.paste(logo, (x, y), logo)
        print(f"✓ Logo añadido: {logo.width}x{logo.height}px en posición ({x}, {y})")
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
        add_logo(image, LOGO_PATH, size=250)
    else:
        print(f"⚠ Logo no encontrado en: {LOGO_PATH}")
        print("  Continuando sin logo...")
    
    # 3. Añadir textos
    print("\n3. Añadiendo textos...")
    draw = ImageDraw.Draw(image)
    
    # Título principal
    add_text(draw, "Entrenador Personal + IA", 350, 48, COLOR_WHITE, "bold")
    
    # Subtítulo
    add_text(draw, "Análisis Biométrico Gratis en 90 Segundos", 420, 32, COLOR_GRAY, "regular")
    
    # Footer con checks
    add_text(draw, "✓ 90seg  ✓ Sin tarjeta  ✓ 100% Gratis", 510, 24, COLOR_GREEN, "regular")
    
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
