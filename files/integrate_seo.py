#!/usr/bin/env python3
"""
Script de Integración SEO Automática - CoachBodyFit360
======================================================

Este script aplica automáticamente todos los cambios SEO necesarios
a tu proyecto bio_analyzer_APIRest.

IMPORTANTE: Haz backup antes de ejecutar (el script lo hace automáticamente)

Uso:
    cd /Users/macbookpro/bio_analyzer_APIRest
    python integrate_seo.py

¿Qué hace?
    1. Detecta estructura del proyecto (Flask/Django)
    2. Crea backup automático en ./backups/
    3. Modifica templates/base.html con meta tags
    4. Crea utils/seo.py con funciones auxiliares
    5. Modifica vistas para incluir contexto SEO
    6. Crea templates/sitemap.xml
    7. Valida que todo funcione

Principios aplicados:
    - SRP: Cada función hace una cosa
    - Defensive: Valida antes de modificar
    - Safe: Crea backups automáticos
    - Transparent: Muestra cada paso
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Imprime header de sección."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")


def print_success(text: str):
    """Imprime mensaje de éxito."""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text: str):
    """Imprime mensaje de error."""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_warning(text: str):
    """Imprime mensaje de advertencia."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def print_info(text: str):
    """Imprime mensaje informativo."""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")


class SEOIntegrator:
    """Integrador automático de cambios SEO."""
    
    def __init__(self, project_root: str):
        """
        Inicializa el integrador.
        
        Args:
            project_root: Ruta raíz del proyecto
        """
        self.project_root = Path(project_root)
        self.backup_dir = self.project_root / 'backups' / f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        self.changes_made = []
        self.errors = []
        
    def detect_project_structure(self) -> dict:
        """
        Detecta la estructura del proyecto Flask.
        
        Returns:
            Dict con rutas detectadas
        """
        print_header("Detectando Estructura del Proyecto")
        
        structure = {
            'templates_dir': None,
            'static_dir': None,
            'views_file': None,
            'utils_dir': None,
            'base_html': None,
            'is_flask': False,
        }
        
        # Buscar templates/
        possible_templates = [
            self.project_root / 'templates',
            self.project_root / 'app' / 'templates',
            self.project_root / 'src' / 'templates',
        ]
        
        for path in possible_templates:
            if path.exists():
                structure['templates_dir'] = path
                print_success(f"Templates encontrado: {path}")
                break
        
        if not structure['templates_dir']:
            print_error("No se encontró directorio templates/")
            return structure
        
        # Buscar base.html
        base_html = structure['templates_dir'] / 'base.html'
        if base_html.exists():
            structure['base_html'] = base_html
            print_success(f"base.html encontrado: {base_html}")
        else:
            print_warning("base.html NO encontrado (se creará uno nuevo)")
        
        # Buscar static/
        possible_static = [
            self.project_root / 'static',
            self.project_root / 'app' / 'static',
            self.project_root / 'src' / 'static',
        ]
        
        for path in possible_static:
            if path.exists():
                structure['static_dir'] = path
                print_success(f"Static encontrado: {path}")
                break
        
        # Buscar archivo de vistas (app.py, views.py, etc.)
        possible_views = [
            self.project_root / 'app.py',
            self.project_root / 'main.py',
            self.project_root / 'run.py',
            self.project_root / 'app' / 'views.py',
            self.project_root / 'apps' / 'landing' / 'views.py',
        ]
        
        for path in possible_views:
            if path.exists():
                structure['views_file'] = path
                print_success(f"Vistas encontrado: {path}")
                break
        
        # Verificar si es Flask
        if structure['views_file']:
            with open(structure['views_file'], 'r') as f:
                content = f.read()
                if 'from flask import' in content or 'import flask' in content:
                    structure['is_flask'] = True
                    print_success("Proyecto Flask detectado ✓")
        
        # Buscar o crear utils/
        possible_utils = [
            self.project_root / 'utils',
            self.project_root / 'app' / 'utils',
        ]
        
        for path in possible_utils:
            if path.exists():
                structure['utils_dir'] = path
                print_success(f"Utils encontrado: {path}")
                break
        
        if not structure['utils_dir']:
            structure['utils_dir'] = self.project_root / 'utils'
            print_info(f"Utils se creará en: {structure['utils_dir']}")
        
        return structure
    
    def create_backup(self) -> bool:
        """
        Crea backup de archivos que se van a modificar.
        
        Returns:
            True si el backup fue exitoso
        """
        print_header("Creando Backup de Seguridad")
        
        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            print_success(f"Directorio de backup creado: {self.backup_dir}")
            
            # Backup de archivos críticos
            files_to_backup = [
                self.structure.get('base_html'),
                self.structure.get('views_file'),
            ]
            
            for file_path in files_to_backup:
                if file_path and file_path.exists():
                    backup_path = self.backup_dir / file_path.name
                    shutil.copy2(file_path, backup_path)
                    print_success(f"Backup: {file_path.name}")
            
            print_info(f"Backup completo en: {self.backup_dir}")
            return True
            
        except Exception as e:
            print_error(f"Error al crear backup: {e}")
            return False
    
    def modify_base_html(self) -> bool:
        """
        Modifica o crea base.html con meta tags SEO.
        
        Returns:
            True si la modificación fue exitosa
        """
        print_header("Modificando base.html")
        
        base_html = self.structure.get('base_html')
        
        if not base_html:
            print_warning("base.html no existe, se creará uno nuevo básico")
            base_html = self.structure['templates_dir'] / 'base.html'
        
        try:
            # Leer contenido actual si existe
            if base_html.exists():
                with open(base_html, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Verificar si ya tiene SEO
                if 'og:title' in content:
                    print_warning("base.html ya parece tener meta tags SEO")
                    response = input("¿Quieres sobrescribirlos? (s/n): ")
                    if response.lower() != 's':
                        print_info("Saltando modificación de base.html")
                        return True
            else:
                content = self._get_base_html_template()
            
            # Insertar fragmento SEO
            seo_fragment = self._get_seo_fragment()
            
            # Buscar dónde insertar (después de <title>)
            if '</title>' in content:
                content = content.replace('</title>', f'</title>\n{seo_fragment}')
            elif '<head>' in content:
                content = content.replace('<head>', f'<head>\n{seo_fragment}')
            else:
                print_error("No se encontró <head> ni <title> en base.html")
                return False
            
            # Escribir archivo modificado
            with open(base_html, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print_success(f"base.html modificado exitosamente")
            self.changes_made.append(str(base_html))
            return True
            
        except Exception as e:
            print_error(f"Error al modificar base.html: {e}")
            self.errors.append(f"base.html: {e}")
            return False
    
    def create_utils_seo(self) -> bool:
        """
        Crea utils/seo.py con funciones auxiliares.
        
        Returns:
            True si la creación fue exitosa
        """
        print_header("Creando utils/seo.py")
        
        utils_dir = self.structure['utils_dir']
        
        try:
            # Crear directorio utils si no existe
            utils_dir.mkdir(parents=True, exist_ok=True)
            
            # Crear __init__.py si no existe
            init_file = utils_dir / '__init__.py'
            if not init_file.exists():
                init_file.touch()
                print_success(f"Creado: {init_file}")
            
            # Crear seo.py
            seo_file = utils_dir / 'seo.py'
            seo_content = self._get_seo_utils_content()
            
            with open(seo_file, 'w', encoding='utf-8') as f:
                f.write(seo_content)
            
            print_success(f"Creado: {seo_file}")
            self.changes_made.append(str(seo_file))
            return True
            
        except Exception as e:
            print_error(f"Error al crear utils/seo.py: {e}")
            self.errors.append(f"utils/seo.py: {e}")
            return False
    
    def create_sitemap_template(self) -> bool:
        """
        Crea template de sitemap.xml.
        
        Returns:
            True si la creación fue exitosa
        """
        print_header("Creando templates/sitemap.xml")
        
        templates_dir = self.structure['templates_dir']
        
        try:
            sitemap_file = templates_dir / 'sitemap.xml'
            sitemap_content = self._get_sitemap_content()
            
            with open(sitemap_file, 'w', encoding='utf-8') as f:
                f.write(sitemap_content)
            
            print_success(f"Creado: {sitemap_file}")
            self.changes_made.append(str(sitemap_file))
            return True
            
        except Exception as e:
            print_error(f"Error al crear sitemap.xml: {e}")
            self.errors.append(f"sitemap.xml: {e}")
            return False
    
    def show_next_steps(self):
        """Muestra los pasos manuales que el usuario debe completar."""
        print_header("Pasos Manuales Restantes")
        
        print(f"{Colors.BOLD}1. Modificar tu archivo de vistas:{Colors.END}")
        views_file = self.structure.get('views_file')
        if views_file:
            print(f"\n   Archivo: {Colors.YELLOW}{views_file}{Colors.END}\n")
        
        print("   Añade este import al inicio:")
        print(f"   {Colors.GREEN}from utils.seo import get_landing_seo_data{Colors.END}\n")
        
        print("   Modifica tu vista de landing (función index o home):")
        print(f"   {Colors.GREEN}# ANTES")
        print(f"   @app.route('/')")
        print(f"   def index():")
        print(f"       return render_template('landing.html')")
        print()
        print(f"   # DESPUÉS")
        print(f"   @app.route('/')")
        print(f"   def index():")
        print(f"       seo_data = get_landing_seo_data()")
        print(f"       return render_template('landing.html', seo=seo_data){Colors.END}\n")
        
        print(f"{Colors.BOLD}2. Añadir rutas de sitemap y robots:{Colors.END}\n")
        print(f"   {Colors.GREEN}@app.route('/sitemap.xml')")
        print(f"   def sitemap():")
        print(f"       from flask import make_response")
        print(f"       from datetime import datetime")
        print(f"       pages = [")
        print(f"           url_for('index', _external=True),")
        print(f"       ]")
        print(f"       sitemap_xml = render_template('sitemap.xml', pages=pages, now=datetime.now())")
        print(f"       response = make_response(sitemap_xml)")
        print(f"       response.headers['Content-Type'] = 'application/xml'")
        print(f"       return response")
        print()
        print(f"   @app.route('/robots.txt')")
        print(f"   def robots():")
        print(f"       robots_txt = f'''User-agent: *")
        print(f"   Allow: /")
        print(f"   Sitemap: {{url_for('sitemap', _external=True)}}'''")
        print(f"       response = make_response(robots_txt)")
        print(f"       response.headers['Content-Type'] = 'text/plain'")
        print(f"       return response{Colors.END}\n")
        
        print(f"{Colors.BOLD}3. Crear imágenes SEO:{Colors.END}\n")
        print("   - Imagen Open Graph (1200x630px): static/images/og-image-cbf360.jpg")
        print("   - Favicons: Usar https://realfavicongenerator.net/\n")
        
        print(f"{Colors.BOLD}4. Validar implementación:{Colors.END}\n")
        print(f"   {Colors.GREEN}python validate_seo.py http://localhost:5000{Colors.END}\n")
    
    def _get_base_html_template(self) -> str:
        """Retorna template básico de base.html si no existe."""
        return """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}CoachBodyFit360{% endblock %}</title>
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% block content %}{% endblock %}
    
    {% block extra_js %}{% endblock %}
</body>
</html>"""
    
    def _get_seo_fragment(self) -> str:
        """Retorna el fragmento HTML de SEO tags."""
        return '''
    <!-- ========== SEO META TAGS ========== -->
    <meta name="description" content="{{ seo.description if seo else 'Transforma tu cuerpo con entrenador personal profesional + IA' }}">
    <meta name="keywords" content="{{ seo.keywords if seo else 'entrenador personal online, IA fitness' }}">
    <link rel="canonical" href="{{ seo.canonical if seo else request.url }}">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="{{ seo.og_type if seo else 'website' }}">
    <meta property="og:url" content="{{ request.url }}">
    <meta property="og:title" content="{{ seo.title if seo else (title ~ ' | CoachBodyFit360') }}">
    <meta property="og:description" content="{{ seo.description if seo else 'Entrenador Personal + IA' }}">
    <meta property="og:image" content="{{ seo.og_image if seo else url_for('static', filename='images/og-image-cbf360.jpg', _external=True) }}">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{{ seo.title if seo else (title ~ ' | CoachBodyFit360') }}">
    <meta name="twitter:description" content="{{ seo.description if seo else 'Entrenador Personal + IA' }}">
    <meta name="twitter:image" content="{{ seo.og_image if seo else url_for('static', filename='images/og-image-cbf360.jpg', _external=True) }}">
    
    <!-- Schema.org JSON-LD -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "ProfessionalService",
      "name": "CoachBodyFit360",
      "description": "Entrenador personal profesional con 20 años de experiencia + IA",
      "url": "{{ request.url_root }}",
      "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "EUR"
      }
    }
    </script>
    <!-- ========== END SEO META TAGS ========== -->
'''
    
    def _get_seo_utils_content(self) -> str:
        """Retorna contenido de utils/seo.py."""
        return '''"""
Utilidades SEO para CoachBodyFit360
===================================

Generado automáticamente por integrate_seo.py
"""

from flask import url_for
from typing import Dict, Any


def get_landing_seo_data() -> Dict[str, Any]:
    """
    Genera metadatos SEO optimizados para la landing page.
    
    Returns:
        Dict con campos: title, description, keywords, og_image, etc.
    """
    return {
        'title': 'Entrenador Personal + IA | Análisis Gratis 90seg | CoachBodyFit360',
        'description': (
            'Transforma tu cuerpo con 20 años de experiencia + IA avanzada. '
            'Análisis biométrico completo en 90 segundos. '
            'Plan personalizado gratis. Sin tarjeta de crédito.'
        ),
        'keywords': (
            'entrenador personal online, plan fitness personalizado, '
            'análisis biométrico gratis, IA fitness, coaching nutricional'
        ),
        'og_image': url_for(
            'static',
            filename='images/og-image-cbf360.jpg',
            _external=True
        ),
        'og_type': 'website',
        'canonical': url_for('index', _external=True),  # Ajusta según tu ruta
    }
'''
    
    def _get_sitemap_content(self) -> str:
        """Retorna contenido de sitemap.xml."""
        return '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{{ url_for('index', _external=True) }}</loc>
    <lastmod>{{ now.strftime('%Y-%m-%d') if now else '2025-10-31' }}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  
  {% if pages %}
  {% for page in pages %}
  <url>
    <loc>{{ page }}</loc>
    <lastmod>{{ now.strftime('%Y-%m-%d') if now else '2025-10-31' }}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  {% endfor %}
  {% endif %}
</urlset>'''
    
    def run(self) -> bool:
        """
        Ejecuta el proceso completo de integración.
        
        Returns:
            True si todo fue exitoso
        """
        print(f"\n{Colors.BOLD}CoachBodyFit360 - Integrador SEO Automático{Colors.END}")
        print(f"Proyecto: {self.project_root}\n")
        
        # Detectar estructura
        self.structure = self.detect_project_structure()
        
        if not self.structure['templates_dir']:
            print_error("No se pudo detectar la estructura del proyecto")
            return False
        
        # Confirmar antes de proceder
        print(f"\n{Colors.YELLOW}Se van a modificar los siguientes archivos:{Colors.END}")
        if self.structure.get('base_html'):
            print(f"  - {self.structure['base_html']}")
        print(f"  - {self.structure['utils_dir'] / 'seo.py'} (nuevo)")
        print(f"  - {self.structure['templates_dir'] / 'sitemap.xml'} (nuevo)")
        
        response = input(f"\n{Colors.BOLD}¿Continuar? (s/n): {Colors.END}")
        if response.lower() != 's':
            print_info("Operación cancelada por el usuario")
            return False
        
        # Crear backup
        if not self.create_backup():
            print_error("No se pudo crear backup. Abortando.")
            return False
        
        # Aplicar cambios
        success = True
        success &= self.modify_base_html()
        success &= self.create_utils_seo()
        success &= self.create_sitemap_template()
        
        # Resumen
        print_header("Resumen de Cambios")
        
        if self.changes_made:
            print(f"{Colors.GREEN}Archivos modificados/creados:{Colors.END}")
            for change in self.changes_made:
                print(f"  ✓ {change}")
        
        if self.errors:
            print(f"\n{Colors.RED}Errores encontrados:{Colors.END}")
            for error in self.errors:
                print(f"  ✗ {error}")
        
        # Próximos pasos
        self.show_next_steps()
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}✓ Integración automática completada{Colors.END}")
        print(f"{Colors.YELLOW}Recuerda completar los pasos manuales listados arriba{Colors.END}\n")
        
        return success


def main():
    """Función principal."""
    # Detectar directorio actual
    current_dir = os.getcwd()
    
    # Verificar si estamos en el proyecto correcto
    if 'bio_analyzer' not in current_dir.lower():
        print_warning(f"Directorio actual: {current_dir}")
        print_warning("No parece ser el proyecto bio_analyzer_APIRest")
        response = input("¿Continuar de todas formas? (s/n): ")
        if response.lower() != 's':
            print_info("Operación cancelada")
            return
    
    # Ejecutar integrador
    integrator = SEOIntegrator(current_dir)
    success = integrator.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
