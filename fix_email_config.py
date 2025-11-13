#!/usr/bin/env python3
"""
Script para diagnosticar y sugerir corrección de configuración de email
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("="*70)
print("🔍 DIAGNÓSTICO: Configuración de Email")
print("="*70)

mail_server = os.environ.get("MAIL_SERVER")
mail_port = os.environ.get("MAIL_PORT")
mail_use_tls = os.environ.get("MAIL_USE_TLS")
mail_use_ssl = os.environ.get("MAIL_USE_SSL")
mail_username = os.environ.get("MAIL_USERNAME")
mail_password = os.environ.get("MAIL_PASSWORD")

print("\n📋 Configuración actual en .env:")
print(f"   MAIL_SERVER={mail_server}")
print(f"   MAIL_PORT={mail_port}")
print(f"   MAIL_USE_TLS={mail_use_tls}")
print(f"   MAIL_USE_SSL={mail_use_ssl}")
print(f"   MAIL_USERNAME={mail_username}")
print(f"   MAIL_PASSWORD={'***' if mail_password else 'NO CONFIGURADO'}")

print("\n" + "="*70)
print("❌ PROBLEMA DETECTADO")
print("="*70)

if mail_port == "587":
    print("\n🔴 Puerto 587 requiere TLS (NO SSL)")
    print("\n   Configuración actual:")
    print(f"   - MAIL_PORT=587")
    print(f"   - MAIL_USE_TLS={mail_use_tls}")
    print(f"   - MAIL_USE_SSL={mail_use_ssl if mail_use_ssl else 'NO DEFINIDO (default: True)'}")
    
    print("\n   ❌ Problema: MAIL_USE_SSL está activado (o no definido)")
    print("   Con puerto 587, DEBE usar TLS y NO SSL")
    
    print("\n" + "="*70)
    print("✅ SOLUCIÓN")
    print("="*70)
    
    print("\nAgrega esta línea a tu archivo .env:")
    print("\n   MAIL_USE_SSL=False")
    
    print("\n📝 Tu configuración .env debe quedar así:")
    print("""
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False          <--- AGREGAR ESTA LÍNEA
MAIL_USERNAME=coachbodyfit@gmail.com
MAIL_PASSWORD=tqgzdouiczewecgh
MAIL_DEFAULT_SENDER=noreply@coachbodyfit360.com
    """)
    
elif mail_port == "465":
    print("\n🔵 Puerto 465 requiere SSL (NO TLS)")
    print("\n   Configuración recomendada:")
    print("""
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=465
MAIL_USE_TLS=False
MAIL_USE_SSL=True
MAIL_USERNAME=coachbodyfit@gmail.com
MAIL_PASSWORD=tu_app_password
MAIL_DEFAULT_SENDER=noreply@coachbodyfit360.com
    """)

print("\n" + "="*70)
print("📚 REFERENCIA")
print("="*70)
print("""
Gmail SMTP tiene 2 configuraciones posibles:

Opción 1 (RECOMENDADA - TLS):
  MAIL_PORT=587
  MAIL_USE_TLS=True
  MAIL_USE_SSL=False

Opción 2 (SSL):
  MAIL_PORT=465
  MAIL_USE_TLS=False
  MAIL_USE_SSL=True

⚠️  NO puedes usar TLS y SSL al mismo tiempo.
""")

print("="*70)
print("\n💡 Después de corregir el .env, ejecuta:")
print("   python test_email_send.py ptecherasosa@icloud.com")
print("="*70)
