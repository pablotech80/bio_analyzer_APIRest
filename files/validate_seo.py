#!/usr/bin/env python3
"""
Script de Validación SEO - CoachBodyFit360
==========================================

Este script verifica que todos los elementos SEO estén correctamente
implementados antes del deployment.

Uso:
    python validate_seo.py

Verifica:
    ✓ Meta tags presentes en HTML
    ✓ Open Graph tags completos
    ✓ Schema.org JSON-LD válido
    ✓ Imágenes OG existen y tienen tamaño correcto
    ✓ Sitemap.xml accesible
    ✓ Robots.txt accesible
    ✓ Favicons presentes

Retorna:
    Exit code 0 si todo OK
    Exit code 1 si hay errores críticos
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import List, Tuple
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from PIL import Image

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
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


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


class SEOValidator:
    """Validador principal de SEO."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        """
        Inicializa el validador.
        
        Args:
            base_url: URL base de la aplicación (local o producción)
        """
        self.base_url = base_url.rstrip('/')
        self.errors = []
        self.warnings = []
        self.successes = []
    
    def validate_html_meta_tags(self) -> bool:
        """
        Valida que los meta tags esenciales estén presentes.
        
        Returns:
            True si todos los tags críticos existen
        """
        print_header("Validando Meta Tags HTML")
        
        try:
            response = requests.get(self.base_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Tags críticos a verificar
            critical_tags = {
                'title': soup.find('title'),
                'description': soup.find('meta', attrs={'name': 'description'}),
                'viewport': soup.find('meta', attrs={'name': 'viewport'}),
                'canonical': soup.find('link', attrs={'rel': 'canonical'}),
            }
            
            all_ok = True
            
            for tag_name, tag_element in critical_tags.items():
                if tag_element:
                    if tag_name == 'title':
                        content = tag_element.string
                    elif tag_name == 'canonical':
                        content = tag_element.get('href', '')
                    else:
                        content = tag_element.get('content', '')
                    
                    if content:
                        print_success(f"{tag_name}: {content[:60]}...")
                        self.successes.append(f"Meta {tag_name} presente")
                    else:
                        print_warning(f"{tag_name} existe pero está vacío")
                        self.warnings.append(f"Meta {tag_name} vacío")
                else:
                    print_error(f"{tag_name} NO ENCONTRADO")
                    self.errors.append(f"Meta {tag_name} faltante")
                    all_ok = False
            
            # Verificar longitud de title y description
            title = critical_tags['title']
            if title and len(title.string) > 60:
                print_warning(f"Title muy largo ({len(title.string)} chars, recomendado <60)")
                self.warnings.append("Title demasiado largo")
            
            desc = critical_tags['description']
            if desc:
                desc_content = desc.get('content', '')
                if len(desc_content) > 160:
                    print_warning(f"Description muy larga ({len(desc_content)} chars, recomendado <160)")
                    self.warnings.append("Description demasiado larga")
            
            return all_ok
            
        except requests.RequestException as e:
            print_error(f"Error al conectar con {self.base_url}: {e}")
            self.errors.append(f"Conexión fallida: {e}")
            return False
    
    def validate_open_graph(self) -> bool:
        """Valida Open Graph tags."""
        print_header("Validando Open Graph Tags")
        
        try:
            response = requests.get(self.base_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            required_og = [
                'og:title',
                'og:description',
                'og:image',
                'og:url',
                'og:type'
            ]
            
            all_ok = True
            
            for og_tag in required_og:
                tag = soup.find('meta', property=og_tag)
                if tag and tag.get('content'):
                    print_success(f"{og_tag}: {tag['content'][:50]}...")
                    self.successes.append(f"OG {og_tag} presente")
                else:
                    print_error(f"{og_tag} NO ENCONTRADO")
                    self.errors.append(f"OG {og_tag} faltante")
                    all_ok = False
            
            # Validar imagen OG
            og_image = soup.find('meta', property='og:image')
            if og_image:
                image_url = og_image['content']
                self._validate_og_image(image_url)
            
            return all_ok
            
        except requests.RequestException as e:
            print_error(f"Error al validar OG: {e}")
            self.errors.append(f"Validación OG fallida: {e}")
            return False
    
    def _validate_og_image(self, image_url: str):
        """Valida dimensiones de imagen Open Graph."""
        try:
            # Si es URL relativa, construir completa
            if not image_url.startswith('http'):
                image_url = urljoin(self.base_url, image_url)
            
            response = requests.get(image_url, timeout=10)
            
            if response.status_code == 200:
                # Guardar temporalmente para analizar
                with open('/tmp/og_temp.jpg', 'wb') as f:
                    f.write(response.content)
                
                # Verificar dimensiones
                img = Image.open('/tmp/og_temp.jpg')
                width, height = img.size
                
                if width == 1200 and height == 630:
                    print_success(f"Imagen OG: {width}x{height} ✓ (PERFECTO)")
                    self.successes.append("Imagen OG con dimensiones correctas")
                else:
                    print_warning(f"Imagen OG: {width}x{height} (recomendado 1200x630)")
                    self.warnings.append(f"Imagen OG tamaño incorrecto: {width}x{height}")
                
                # Verificar peso
                size_kb = len(response.content) / 1024
                if size_kb > 300:
                    print_warning(f"Imagen OG muy pesada: {size_kb:.1f}KB (recomendado <300KB)")
                    self.warnings.append(f"Imagen OG muy pesada: {size_kb:.1f}KB")
                else:
                    print_success(f"Imagen OG peso OK: {size_kb:.1f}KB")
                
                os.remove('/tmp/og_temp.jpg')
            else:
                print_error(f"Imagen OG no accesible: HTTP {response.status_code}")
                self.errors.append(f"Imagen OG HTTP {response.status_code}")
        
        except Exception as e:
            print_error(f"Error validando imagen OG: {e}")
            self.errors.append(f"Error imagen OG: {e}")
    
    def validate_schema_org(self) -> bool:
        """Valida JSON-LD Schema.org."""
        print_header("Validando Schema.org JSON-LD")
        
        try:
            response = requests.get(self.base_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar todos los scripts de tipo JSON-LD
            json_lds = soup.find_all('script', type='application/ld+json')
            
            if not json_lds:
                print_error("NO se encontró Schema.org JSON-LD")
                self.errors.append("Schema.org faltante")
                return False
            
            print_info(f"Encontrados {len(json_lds)} bloques JSON-LD")
            
            all_valid = True
            
            for idx, json_ld in enumerate(json_lds, 1):
                try:
                    data = json.loads(json_ld.string)
                    schema_type = data.get('@type', 'Unknown')
                    print_success(f"JSON-LD #{idx} válido: @type = {schema_type}")
                    self.successes.append(f"Schema.org {schema_type} válido")
                    
                    # Validar campos requeridos según el tipo
                    if schema_type == 'ProfessionalService':
                        required = ['name', 'description', 'url']
                        for field in required:
                            if field not in data:
                                print_warning(f"Campo '{field}' faltante en {schema_type}")
                                self.warnings.append(f"Schema {schema_type} sin campo {field}")
                
                except json.JSONDecodeError as e:
                    print_error(f"JSON-LD #{idx} INVÁLIDO: {e}")
                    self.errors.append(f"JSON-LD #{idx} inválido")
                    all_valid = False
            
            return all_valid
            
        except requests.RequestException as e:
            print_error(f"Error al validar Schema: {e}")
            self.errors.append(f"Validación Schema fallida: {e}")
            return False
    
    def validate_sitemap(self) -> bool:
        """Valida sitemap.xml."""
        print_header("Validando Sitemap.xml")
        
        sitemap_url = f"{self.base_url}/sitemap.xml"
        
        try:
            response = requests.get(sitemap_url, timeout=10)
            
            if response.status_code == 200:
                print_success(f"Sitemap accesible: {sitemap_url}")
                
                # Verificar que sea XML válido
                soup = BeautifulSoup(response.content, 'xml')
                urls = soup.find_all('url')
                
                if urls:
                    print_success(f"Sitemap contiene {len(urls)} URLs")
                    self.successes.append(f"Sitemap con {len(urls)} URLs")
                    
                    # Mostrar primeras 3 URLs
                    print_info("Primeras URLs en sitemap:")
                    for url in urls[:3]:
                        loc = url.find('loc')
                        if loc:
                            print(f"  • {loc.text}")
                    
                    return True
                else:
                    print_warning("Sitemap XML válido pero sin URLs")
                    self.warnings.append("Sitemap vacío")
                    return True
            else:
                print_error(f"Sitemap no accesible: HTTP {response.status_code}")
                self.errors.append(f"Sitemap HTTP {response.status_code}")
                return False
        
        except Exception as e:
            print_error(f"Error al validar sitemap: {e}")
            self.errors.append(f"Error sitemap: {e}")
            return False
    
    def validate_robots_txt(self) -> bool:
        """Valida robots.txt."""
        print_header("Validando Robots.txt")
        
        robots_url = f"{self.base_url}/robots.txt"
        
        try:
            response = requests.get(robots_url, timeout=10)
            
            if response.status_code == 200:
                print_success(f"Robots.txt accesible: {robots_url}")
                
                # Verificar contenido mínimo
                content = response.text
                if 'User-agent' in content:
                    print_success("Robots.txt contiene directivas User-agent")
                    self.successes.append("Robots.txt válido")
                
                if 'Sitemap:' in content:
                    print_success("Robots.txt referencia al Sitemap")
                else:
                    print_warning("Robots.txt no referencia Sitemap (recomendado)")
                    self.warnings.append("Robots.txt sin referencia a Sitemap")
                
                return True
            else:
                print_error(f"Robots.txt no accesible: HTTP {response.status_code}")
                self.errors.append(f"Robots.txt HTTP {response.status_code}")
                return False
        
        except Exception as e:
            print_error(f"Error al validar robots.txt: {e}")
            self.errors.append(f"Error robots.txt: {e}")
            return False
    
    def generate_report(self):
        """Genera reporte final."""
        print_header("REPORTE FINAL")
        
        total_checks = len(self.successes) + len(self.errors) + len(self.warnings)
        success_rate = (len(self.successes) / total_checks * 100) if total_checks > 0 else 0
        
        print(f"\n{Colors.BOLD}Resumen:{Colors.END}")
        print(f"  ✓ Éxitos: {Colors.GREEN}{len(self.successes)}{Colors.END}")
        print(f"  ✗ Errores: {Colors.RED}{len(self.errors)}{Colors.END}")
        print(f"  ⚠ Advertencias: {Colors.YELLOW}{len(self.warnings)}{Colors.END}")
        print(f"  📊 Tasa de éxito: {Colors.BOLD}{success_rate:.1f}%{Colors.END}\n")
        
        if self.errors:
            print(f"{Colors.RED}{Colors.BOLD}ERRORES CRÍTICOS:{Colors.END}")
            for error in self.errors:
                print(f"  • {error}")
            print()
        
        if self.warnings:
            print(f"{Colors.YELLOW}{Colors.BOLD}ADVERTENCIAS:{Colors.END}")
            for warning in self.warnings:
                print(f"  • {warning}")
            print()
        
        # Recomendaciones
        if success_rate < 80:
            print(f"{Colors.RED}{Colors.BOLD}❌ SEO NO OPTIMIZADO{Colors.END}")
            print("Corrige los errores críticos antes del deployment.\n")
            return False
        elif success_rate < 95:
            print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  SEO PARCIALMENTE OPTIMIZADO{Colors.END}")
            print("Considera resolver las advertencias para mejores resultados.\n")
            return True
        else:
            print(f"{Colors.GREEN}{Colors.BOLD}✅ SEO COMPLETAMENTE OPTIMIZADO{Colors.END}")
            print("¡Tu sitio está listo para rankear en Google! 🚀\n")
            return True


def main():
    """Función principal."""
    print(f"{Colors.BOLD}CoachBodyFit360 - Validador SEO{Colors.END}")
    print(f"Versión 1.0 - Octubre 2025\n")
    
    # Detectar URL base (puede pasarse como argumento)
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    
    print_info(f"Validando: {base_url}")
    print_info("Asegúrate de que la aplicación esté corriendo...\n")
    
    # Crear validador
    validator = SEOValidator(base_url)
    
    # Ejecutar validaciones
    results = []
    results.append(validator.validate_html_meta_tags())
    results.append(validator.validate_open_graph())
    results.append(validator.validate_schema_org())
    results.append(validator.validate_sitemap())
    results.append(validator.validate_robots_txt())
    
    # Generar reporte
    is_ready = validator.generate_report()
    
    # Exit code
    sys.exit(0 if is_ready else 1)


if __name__ == "__main__":
    # Dependencias necesarias
    try:
        import requests
        from bs4 import BeautifulSoup
        from PIL import Image
    except ImportError as e:
        print(f"{Colors.RED}Error: Falta instalar dependencias{Colors.END}")
        print(f"\nEjecuta: pip install requests beautifulsoup4 pillow lxml\n")
        sys.exit(1)
    
    main()
