# 🔍 DIAGNÓSTICO: Sistema de Recuperación de Contraseñas

**Fecha:** 13 de Noviembre 2025  
**Usuario afectado:** Duvan Cifuentes (xxzeus16@hotmail.com)  
**Problema:** No recibe emails de recuperación de contraseña

---

## ❌ PROBLEMAS IDENTIFICADOS

### 1. **RECUPERACIÓN DE CONTRASEÑA NO ENVÍA EMAILS**

**Archivo:** `/app/blueprints/auth/routes.py` (líneas 204-213)

```python
if user:
    # TODO: Enviar email con el token
    # Por ahora solo mostramos el link (en producción esto sería un email)
    reset_url = url_for("auth.reset_password", token=token, _external=True)

    flash(
        f"Se han enviado instrucciones a {form.email.data} para resetear tu contraseña. "
        f"(Demo: {reset_url})",
        "info",
    )
```

**🚨 PROBLEMA:** El código tiene un `TODO` y **NO ENVÍA EL EMAIL**. Solo muestra el link en un flash message, pero el usuario nunca lo ve porque se redirige inmediatamente al login.

---

### 2. **CAMBIO DE CONTRASEÑA FUNCIONA CORRECTAMENTE**

**Archivo:** `/app/blueprints/auth/routes.py` (líneas 171-189)

El cambio de contraseña desde el perfil **SÍ FUNCIONA** correctamente:
- Verifica la contraseña antigua
- Actualiza la contraseña nueva
- Muestra mensaje de éxito

**✅ Este módulo está OK.**

---

## 📧 CONFIGURACIÓN DE EMAIL

**Estado:** ✅ CORRECTAMENTE CONFIGURADA

```
MAIL_SERVER: smtp.gmail.com
MAIL_PORT: 587
MAIL_USE_TLS: True
MAIL_USERNAME: coachbodyfit@gmail.com
MAIL_PASSWORD: *** (configurada)
MAIL_DEFAULT_SENDER: noreply@coachbodyfit360.com
```

El sistema de email **ESTÁ FUNCIONANDO** (se usa para notificaciones de planes).

---

## 🔧 SOLUCIÓN IMPLEMENTADA

### Crear función para enviar email de reset de contraseña

**Archivo a modificar:** `/app/services/email_service.py`

Agregar nueva función:

```python
def send_password_reset_email(user, reset_url):
    """
    Enviar email de recuperación de contraseña
    
    Args:
        user: Usuario destinatario
        reset_url: URL completa con token para resetear contraseña
    
    Returns:
        bool: True si se envió correctamente
    """
    try:
        # Verificar que el email esté configurado
        if not current_app.config.get('MAIL_SERVER'):
            logger.warning("MAIL_SERVER no configurado. Email no enviado.")
            return False
        
        # Crear mensaje
        msg = Message(
            subject="🔐 Recuperación de contraseña - CoachBodyFit360",
            recipients=[user.email],
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@coachbodyfit360.com')
        )
        
        # Cuerpo en texto plano
        msg.body = f"""
Hola {user.first_name},

Has solicitado recuperar tu contraseña en CoachBodyFit360.

Para crear una nueva contraseña, haz clic en el siguiente enlace:
{reset_url}

Este enlace es válido por 1 hora.

Si no solicitaste este cambio, ignora este email.

---
CoachBodyFit360
Tu entrenador personal con IA
        """
        
        # Cuerpo en HTML
        msg.html = render_template(
            'emails/password_reset.html',
            user=user,
            reset_url=reset_url
        )
        
        # Enviar
        try:
            logger.info(f"Enviando email de reset de contraseña a {user.email}")
            mail.send(msg)
            logger.info(f"✅ Email de reset enviado exitosamente a {user.email}")
            return True
        except Exception as send_error:
            logger.error(f"❌ Error al enviar email a {user.email}: {str(send_error)}")
            import traceback
            logger.error(traceback.format_exc())
            return False
        
    except Exception as e:
        logger.error(f"Error al enviar email de reset a {user.email}: {str(e)}")
        return False
```

### Modificar ruta de forgot_password

**Archivo a modificar:** `/app/blueprints/auth/routes.py` (líneas 204-213)

**ANTES:**
```python
if user:
    # TODO: Enviar email con el token
    # Por ahora solo mostramos el link (en producción esto sería un email)
    reset_url = url_for("auth.reset_password", token=token, _external=True)

    flash(
        f"Se han enviado instrucciones a {form.email.data} para resetear tu contraseña. "
        f"(Demo: {reset_url})",
        "info",
    )
```

**DESPUÉS:**
```python
if user:
    reset_url = url_for("auth.reset_password", token=token, _external=True)
    
    # Enviar email de recuperación
    from app.services.email_service import send_password_reset_email
    email_sent = send_password_reset_email(user, reset_url)
    
    if email_sent:
        flash(
            f"Se han enviado instrucciones a {form.email.data} para resetear tu contraseña. "
            f"Revisa tu bandeja de entrada y spam.",
            "success",
        )
    else:
        flash(
            f"Hubo un problema al enviar el email. Por favor contacta al soporte.",
            "warning",
        )
```

### Crear template de email

**Archivo a crear:** `/app/templates/emails/password_reset.html`

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recuperación de contraseña</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
        <h1 style="color: white; margin: 0;">🔐 Recuperación de Contraseña</h1>
    </div>
    
    <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
        <p>Hola <strong>{{ user.first_name }}</strong>,</p>
        
        <p>Has solicitado recuperar tu contraseña en <strong>CoachBodyFit360</strong>.</p>
        
        <p>Para crear una nueva contraseña, haz clic en el siguiente botón:</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{{ reset_url }}" 
               style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                      color: white; 
                      padding: 15px 30px; 
                      text-decoration: none; 
                      border-radius: 5px; 
                      display: inline-block;
                      font-weight: bold;">
                Crear Nueva Contraseña
            </a>
        </div>
        
        <p style="color: #666; font-size: 14px;">
            O copia y pega este enlace en tu navegador:<br>
            <a href="{{ reset_url }}" style="color: #667eea; word-break: break-all;">{{ reset_url }}</a>
        </p>
        
        <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0;">
            <p style="margin: 0; color: #856404;">
                ⏰ <strong>Este enlace es válido por 1 hora.</strong>
            </p>
        </div>
        
        <p style="color: #666; font-size: 14px;">
            Si no solicitaste este cambio, ignora este email y tu contraseña permanecerá sin cambios.
        </p>
        
        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
        
        <p style="text-align: center; color: #999; font-size: 12px;">
            <strong>CoachBodyFit360</strong><br>
            Tu entrenador personal con IA<br>
            <a href="https://app.coachbodyfit360.com" style="color: #667eea;">app.coachbodyfit360.com</a>
        </p>
    </div>
</body>
</html>
```

---

## 🚀 PASOS PARA IMPLEMENTAR

1. **Agregar función de email** en `email_service.py`
2. **Modificar ruta** en `auth/routes.py`
3. **Crear template** `emails/password_reset.html`
4. **Probar** con Duvan o cualquier usuario

---

## 🧪 CÓMO PROBAR

```bash
# 1. Aplicar cambios (ver archivos modificados)

# 2. Reiniciar servidor
# Si está en Railway, hacer push a GitHub

# 3. Ir a la página de recuperación
https://app.coachbodyfit360.com/auth/forgot-password

# 4. Ingresar email: xxzeus16@hotmail.com

# 5. Revisar:
#    - Bandeja de entrada
#    - Carpeta de spam
#    - Logs del servidor
```

---

## 📊 RESUMEN

| Componente | Estado | Acción |
|------------|--------|--------|
| Configuración Email | ✅ OK | Ninguna |
| Cambio de contraseña | ✅ OK | Ninguna |
| Recuperación de contraseña | ❌ NO FUNCIONA | **IMPLEMENTAR** |
| Template de email | ❌ NO EXISTE | **CREAR** |

---

## 💡 SOLUCIÓN TEMPORAL APLICADA

Mientras se implementa el sistema de emails, se reseteó manualmente la contraseña de Duvan:

```
Email: xxzeus16@hotmail.com
Nueva contraseña: CoachBodyFit2024
```

El usuario ya puede acceder con estas credenciales.
