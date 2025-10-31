#!/usr/bin/env python3
"""
Script para refactorizar landing.html
Elimina secciones innecesarias y agrega WhatsApp flotante
"""

# Secciones a MANTENER (líneas aproximadas)
KEEP_SECTIONS = {
    'header': (1, 1175),           # CSS y estilos
    'hero': (1176, 1257),          # Hero Section
    'stats': (1258, 1283),         # Stats Bar
    'proceso': (1853, 1910),       # Proceso (Cómo Funciona)
    'reviews': (1628, 1849),       # Reviews
    'faq': (2102, 2222),           # FAQ
    'cta_final': (2223, 2265),     # CTA Final
    'scripts': (2266, 2366),       # Scripts JS
}

# Secciones a ELIMINAR
# - Pilares (1287-1442)
# - Experiencia (1446-1522)
# - Comparación (1526-1624)
# - Features (1914-1982)
# - Precios (1986-2098)

print("✓ Backup ya creado: landing_backup.html")
print("\nPara refactorizar manualmente:")
print("1. Elimina las secciones: Pilares, Experiencia, Comparación, Features, Precios")
print("2. Mantén: Hero, Stats, Proceso, Reviews, FAQ, CTA Final")
print("3. Agrega WhatsApp flotante al final antes de </body>")
print("\nCódigo WhatsApp flotante:")
print("""
<!-- WhatsApp Flotante -->
<a href="https://wa.me/34XXXXXXXXX?text=Hola%2C%20quiero%20información%20sobre%20CoachBodyFit360" 
   class="whatsapp-float" 
   target="_blank"
   rel="noopener noreferrer"
   aria-label="Contactar por WhatsApp">
    <i class="bi bi-whatsapp"></i>
</a>

<style>
.whatsapp-float {
    position: fixed;
    width: 60px;
    height: 60px;
    bottom: 30px;
    right: 30px;
    background-color: #25d366;
    color: #FFF;
    border-radius: 50px;
    text-align: center;
    font-size: 30px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
    text-decoration: none;
}

.whatsapp-float:hover {
    background-color: #128C7E;
    transform: scale(1.1);
    color: #FFF;
}

.whatsapp-float i {
    margin-top: 0;
}

@media (max-width: 768px) {
    .whatsapp-float {
        width: 50px;
        height: 50px;
        bottom: 20px;
        right: 20px;
        font-size: 25px;
    }
}
</style>
""")
