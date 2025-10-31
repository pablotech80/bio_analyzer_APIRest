# 🚀 GUÍA DE INTEGRACIÓN RÁPIDA
## Para tu proyecto: /Users/macbookpro/bio_analyzer_APIRest

---

## ⚡ OPCIÓN 1: INTEGRACIÓN AUTOMÁTICA (Recomendada)

### Paso 1: Descargar archivos
Descarga todos los archivos del paquete SEO en tu proyecto:
```
/Users/macbookpro/bio_analyzer_APIRest/
```

### Paso 2: Ejecutar script automático
```bash
cd /Users/macbookpro/bio_analyzer_APIRest
python integrate_seo.py
```

El script automáticamente:
- ✅ Detecta tu estructura de proyecto
- ✅ Crea backup de seguridad
- ✅ Modifica `templates/base.html`
- ✅ Crea `utils/seo.py`
- ✅ Crea `templates/sitemap.xml`
- ✅ Te muestra los pasos manuales restantes

---

## 🔧 OPCIÓN 2: INTEGRACIÓN MANUAL (Si prefieres control total)

### PASO 1: Modificar `templates/base.html`

**Ubicación:** `/Users/macbookpro/bio_analyzer_APIRest/templates/base.html`

**Acción:** Abre el archivo y busca la línea `</title>`.

**Justo después** de `</title>`, pega este código:

```html
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
```

---

### PASO 2: Crear `utils/seo.py`

**Ubicación:** `/Users/macbookpro/bio_analyzer_APIRest/utils/seo.py`

**Acción:** Crea el archivo y pega este código:

```python
"""
Utilidades SEO para CoachBodyFit360
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
```

**IMPORTANTE:** Si no tienes carpeta `utils/`, créala primero:
```bash
mkdir -p /Users/macbookpro/bio_analyzer_APIRest/utils
touch /Users/macbookpro/bio_analyzer_APIRest/utils/__init__.py
```

---

### PASO 3: Modificar tu archivo principal de vistas

**Ubicación probable:** `/Users/macbookpro/bio_analyzer_APIRest/app.py` o similar

**Busca la función que renderiza la landing page** (probablemente se llame `index()` o `home()`).

**ANTES:**
```python
@app.route('/')
def index():
    return render_template('landing.html')
```

**DESPUÉS:**
```python
from utils.seo import get_landing_seo_data  # ← Añadir este import al inicio

@app.route('/')
def index():
    seo_data = get_landing_seo_data()  # ← Añadir esta línea
    return render_template('landing.html', seo=seo_data)  # ← Modificar esta línea
```

---

### PASO 4: Añadir rutas de Sitemap y Robots

**En el mismo archivo de vistas**, añade estas dos funciones:

```python
from flask import make_response
from datetime import datetime

@app.route('/sitemap.xml')
def sitemap():
    """Genera sitemap.xml dinámico."""
    pages = [
        url_for('index', _external=True),
        # Añade más URLs aquí si tienes
    ]
    sitemap_xml = render_template('sitemap.xml', pages=pages, now=datetime.now())
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response


@app.route('/robots.txt')
def robots():
    """Genera robots.txt dinámico."""
    robots_txt = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/private/

Sitemap: {url_for('sitemap', _external=True)}
"""
    response = make_response(robots_txt)
    response.headers['Content-Type'] = 'text/plain'
    return response
```

---

### PASO 5: Crear template `sitemap.xml`

**Ubicación:** `/Users/macbookpro/bio_analyzer_APIRest/templates/sitemap.xml`

**Acción:** Crea el archivo y pega:

```xml
<?xml version="1.0" encoding="UTF-8"?>
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
</urlset>
```

---

## 🎨 PASO 6: Crear Imágenes SEO

### Imagen Open Graph (CRÍTICO)

**Destino:** `/Users/macbookpro/bio_analyzer_APIRest/static/images/og-image-cbf360.jpg`

**Dimensiones:** 1200x630px (OBLIGATORIO)

**Herramienta:** https://www.canva.com/

**Contenido:**
1. Fondo: Gradiente negro (#1A1A1A → #2C3E50)
2. Logo centrado (250x250px)
3. Texto: "Entrenador Personal + IA" (Poppins Bold, 48px, blanco)
4. Subtexto: "Análisis Biométrico Gratis" (Inter, 32px, gris)
5. Footer: "✓ 90seg  ✓ Sin tarjeta  ✓ 100% Gratis" (Inter, 24px, verde)

### Favicons

**Herramienta:** https://realfavicongenerator.net/

**Proceso:**
1. Sube tu logo
2. Configura colores (theme: #E74C3C)
3. Descarga el pack
4. Extrae en `/Users/macbookpro/bio_analyzer_APIRest/static/`

---

## ✅ PASO 7: Validar

### Validación Local

```bash
cd /Users/macbookpro/bio_analyzer_APIRest

# Instalar dependencias
pip install requests beautifulsoup4 pillow lxml

# Ejecutar Flask
flask run

# En otra terminal, validar
python validate_seo.py http://localhost:5000
```

**Objetivo:** Tasa de éxito ≥ 95%

---

## 🚀 PASO 8: Deploy

```bash
# Commit
git add .
git commit -m "feat(seo): implementar meta tags, OG, Schema.org y sitemap"

# Push
git push origin main
```

---

## 📊 CHECKLIST DE VERIFICACIÓN

- [ ] `templates/base.html` modificado con meta tags
- [ ] `utils/seo.py` creado
- [ ] Vista de landing modificada (pasa contexto `seo`)
- [ ] Rutas `/sitemap.xml` y `/robots.txt` añadidas
- [ ] `templates/sitemap.xml` creado
- [ ] Imagen OG creada (1200x630px)
- [ ] Favicons instalados
- [ ] Script de validación ejecutado (>95%)
- [ ] Código desplegado a producción
- [ ] Validado en Facebook Debugger
- [ ] Validado en Google Rich Results

---

## 🆘 AYUDA RÁPIDA

### Error: "No module named 'utils'"

**Solución:**
```bash
mkdir -p /Users/macbookpro/bio_analyzer_APIRest/utils
touch /Users/macbookpro/bio_analyzer_APIRest/utils/__init__.py
```

### Error: "Template not found: sitemap.xml"

**Solución:** Verifica que el archivo existe en:
```
/Users/macbookpro/bio_analyzer_APIRest/templates/sitemap.xml
```

### Error: Imagen OG no aparece

**Solución:**
1. Verifica que existe: `static/images/og-image-cbf360.jpg`
2. Dimensiones exactas: 1200x630px
3. Usar Facebook Debugger → "Scrape Again"

---

## 📞 SIGUIENTE PASO

Una vez completado todo esto:

**Responde "éxito"** y pasamos a la **FASE 2: Optimización de Conversión (CRO)**
- Refactorizar Hero Section
- CTA above the fold
- Quick Trust Section
- +200% conversión adicional

---

*Última actualización: 31 Octubre 2025*
