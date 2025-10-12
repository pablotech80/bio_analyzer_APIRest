BRIEFING COMPLETO PARA WINDSURF - CoachBodyFit360 Landing Rediseño
🎯 OBJETIVO DEL PROYECTO
Rediseñar completamente el landing page de CoachBodyFit360 para reflejar:

Experiencia real de 20 años en fitness (sin exponer titulaciones)
Metodología propia validada por resultados reales (Google Reviews 4.9★)
IA como herramienta que potencia la experiencia, no sustituye
Responsabilidad médica/legal delegada al usuario (disclaimers claros)


👤 IDENTIDAD DE MARCA
Propietario y Experiencia
Nombre: Pablo Techera
Años de experiencia: 20 años (2005-2025)
Marca propia: 10 años (2015-2025)
Clientes transformados: +500
Especialidades: Desde salud básica hasta fitness de competición
Valoración: 4.9★ en Google Reviews (127 reseñas verificadas)
Posicionamiento Estratégico
❌ NO ES: "Entrenador certificado" o "profesional titulado"
✅ ES: "Experto con 20 años de experiencia práctica"

❌ NO ES: "IA médica" o "diagnóstico automático"
✅ ES: "IA educativa basada en metodología probada"

MENSAJE CLAVE:
"Mi experiencia de 20 años + FitMaster AI = 
Tu plan personalizado disponible 24/7"
Estrategia Legal/Responsabilidad
DISCLAIMERS OBLIGATORIOS (destacados):

1. HERO SECTION:
   "Herramienta informativa y educativa. 
    No sustituye consulta médica profesional."

2. ANTES DEL REGISTRO:
   "CoachBodyFit360 es una herramienta educativa basada en 
    metodología fitness con 20 años de experiencia práctica.
    Consulta con un médico antes de iniciar cualquier programa."

3. FOOTER (visible):
   ⚠️ "Esta plataforma ofrece información general sobre fitness.
       No proporciona diagnóstico médico ni sustituye 
       la supervisión de profesionales sanitarios."

4. ENFOQUE EN RESULTADOS DE USUARIOS:
   "Basado en la experiencia de +500 personas que aplicaron 
    esta metodología bajo su propia responsabilidad."

🎨 IDENTIDAD VISUAL
Logo Existente
Archivo: logo CoachBodyFit
Elementos:
- Silueta atlética con barra
- Llama/fuego rojo-naranja (transformación)
- Texto circular: "STRONG · NOURISH · THE LIVE · ELEVATE"
- COACHBODYFIT en blanco, mayúsculas, bold

Colores del logo:
- Rojo/Naranja: #E74C3C / #E67E22
- Negro: #1A1A1A
- Gris: #BDC3C7
- Blanco: #FFFFFF
Paleta de Colores Definitiva
css:root {
    /* PRIMARIOS (del logo) */
    --primary-red:      #E74C3C;
    --primary-orange:   #E67E22;
    --primary-black:    #1A1A1A;
    
    /* SECUNDARIOS */
    --secondary-gray:   #BDC3C7;
    --secondary-dark:   #2C3E50;
    
    /* ACENTOS */
    --accent-success:   #27AE60;
    --accent-warning:   #F39C12;
    --accent-info:      #3498DB;
    
    /* NEUTRALES */
    --white:            #FFFFFF;
    --light-gray:       #ECF0F1;
    --dark-gray:        #34495E;
    
    /* GRADIENTES */
    --gradient-hero:    linear-gradient(135deg, #E74C3C 0%, #E67E22 100%);
    --gradient-dark:    linear-gradient(135deg, #1A1A1A 0%, #2C3E50 100%);
    --gradient-cta:     linear-gradient(135deg, #E67E22 0%, #F39C12 100%);
}
Tipografía
Headings:  'Poppins', sans-serif (bold, moderno)
Body:      'Inter', sans-serif (legible, profesional)
Números:   'Bebas Neue', sans-serif (impacto visual en stats)

Escala:
- Hero H1:    clamp(2.5rem, 5vw, 4rem)
- Section H2: clamp(2rem, 4vw, 3rem)
- Body:       1.125rem (18px)

🏗️ ESTRUCTURA DEL LANDING
1. HERO SECTION
LAYOUT:
┌────────────────────────────────────────────────┐
│ [Fondo: Negro con textura sutil]               │
│                                                │
│ [Logo CoachBodyFit centrado arriba - 100px]   │
│                                                │
│ [Badge: ⭐ 4.9 · 127 reseñas · 20 años exp.]  │
│                                                │
│ H1 (blanco, grande):                          │
│ TU METODOLOGÍA FITNESS                         │
│ CON 20 AÑOS DE EXPERIENCIA                    │
│ [Gradiente rojo en "20 AÑOS"]                 │
│                                                │
│ Subtítulo (gris claro):                       │
│ Más de 500 personas han transformado su       │
│ cuerpo aplicando esta metodología.            │
│ Ahora potenciada con FitMaster IA.            │
│                                                │
│ [CTA Primario - Rojo gradiente, grande]:      │
│ 🔥 Comenzar Mi Análisis Gratis                │
│                                                │
│ [CTA Secundario - Outline rojo]:              │
│ 📊 Ver Casos de Éxito Reales                  │
│                                                │
│ [Trust Badges horizontales]:                   │
│ ✓ Sin tarjeta  ✓ 60 segundos  ✓ 100% Gratis  │
│                                                │
│ [Disclaimer pequeño pero visible]:             │
│ ⚠️ Herramienta educativa. No sustituye        │
│    consulta médica profesional.               │
└────────────────────────────────────────────────┘

ANIMACIÓN:
- Fade-in suave del logo (0.5s)
- Texto aparece de abajo hacia arriba (0.8s)
- CTAs con efecto hover: translateY(-3px) + shadow

2. STATS BAR
LAYOUT (fondo rojo gradiente, texto blanco):
┌────────────────────────────────────────────────┐
│  20 AÑOS       │  500+         │  4.9★        │
│  Experiencia   │  Clientes     │  Google      │
│                │  Reales       │  Reviews     │
└────────────────────────────────────────────────┘

DISEÑO:
- 4 columnas en desktop, stack en mobile
- Números grandes (3rem) con Bebas Neue
- Texto pequeño debajo (0.875rem)
- Separadores verticales entre columnas

3. LOS 4 PILARES (basado en logo)
SECCIÓN: "Los 4 Pilares de la Metodología"
Fondo: Negro oscuro (#1A1A1A)

Grid 4 columnas:

┌──────────────────────────────────────────────────┐
│  [Icono] 💪                                      │
│  STRONG                                          │
│  Rutinas personalizadas según tu composición    │
│  corporal y objetivos específicos.              │
│                                                  │
│  Color: Rojo (#E74C3C)                          │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│  [Icono] 🍎                                      │
│  NOURISH                                         │
│  Planes nutricionales con 5 comidas diarias     │
│  y macros adaptados a tu metabolismo.           │
│                                                  │
│  Color: Verde (#27AE60)                         │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│  [Icono] ❤️                                      │
│  LIVE                                            │
│  Seguimiento continuo con métricas biométricas  │
│  profesionales (IMC, FFMI, % grasa, etc).       │
│                                                  │
│  Color: Rojo (#E74C3C)                          │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│  [Icono] 📈                                      │
│  ELEVATE                                         │
│  IA que aprende de tus respuestas y ajusta      │
│  el plan automáticamente.                       │
│                                                  │
│  Color: Naranja (#E67E22)                       │
└──────────────────────────────────────────────────┘

INTERACCIÓN:
- Hover en cada card: scale(1.05) + glow effect
- Iconos animados al hacer scroll (bounce)

4. EXPERIENCIA Y METODOLOGÍA
SECCIÓN: "20 Años de Experiencia Aplicada"
Fondo: Blanco

LAYOUT (2 columnas):

IZQUIERDA:
┌────────────────────────────────────┐
│  [Icono grande de medalla/trofeo]  │
│  Diseño minimalista, rojo          │
└────────────────────────────────────┘

DERECHA (texto):
┌────────────────────────────────────────────────┐
│ H2: Mi Experiencia, Tu Transformación         │
│                                                │
│ Soy Pablo Techera, y durante 20 años he       │
│ trabajado con más de 500 personas ayudándolas │
│ a alcanzar sus objetivos:                     │
│                                                │
│ ✓ Desde personas que buscan mejorar su salud  │
│   básica y perder peso                        │
│                                                │
│ ✓ Hasta atletas que compiten y necesitan      │
│   optimización de rendimiento                 │
│                                                │
│ ✓ Cada cuerpo es diferente, cada objetivo     │
│   es único. Esa es la base de mi metodología  │
│                                                │
│ CoachBodyFit360 es la evolución natural:      │
│ mi experiencia práctica validada por          │
│ resultados reales + tecnología IA que         │
│ personaliza TODO específicamente para ti.     │
│                                                │
│ [Blockquote con borde rojo]:                  │
│ "No soy médico ni nutricionista. Soy un      │
│  experto en fitness con 20 años aplicando     │
│  y perfeccionando una metodología que         │
│  funciona. Los resultados de mis clientes     │
│  hablan por sí mismos."                       │
└────────────────────────────────────────────────┘

DISCLAIMER al final de esta sección:
⚠️ Esta metodología está basada en experiencia 
   práctica, no en titulación médica. Consulta 
   con profesionales sanitarios antes de iniciar
   cualquier programa.

5. COMPARACIÓN DE VALOR
SECCIÓN: "El Valor de la Experiencia, Accesible"
Fondo: Gris claro (#ECF0F1)

TABLA VISUAL (2 columnas):

┌─────────────────────────────────────────────────┐
│  Entrenador Personal      CoachBodyFit360       │
│  Presencial                                     │
├─────────────────────────────────────────────────┤
│  €80-120 por sesión       GRATIS (Freemium)    │
│  1-2 veces/semana         24/7 disponible       │
│  Horario fijo             Sin horarios          │
│  Plan genérico            IA + 20 años exp.     │
│  Sin seguimiento          Métricas en tiempo    │
│  Mediciones básicas       15+ métricas pro      │
└─────────────────────────────────────────────────┘

DISEÑO:
- Columna izquierda: fondo blanco, check marks grises
- Columna derecha: fondo rojo suave, check marks verdes
- Bordes redondeados, sombras sutiles

6. GOOGLE REVIEWS
SECCIÓN: "Transformaciones Reales, Reseñas Verificadas"
Fondo: Blanco

H2: Lo que dicen quienes aplicaron esta metodología

[Widget de Google Reviews integrado]
URL: https://www.google.com/search?q=coachbodyfit+opiniones

CARRUSEL DE TESTIMONIOS (3 cards visibles):

┌─────────────────────────────────────────┐
│  [Avatar Google]  María González        │
│  ⭐⭐⭐⭐⭐           Hace 2 meses       │
│  ✓ Reseña verificada                   │
│                                         │
│  "La metodología de Pablo funciona.     │
│   Perdí 12kg siguiendo sus planes       │
│   personalizados. Lo mejor es que       │
│   puedo consultarle cuando tengo dudas  │
│   a través de la IA."                   │
│                                         │
│  [Badge] Perdió 12kg en 4 meses        │
└─────────────────────────────────────────┘

[Botón CTA]:
📱 Ver las 127 reseñas en Google →

IMPORTANTE:
- Enlace directo real a Google Reviews
- Solo mostrar reseñas verificadas (con check)
- No inventar testimonios, usar reales de Google

7. PROCESO SIMPLE
SECCIÓN: "Cómo Funciona"
Fondo: Negro con textura

3 PASOS CON TIMELINE VISUAL:

┌────────────────────────────────────────┐
│  [1]  Regístrate Gratis                │
│   ↓   30 segundos, sin tarjeta         │
│  [2]  Análisis Biométrico              │
│   ↓   Introduce tus medidas (60s)      │
│  [3]  Recibe tu Plan                   │
│       IA + Experiencia = Personalizado │
└────────────────────────────────────────┘

DISEÑO:
- Números en círculos rojos con gradiente
- Línea vertical conectando los 3 pasos
- Iconos ilustrativos para cada paso
- Tiempo estimado debajo de cada uno

8. FEATURES DETALLADOS
SECCIÓN: "Qué Obtienes Exactamente"
Fondo: Blanco

Grid 3 columnas:

ANÁLISIS COMPLETO:
┌────────────────────────────┐
│ [Icono gráfica]            │
│ 15+ Métricas Biométricas   │
│                            │
│ • IMC y clasificación      │
│ • % Grasa corporal (Navy)  │
│ • Masa magra y FFMI        │
│ • Edad metabólica          │
│ • Peso ideal               │
│ • Requerimientos calóricos │
│ • Y mucho más...           │
└────────────────────────────┘

PLAN NUTRICIONAL:
┌────────────────────────────┐
│ [Icono comida]             │
│ 5 Comidas Personalizadas   │
│                            │
│ • Desayuno, snacks, comida │
│ • Macros calculados        │
│ • Opciones intercambiables │
│ • Adaptado a tus objetivos │
│ • Actualización automática │
└────────────────────────────┘

RUTINA ENTRENAMIENTO:
┌────────────────────────────┐
│ [Icono pesas]              │
│ Ejercicios Específicos     │
│                            │
│ • Series y repeticiones    │
│ • Descansos optimizados    │
│ • Progresión semanal       │
│ • Adaptado a tu nivel      │
│ • Videos explicativos      │
└────────────────────────────┘

9. FAQ ANTICIPANDO OBJECIONES
SECCIÓN: "Preguntas Frecuentes"
Fondo: Gris claro

ACCORDION BOOTSTRAP:

Q: ¿Es esto un sustituto de un médico o nutricionista?
A: No. CoachBodyFit360 es una herramienta educativa 
   basada en 20 años de experiencia práctica en fitness.
   Siempre debes consultar con profesionales sanitarios
   antes de iniciar cualquier programa de ejercicio o dieta.

Q: ¿Pablo Techera es un profesional certificado?
A: Pablo tiene 20 años de experiencia práctica trabajando
   con +500 personas en transformación física. La plataforma
   ofrece metodología basada en esa experiencia, no en
   titulación académica. Tú decides si aplicar esta
   información bajo tu propia responsabilidad.

Q: ¿Cómo funciona la IA?
A: FitMaster IA aplica la metodología desarrollada durante
   20 años, personalizándola con tus datos específicos.
   No es IA médica ni diagnóstica, es educativa.

Q: ¿Es realmente gratis?
A: Sí. El análisis biométrico y plan básico son 100% gratis.
   En el futuro habrá funciones premium opcionales.

Q: ¿Mis datos están seguros?
A: Sí. Usamos encriptación y cumplimos con GDPR.
   Nunca vendemos ni compartimos datos personales.

Q: ¿Puedo cancelar cuando quiera?
A: Sí, sin preguntas. Tus datos permanecen disponibles
   mientras quieras mantener tu cuenta.

10. CTA FINAL
SECCIÓN: [Fondo gradiente rojo-naranja]
Texto: Blanco

H2 (grande, centrado):
¿Listo Para Aplicar 20 Años de Experiencia
a Tu Transformación?

Párrafo:
Únete a las +500 personas que ya han transformado
su cuerpo aplicando esta metodología probada.

[CTA MUY GRANDE - Blanco con sombra]:
🔥 Comenzar Mi Análisis Gratis

[Texto pequeño debajo]:
✓ Sin tarjeta de crédito
✓ Resultados en 60 segundos
✓ 100% Gratis siempre

[Link]:
¿Ya tienes cuenta? Inicia Sesión →

[Disclaimer obligatorio]:
⚠️ Herramienta educativa e informativa.
   Consulta con profesionales médicos antes
   de iniciar cualquier programa.

11. FOOTER
DISEÑO: Fondo negro (#1A1A1A), texto gris claro

4 COLUMNAS:

COLUMNA 1: Marca
┌────────────────────────────┐
│ [Logo pequeño 60px]        │
│ CoachBodyFit360            │
│                            │
│ Metodología fitness con    │
│ 20 años de experiencia     │
│ potenciada por IA.         │
│                            │
│ [Iconos redes sociales]    │
└────────────────────────────┘

COLUMNA 2: Navegación
- Inicio
- Cómo Funciona
- Casos de Éxito
- Preguntas Frecuentes
- Sobre la Metodología

COLUMNA 3: Legal
- Política de Privacidad
- Términos y Condiciones
- Política de Cookies
- Aviso Legal

COLUMNA 4: Contacto
- Email: contacto@coachbodyfit360.com
- Reseñas Google
- Soporte

SEPARADOR

FOOTER BOTTOM (centrado):
© 2025 CoachBodyFit360. Todos los derechos reservados.

⚠️ DISCLAIMER LEGAL (obligatorio, destacado):
Esta plataforma ofrece información educativa sobre 
fitness basada en experiencia práctica de 20 años.
No proporciona diagnóstico médico, asesoramiento 
nutricional profesional ni sustituye la supervisión
de profesionales sanitarios titulados. Consulta con
un médico antes de iniciar cualquier programa de
ejercicio o cambio nutricional. Al usar esta 
plataforma, aceptas hacerlo bajo tu propia 
responsabilidad.

🎨 COMPONENTES Y EFECTOS
Botones
PRIMARIO (CTA principal):
- Background: gradient(#E67E22, #F39C12)
- Color: white
- Padding: 1rem 2.5rem
- Border-radius: 8px
- Font-weight: 600
- Shadow: 0 10px 30px rgba(230, 126, 34, 0.3)
- Hover: translateY(-3px) + shadow increase

SECUNDARIO (CTA secundario):
- Background: transparent
- Border: 2px solid #E74C3C
- Color: #E74C3C (o white si fondo oscuro)
- Hover: background #E74C3C, color white
Cards
ESTILO GENERAL:
- Background: white
- Border-radius: 12px
- Padding: 2rem
- Box-shadow: 0 5px 15px rgba(0,0,0,0.08)
- Transition: all 0.3s ease

HOVER:
- Transform: translateY(-10px)
- Box-shadow: 0 15px 40px rgba(0,0,0,0.15)
- (Solo en features, no en testimonios)
Animaciones
SCROLL ANIMATIONS (Intersection Observer):
- Fade-in-up para secciones
- Counter animation para números stats
- Stagger effect en grids (delay incremental)

HOVER EFFECTS:
- Buttons: scale(1.05) + shadow
- Cards: translateY(-10px)
- Links: underline con color primario

📱 RESPONSIVE
Breakpoints
Mobile:     < 576px
Tablet:     576px - 991px
Desktop:    > 992px

AJUSTES MOBILE:
- Hero H1: 2.5rem (vs 4rem desktop)
- Stats bar: stack vertical
- 4 Pilares: stack vertical
- Comparación tabla: stack vertical con tabs
- Footer: stack todas columnas

🔧 TECNOLOGÍAS
Stack Requerido
- Framework: Bootstrap 5.3
- Iconos: Bootstrap Icons (no Font Awesome)
- Tipografía: Google Fonts (Poppins + Inter)
- Animaciones: Intersection Observer API (vanilla JS)
- No jQuery
Archivos a Modificar
templates/
  └── index.html (o landing.html)

static/
  ├── css/
  │   └── landing.css (nuevo, estilos custom)
  ├── js/
  │   └── landing.js (nuevo, animaciones)
  └── images/
      └── logo-coachbodyfit.png (logo existente)

⚖️ DISCLAIMERS Y LEGALIDAD
Ubicaciones Obligatorias
1. HERO (siempre visible):
   "⚠️ Herramienta educativa. No sustituye consulta médica."

2. ANTES DE REGISTRO (modal o página):
   [Checkbox obligatorio]:
   "☐ Entiendo que CoachBodyFit360 es una herramienta 
       educativa basada en experiencia práctica, no en
       titulación médica. Consultaré con un profesional
       sanitario antes de aplicar cualquier recomendación."

3. FOOTER (siempre visible):
   Disclaimer completo legal

4. TÉRMINOS Y CONDICIONES (página dedicada):
   Sección completa sobre limitación de responsabilidad
Tono del Mensaje
❌ EVITAR:
- "Diagnóstico"
- "Prescripción"
- "Tratamiento"
- "Médico", "Doctor"
- "Certificado profesional"
- "Garantizamos resultados"

✅ USAR:
- "Metodología basada en experiencia"
- "Herramienta educativa"
- "Plan personalizado informativo"
- "Experto con 20 años de práctica"
- "Resultados reales de usuarios"
- "Bajo tu propia responsabilidad"

📊 MÉTRICAS Y OBJETIVOS
KPIs a Mejorar
ACTUAL → OBJETIVO

Bounce Rate:        ~65% → <40%
Time on Page:       ~45s → >90s
Scroll Depth:       ~40% → >70%
Click Hero CTA:     ~2%  → >5%
Conversion Sign-up: ~0.5% → >2%
A/B Testing Futuro
Variables a testear:
- Copy del Hero (variaciones de "20 años")
- Ubicación de Google Reviews (arriba vs abajo)
- CTA wording ("Comenzar" vs "Analizar" vs "Probar")
- Presencia/ausencia de countdown timer

✅ CHECKLIST DE IMPLEMENTACIÓN
FASE 1: Estructura y Contenido
☐ Copiar todo este briefing a Windsurf
☐ Crear templates/landing.html
☐ Implementar estructura HTML completa
☐ Todos los disclaimers en su sitio
☐ Integrar logo existente

FASE 2: Estilos
☐ Crear static/css/landing.css
☐ Implementar paleta de colores
☐ Tipografía Google Fonts
☐ Componentes (buttons, cards, etc)
☐ Responsive breakpoints

FASE 3: Interactividad
☐ Crear static/js/landing.js
☐ Scroll animations (Intersection Observer)
☐ Counter animations en stats
☐ Smooth scroll a secciones
☐ Carrusel de testimonios

FASE 4: Integraciones
☐ Widget Google Reviews
☐ Enlaces a rutas Flask correctas
☐ Forms con CSRF token
☐ Analytics tracking (opcional)

FASE 5: Testing
☐ Test responsive (móvil, tablet, desktop)
☐ Test cross-browser (Chrome, Firefox, Safari)
☐ Test velocidad (Lighthouse)
☐ Test accesibilidad (WAVE)
☐ Validación HTML/CSS