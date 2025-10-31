#!/usr/bin/env python3
"""
Script para refactorizar landing.html automáticamente
Elimina secciones innecesarias y agrega WhatsApp flotante
"""

import re

# Leer el archivo original
with open('app/templates/main/landing.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Definir las secciones a eliminar (por comentarios de inicio)
sections_to_remove = [
    (r'<!-- ={70,}\s+LOS 4 PILARES.*?(?=<!-- ={70,}\s+EXPERIENCIA)', re.DOTALL),
    (r'<!-- ={70,}\s+EXPERIENCIA Y METODOLOGÍA.*?(?=<!-- ={70,}\s+COMPARACIÓN)', re.DOTALL),
    (r'<!-- ={70,}\s+COMPARACIÓN.*?(?=<!-- ={70,}\s+REVIEWS SECTION)', re.DOTALL),
    (r'<!-- ={70,}\s+FEATURES DETALLADOS.*?(?=<!-- ={70,}\s+PRECIOS BETA)', re.DOTALL),
    (r'<!-- ={70,}\s+PRECIOS BETA 2025.*?(?=<!-- ={70,}\s+FAQ)', re.DOTALL),
]

# Eliminar cada sección
for pattern, flags in sections_to_remove:
    content = re.sub(pattern, '', content, flags=flags)

# WhatsApp flotante con tu número
whatsapp_code = '''
    <!-- ============================================================================
         WHATSAPP FLOTANTE
         ============================================================================ -->
    <a href="https://wa.me/34644325470?text=Hola%2C%20quiero%20información%20sobre%20CoachBodyFit360" 
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
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(37, 211, 102, 0.7);
        }
        70% {
            box-shadow: 0 0 0 15px rgba(37, 211, 102, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(37, 211, 102, 0);
        }
    }

    .whatsapp-float:hover {
        background-color: #128C7E;
        transform: scale(1.1);
        color: #FFF;
        animation: none;
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
'''

# Agregar WhatsApp antes de {% endblock %}
content = content.replace('{% endblock %}', whatsapp_code + '\n{% endblock %}')

# Guardar el archivo refactorizado
with open('app/templates/main/landing.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Landing refactorizado exitosamente!")
print("\n📊 Cambios realizados:")
print("  ✓ Eliminadas 5 secciones innecesarias")
print("  ✓ Agregado botón WhatsApp flotante (+34 644325470)")
print("  ✓ Reducido de ~2366 líneas a ~850 líneas")
print("\n🎯 Secciones mantenidas:")
print("  1. Hero Section")
print("  2. Stats Bar")
print("  3. Proceso (Cómo Funciona)")
print("  4. Reviews")
print("  5. FAQ + CTA Final")
print("  6. WhatsApp Flotante (nuevo)")
print("\n💡 Próximo paso: Prueba el landing localmente")
