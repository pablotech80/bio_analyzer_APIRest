# 📧 Sistema de Notificaciones - Guía de Configuración

## ✅ Funcionalidades Implementadas

### 1. **Notificaciones en Base de Datos**
- ✅ Tabla `notifications` creada en PostgreSQL
- ✅ Modelo `Notification` con todos los campos necesarios
- ✅ Relaciones con usuarios, planes de nutrición y entrenamiento

### 2. **Interfaz de Usuario**
- ✅ Página `/notificaciones` para ver todas las notificaciones
- ✅ Badge en navbar con contador de no leídas
- ✅ Marcar como leída (individual o todas)
- ✅ Eliminar notificaciones
- ✅ Links directos a planes relacionados

### 3. **Envío de Emails**
- ✅ Integración con Flask-Mail
- ✅ Templates HTML profesionales
- ✅ Email automático cuando admin notifica planes listos
- ✅ Fallback si email no está configurado

## 🔧 Configuración de Email (Gmail)

### Opción 1: Gmail con Contraseña de Aplicación (Recomendado)

1. **Habilitar 2FA en tu cuenta de Gmail:**
   - Ve a https://myaccount.google.com/security
   - Activa "Verificación en 2 pasos"

2. **Generar Contraseña de Aplicación:**
   - Ve a https://myaccount.google.com/apppasswords
   - Selecciona "Correo" y "Otro (nombre personalizado)"
   - Escribe "CoachBodyFit360"
   - Copia la contraseña de 16 caracteres

3. **Configurar Variables de Entorno en Railway:**
   ```bash
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=coachbodyfit@gmail.com
   MAIL_PASSWORD=xxxx xxxx xxxx xxxx  # Contraseña de aplicación
   MAIL_DEFAULT_SENDER=CoachBodyFit360 <coachbodyfit@gmail.com>
   ```

### Opción 2: Servicio de Email Profesional (SendGrid, Mailgun, etc.)

**SendGrid (Recomendado para producción):**
```bash
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=apikey
MAIL_PASSWORD=SG.xxxxxxxxxxxxxxxxxxxxxx  # API Key de SendGrid
MAIL_DEFAULT_SENDER=noreply@coachbodyfit360.com
```

**Mailgun:**
```bash
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=postmaster@mg.coachbodyfit360.com
MAIL_PASSWORD=tu-password-mailgun
MAIL_DEFAULT_SENDER=noreply@coachbodyfit360.com
```

## 🚀 Configurar en Railway

### Método 1: Desde el Dashboard Web

1. Ve a tu proyecto en Railway
2. Selecciona el servicio de tu app
3. Ve a "Variables"
4. Agrega las variables de email:
   - `MAIL_SERVER`
   - `MAIL_PORT`
   - `MAIL_USE_TLS`
   - `MAIL_USERNAME`
   - `MAIL_PASSWORD`
   - `MAIL_DEFAULT_SENDER`
5. Guarda y espera el redeploy automático

### Método 2: Desde Railway CLI

```bash
railway variables set MAIL_SERVER=smtp.gmail.com
railway variables set MAIL_PORT=587
railway variables set MAIL_USE_TLS=true
railway variables set MAIL_USERNAME=coachbodyfit@gmail.com
railway variables set MAIL_PASSWORD="xxxx xxxx xxxx xxxx"
railway variables set MAIL_DEFAULT_SENDER="CoachBodyFit360 <coachbodyfit@gmail.com>"
```

## 📱 Cómo Usar el Sistema

### Para el Admin:

1. **Crear planes para un usuario:**
   - Ve a "Usuarios" → Selecciona usuario
   - Crea plan de nutrición y/o entrenamiento

2. **Notificar al usuario:**
   - En el dashboard del usuario, haz clic en "Notificar Planes Listos" 🔔
   - El sistema:
     - ✅ Crea notificación en BD
     - ✅ Envía email al usuario
     - ✅ Muestra mensaje de confirmación

### Para el Usuario:

1. **Ver notificaciones:**
   - Haz clic en "🔔 Notificaciones" en la navbar
   - Verás badge rojo con número de no leídas

2. **Acciones disponibles:**
   - ✅ Marcar como leída
   - ✅ Ver planes relacionados (links directos)
   - ✅ Eliminar notificación
   - ✅ Marcar todas como leídas

## 📧 Templates de Email

### Email de Planes Listos
- **Archivo:** `app/templates/emails/plans_ready.html`
- **Diseño:** HTML responsive con gradiente rojo-naranja
- **Contenido:**
  - Saludo personalizado
  - Lista de planes disponibles
  - Botón CTA "Ver mis planes"
  - Footer con branding

### Email Genérico de Notificación
- **Archivo:** `app/templates/emails/notification.html`
- **Uso:** Para notificaciones personalizadas
- **Contenido:** Título y mensaje de la notificación

## 🧪 Probar el Sistema

### 1. Probar Localmente (Sin Email)

```bash
# El sistema funcionará sin email configurado
# Mostrará advertencia pero guardará notificaciones en BD
flask run
```

### 2. Probar con Email Real

```bash
# Configura las variables en .env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-app
MAIL_DEFAULT_SENDER=tu-email@gmail.com

# Ejecuta la app
flask run

# Crea un plan y notifica al usuario
# Revisa tu bandeja de entrada
```

## 🔍 Troubleshooting

### Email no se envía

**Problema:** "Email no enviado: servidor no configurado"
- **Solución:** Verifica que `MAIL_SERVER` esté configurado en Railway

**Problema:** "Authentication failed"
- **Solución:** 
  - Gmail: Usa contraseña de aplicación, no tu contraseña normal
  - Verifica que 2FA esté habilitado

**Problema:** "Connection refused"
- **Solución:** 
  - Verifica que `MAIL_PORT` sea 587 (TLS) o 465 (SSL)
  - Verifica que `MAIL_USE_TLS` esté en `true`

### Notificaciones no aparecen

**Problema:** Badge no muestra contador
- **Solución:** Verifica que la relación `user.notifications` esté en el modelo User

**Problema:** Error 404 en `/notificaciones`
- **Solución:** Verifica que el blueprint esté registrado en `app/__init__.py`

## 📊 Estructura de Archivos

```
app/
├── blueprints/
│   ├── notifications/
│   │   ├── __init__.py
│   │   └── routes.py          # Rutas de notificaciones
│   └── admin/
│       └── routes.py          # Ruta notify_user_plans actualizada
├── models/
│   └── notification.py        # Modelo Notification
├── services/
│   └── email_service.py       # Servicio de envío de emails
└── templates/
    ├── notifications/
    │   └── index.html         # Página de notificaciones
    └── emails/
        ├── plans_ready.html   # Email de planes listos
        └── notification.html  # Email genérico
```

## 🎯 Próximas Mejoras (Opcional)

- [ ] Notificaciones push (Firebase Cloud Messaging)
- [ ] Notificaciones en tiempo real (WebSockets)
- [ ] Preferencias de notificación por usuario
- [ ] Digest diario de notificaciones
- [ ] Notificaciones por SMS (Twilio)
- [ ] Plantillas de email personalizables desde admin

## 📞 Soporte

Si tienes problemas con la configuración:
1. Revisa los logs de Railway
2. Verifica que todas las variables estén configuradas
3. Prueba localmente primero
4. Contacta al desarrollador si persiste el problema

---

**¡Sistema de Notificaciones Completo y Funcionando!** 🎉
