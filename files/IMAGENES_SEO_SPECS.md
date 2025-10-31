# Especificaciones de Imágenes para SEO
## CoachBodyFit360 - Guía Técnica

---

## 🎨 IMAGEN OPEN GRAPH (og-image-cbf360.jpg)

### Propósito
Esta imagen aparece cuando alguien comparte tu web en:
- Facebook
- LinkedIn  
- WhatsApp
- Twitter/X
- Slack
- Discord

### Especificaciones Técnicas

**Dimensiones:**
- Ancho: 1200px
- Alto: 630px
- Ratio: 1.91:1 (obligatorio)
- Formato: JPG o PNG
- Peso máximo: 300KB (recomendado <150KB)
- Resolución: 72 DPI

**Zona segura:**
- Deja 40px de margen en todos los lados
- Contenido crítico en el centro (600x314px)
- Evita texto < 24px (ilegible en móvil)

### Contenido Requerido

```
┌─────────────────────────────────────────────────┐
│                  [40px margen]                  │
│                                                 │
│     ┌────────────────────────────────────┐     │
│     │                                    │     │
│     │         [Logo CBF360]              │     │
│     │         (250x250px)                │     │
│     │                                    │     │
│     │  Entrenador Personal + IA          │     │
│     │  [Tipografía Poppins Bold 48px]   │     │
│     │                                    │     │
│     │  Análisis Biométrico Gratis       │     │
│     │  [Tipografía Inter Regular 32px]  │     │
│     │                                    │     │
│     │  ✓ 90 segundos  ✓ Sin tarjeta     │     │
│     │  [Tipografía Inter 24px]          │     │
│     │                                    │     │
│     └────────────────────────────────────┘     │
│                                                 │
│                  [40px margen]                  │
└─────────────────────────────────────────────────┘
```

**Colores:**
- Fondo: Gradiente de #1A1A1A a #2C3E50 (tu gradient-dark)
- Texto principal: #FFFFFF
- Texto secundario: #BDC3C7
- Accentos: #E74C3C y #E67E22 (tu gradient-hero)

### Cómo Crear (Opciones)

#### Opción 1: Figma (Recomendado)
1. Crear frame de 1200x630px
2. Importar tu logo actual
3. Añadir textos con tipografías Google Fonts (Poppins + Inter)
4. Exportar como JPG calidad 85%

#### Opción 2: Canva
1. Dimensiones personalizadas: 1200x630px
2. Usar plantilla "Facebook Post"
3. Ajustar textos y colores
4. Descargar como JPG

#### Opción 3: Photoshop/GIMP
1. Nuevo archivo 1200x630px, 72 DPI
2. Fondo con gradiente CSS traducido
3. Texto con fuentes instaladas
4. Guardar para web (JPG, calidad 80-85)

#### Opción 4: Código (Generación automática)
```python
# Opción avanzada: Generar con PIL/Pillow
from PIL import Image, ImageDraw, ImageFont

def generate_og_image():
    # Crear imagen base
    img = Image.new('RGB', (1200, 630), color='#1A1A1A')
    draw = ImageDraw.Draw(img)
    
    # Cargar fuentes (debes tener los .ttf instalados)
    font_title = ImageFont.truetype('Poppins-Bold.ttf', 48)
    font_subtitle = ImageFont.truetype('Inter-Regular.ttf', 32)
    
    # Dibujar textos
    draw.text((600, 200), 'Entrenador Personal + IA', 
              font=font_title, fill='#FFFFFF', anchor='mm')
    draw.text((600, 280), 'Análisis Biométrico Gratis', 
              font=font_subtitle, fill='#BDC3C7', anchor='mm')
    
    # Guardar
    img.save('static/images/og-image-cbf360.jpg', quality=85)

# TODO: Integrar en script de deployment
```

### Validación
Después de crear la imagen, verifica en:
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
- [Twitter Card Validator](https://cards-dev.twitter.com/validator)
- [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)

---

## 🔖 FAVICON PACK

### Archivos Necesarios

**1. favicon.ico** (Navegadores legacy)
- 16x16px + 32x32px (multi-resolución)
- Formato: ICO
- Ubicación: `/static/favicon.ico`

**2. favicon-16x16.png**
- 16x16px
- Formato: PNG-8
- Transparencia: Sí

**3. favicon-32x32.png**
- 32x32px
- Formato: PNG-8
- Transparencia: Sí

**4. apple-touch-icon.png**
- 180x180px
- Formato: PNG-24
- Fondo: Sólido (sin transparencia)
- Diseño: Logo centrado con padding

**5. site.webmanifest** (PWA)
```json
{
  "name": "CoachBodyFit360",
  "short_name": "CBF360",
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
  "display": "standalone"
}
```

### Generador Automático
Usa [RealFaviconGenerator](https://realfavicongenerator.net/):
1. Sube tu logo (mínimo 260x260px)
2. Configura colores (theme: #E74C3C)
3. Descarga el pack completo
4. Extrae en `/static/images/`

---

## 📊 CHECKLIST DE IMPLEMENTACIÓN

### Paso 1: Crear Imágenes
- [ ] og-image-cbf360.jpg (1200x630px)
- [ ] favicon.ico (16x16 + 32x32)
- [ ] favicon-16x16.png
- [ ] favicon-32x32.png
- [ ] apple-touch-icon.png (180x180px)
- [ ] android-chrome-192x192.png
- [ ] android-chrome-512x512.png

### Paso 2: Ubicar Archivos
```
static/
├── images/
│   ├── og-image-cbf360.jpg         ← Open Graph
│   ├── favicon-16x16.png
│   ├── favicon-32x32.png
│   ├── apple-touch-icon.png
│   ├── android-chrome-192x192.png
│   └── android-chrome-512x512.png
├── favicon.ico                      ← Raíz de static
└── site.webmanifest                 ← Raíz de static
```

### Paso 3: Validar
- [ ] Visitar tu site y verificar favicon en pestaña
- [ ] Compartir URL en WhatsApp → ver preview correcto
- [ ] Compartir URL en Facebook → ver preview correcto
- [ ] Validar en [Facebook Debugger](https://developers.facebook.com/tools/debug/)

---

## 🎯 IMPACTO ESPERADO

**Antes (sin Open Graph):**
```
Compartir en WhatsApp:
┌────────────────────────┐
│ coachbodyfit360.com    │  ← Solo URL, sin contexto
└────────────────────────┘
```

**Después (con Open Graph):**
```
Compartir en WhatsApp:
┌────────────────────────────────────┐
│ [Imagen llamativa 1200x630]        │
│                                    │
│ Entrenador Personal + IA          │
│ Análisis Biométrico Gratis...     │
│                                    │
│ coachbodyfit360.com                │
└────────────────────────────────────┘
```

**CTR en redes sociales: +300% a +500%** 🚀

---

## 📚 RECURSOS EXTERNOS

- [Open Graph Protocol](https://ogp.me/)
- [Twitter Card Docs](https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards)
- [Favicon Generator](https://realfavicongenerator.net/)
- [Image Compression](https://tinypng.com/)
- [OG Preview Tool](https://www.opengraph.xyz/)
