#!/usr/bin/env python3
"""
Script para generar favicons automáticamente
Genera todos los tamaños necesarios para multi-dispositivo
"""

from PIL import Image
import os
import json

# Configuración
LOGO_PATH = "app/static/images/logo2-coachbodyfit360.png"
STATIC_DIR = "app/static"
IMAGES_DIR = "app/static/images"

# Tamaños a generar
FAVICON_SIZES = {
    "favicon-16x16.png": 16,
    "favicon-32x32.png": 32,
    "apple-touch-icon.png": 180,
    "android-chrome-192x192.png": 192,
    "android-chrome-512x512.png": 512,
}

def generate_favicon_ico(logo_path, output_path):
    """Genera favicon.ico con múltiples tamaños."""
    try:
        logo = Image.open(logo_path).convert("RGBA")
        
        # Generar múltiples tamaños para .ico
        sizes = [(16, 16), (32, 32), (48, 48)]
        icons = []
        
        for size in sizes:
            resized = logo.copy()
            resized.thumbnail(size, Image.Resampling.LANCZOS)
            icons.append(resized)
        
        # Guardar como .ico
        icons[0].save(
            output_path,
            format='ICO',
            sizes=sizes,
            append_images=icons[1:]
        )
        print(f"✓ favicon.ico generado: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Error generando favicon.ico: {e}")
        return False

def generate_png_favicon(logo_path, output_path, size):
    """Genera un favicon PNG de tamaño específico."""
    try:
        logo = Image.open(logo_path).convert("RGBA")
        logo.thumbnail((size, size), Image.Resampling.LANCZOS)
        
        # Crear imagen cuadrada con el logo centrado
        favicon = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        offset = ((size - logo.width) // 2, (size - logo.height) // 2)
        favicon.paste(logo, offset, logo)
        
        favicon.save(output_path, "PNG", optimize=True)
        file_size = os.path.getsize(output_path) / 1024
        print(f"✓ {os.path.basename(output_path)}: {size}x{size}px ({file_size:.1f} KB)")
        return True
    except Exception as e:
        print(f"✗ Error generando {output_path}: {e}")
        return False

def generate_webmanifest():
    """Genera site.webmanifest para PWA."""
    manifest = {
        "name": "CoachBodyFit360",
        "short_name": "CBF360",
        "description": "Entrenador Personal + IA - Análisis Biométrico Gratis",
        "icons": [
            {
                "src": "/static/images/android-chrome-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/images/android-chrome-512x512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ],
        "theme_color": "#E74C3C",
        "background_color": "#1A1A1A",
        "display": "standalone",
        "start_url": "/"
    }
    
    output_path = os.path.join(STATIC_DIR, "site.webmanifest")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print(f"✓ site.webmanifest generado: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Error generando webmanifest: {e}")
        return False

def generate_all_favicons():
    """Genera todos los favicons necesarios."""
    print("\n" + "="*70)
    print("Generando Favicons - CoachBodyFit360".center(70))
    print("="*70 + "\n")
    
    if not os.path.exists(LOGO_PATH):
        print(f"✗ Error: Logo no encontrado en {LOGO_PATH}")
        return False
    
    # Crear directorios si no existen
    os.makedirs(STATIC_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    success_count = 0
    total_count = len(FAVICON_SIZES) + 2  # +2 por favicon.ico y webmanifest
    
    # 1. Generar favicon.ico
    print("1. Generando favicon.ico...")
    if generate_favicon_ico(LOGO_PATH, os.path.join(STATIC_DIR, "favicon.ico")):
        success_count += 1
    
    # 2. Generar PNGs
    print("\n2. Generando favicons PNG...")
    for filename, size in FAVICON_SIZES.items():
        output_path = os.path.join(IMAGES_DIR, filename)
        if generate_png_favicon(LOGO_PATH, output_path, size):
            success_count += 1
    
    # 3. Generar webmanifest
    print("\n3. Generando site.webmanifest...")
    if generate_webmanifest():
        success_count += 1
    
    # Resumen
    print("\n" + "="*70)
    if success_count == total_count:
        print("✓ TODOS LOS FAVICONS GENERADOS EXITOSAMENTE".center(70))
    else:
        print(f"⚠ {success_count}/{total_count} archivos generados".center(70))
    print("="*70 + "\n")
    
    print("Archivos generados:")
    print(f"  - {STATIC_DIR}/favicon.ico")
    print(f"  - {STATIC_DIR}/site.webmanifest")
    for filename in FAVICON_SIZES.keys():
        print(f"  - {IMAGES_DIR}/{filename}")
    
    print("\nPróximo paso: Validar implementación SEO")
    
    return success_count == total_count

if __name__ == "__main__":
    try:
        generate_all_favicons()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nAsegúrate de tener instalado Pillow:")
        print("  pip install Pillow")
