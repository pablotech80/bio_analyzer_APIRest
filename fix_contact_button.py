#!/usr/bin/env python3
"""
Script para reemplazar WhatsApp por botón de Email
"""

import re

# Leer el archivo
with open('app/templates/main/landing.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Patrón para eliminar TODAS las secciones de WhatsApp (incluyendo estilos)
whatsapp_pattern = r'<!-- ={70,}\s+WHATSAPP FLOTANTE\s+={70,} -->.*?</style>'

# Eliminar todas las ocurrencias de WhatsApp
content = re.sub(whatsapp_pattern, '', content, flags=re.DOTALL)

# Botón de email profesional
email_button = '''    <!-- ============================================================================
         BOTÓN CONTACTO FLOTANTE
         ============================================================================ -->
    <a href="mailto:contacto@coachbodyfit360.com?subject=Consulta%20desde%20CoachBodyFit360&body=Hola%2C%0A%0AMe%20gustaría%20obtener%20más%20información%20sobre%20CoachBodyFit360.%0A%0AGracias." 
       class="contact-float" 
       target="_blank"
       rel="noopener noreferrer"
       aria-label="Contactar por Email"
       title="Enviar Email">
        <i class="bi bi-envelope-fill"></i>
    </a>

    <style>
    .contact-float {
        position: fixed;
        width: 60px;
        height: 60px;
        bottom: 30px;
        right: 30px;
        background: linear-gradient(135deg, #E74C3C 0%, #E67E22 100%);
        color: #FFF;
        border-radius: 50px;
        text-align: center;
        font-size: 28px;
        box-shadow: 0 4px 15px rgba(231, 76, 60, 0.4);
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
            box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.7);
        }
        70% {
            box-shadow: 0 0 0 15px rgba(231, 76, 60, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(231, 76, 60, 0);
        }
    }

    .contact-float:hover {
        background: linear-gradient(135deg, #C0392B 0%, #D35400 100%);
        transform: scale(1.1);
        color: #FFF;
        animation: none;
        box-shadow: 0 6px 20px rgba(231, 76, 60, 0.6);
    }

    .contact-float i {
        margin-top: 0;
    }

    @media (max-width: 768px) {
        .contact-float {
            width: 50px;
            height: 50px;
            bottom: 20px;
            right: 20px;
            font-size: 22px;
        }
    }
    </style>
'''

# Agregar botón de email antes de {% endblock %}
content = content.replace('{% endblock %}', email_button + '\n{% endblock %}')

# Guardar
with open('app/templates/main/landing.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ WhatsApp reemplazado por botón de Email!")
print("\n📧 Email configurado: contacto@coachbodyfit360.com")
print("🎨 Botón flotante con gradiente rojo (colores de la marca)")
print("✨ Animación pulse para llamar la atención")
print("\n💡 El botón abre el cliente de email con:")
print("   - Destinatario: contacto@coachbodyfit360.com")
print("   - Asunto: Consulta desde CoachBodyFit360")
print("   - Cuerpo: Mensaje pre-llenado")
