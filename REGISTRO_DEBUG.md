# 🔍 Guía de Diagnóstico - Problemas de Registro en Producción

## Problemas Identificados

### 1. **Rol 'client' Faltante** ⚠️
El sistema requiere que exista un rol llamado 'client' en la tabla `roles`. Si no existe, los registros fallan.

**Solución:**
```bash
# En Railway, ejecutar:
python fix_production_roles.py
```

### 2. **Cookies Seguras y HTTPS** 🔒
La configuración de producción requiere HTTPS estricto:
- `SESSION_COOKIE_SECURE = True`
- `REMEMBER_COOKIE_SECURE = True`
- `JWT_COOKIE_SECURE = True`

Si Railway tiene problemas con SSL, las sesiones fallan silenciosamente.

**Solución Temporal:**
```bash
# En Railway, agregar variable de entorno:
FORCE_HTTPS=false
```

### 3. **CSRF Tokens** 🛡️
Los tokens CSRF pueden fallar si:
- No hay SECRET_KEY configurado
- Las cookies no se guardan correctamente
- Hay problemas de CORS

**Verificar:**
```bash
# En Railway, verificar que existe:
SECRET_KEY=tu-clave-secreta-aqui
```

### 4. **Errores de Base de Datos Ocultos** 💾
Los errores genéricos ocultan problemas reales de PostgreSQL.

**Ahora se loguean con detalles:**
- Errores de validación
- Errores de BD
- Problemas con roles

## Scripts de Diagnóstico

### 1. Verificar Estado de Producción
```bash
python check_production_db.py
```

Este script verifica:
- ✅ Conexión a PostgreSQL
- ✅ Existencia de tablas (users, roles)
- ✅ Existencia del rol 'client'
- ✅ Variables de entorno
- ✅ Constraints de BD

### 2. Crear Roles Faltantes
```bash
python fix_production_roles.py
```

Crea automáticamente:
- `client` - Usuario estándar
- `admin` - Administrador
- `trainer` - Entrenador

### 3. Ver Logs en Railway
```bash
# En Railway Dashboard:
# 1. Ir a tu servicio
# 2. Click en "Deployments"
# 3. Click en el deployment activo
# 4. Ver "Logs"
```

Buscar errores como:
- `Error de validación en registro:`
- `Error crítico en registro:`
- `Error al crear rol 'client':`
- `Error al guardar usuario en BD:`

## Cambios Implementados

### ✅ Mejoras en `auth/routes.py`
- Logging detallado de errores de validación
- Mensajes de error más descriptivos
- Log de errores de formulario

### ✅ Mejoras en `auth/services.py`
- Creación automática de rol 'client' si no existe
- Rollback en caso de error de BD
- Logging de cada paso del registro
- Mensajes de error específicos

### ✅ Mejoras en `config.py`
- Variable `FORCE_HTTPS` para debugging
- Permite desactivar cookies seguras temporalmente

## Pasos para Resolver en Producción

### Paso 1: Diagnosticar
```bash
# Ejecutar en Railway o localmente con DATABASE_URL de producción:
python check_production_db.py
```

### Paso 2: Crear Roles
```bash
# Si el diagnóstico muestra que falta el rol 'client':
python fix_production_roles.py
```

### Paso 3: Verificar Variables de Entorno
En Railway Dashboard, verificar:
```
SECRET_KEY=<clave-secreta-fuerte>
DATABASE_URL=<postgresql://...>
DATABASE_PRIVATE_URL=<postgresql://...>
FLASK_ENV=production
```

### Paso 4: Probar Registro
1. Ir a: https://app.coachbodyfit360.com/auth/register
2. Intentar registrar un usuario de prueba
3. Si falla, revisar logs en Railway

### Paso 5: Si Persiste el Error
Activar modo debug temporal:
```bash
# En Railway, agregar:
FORCE_HTTPS=false
```

Luego intentar registrarse nuevamente y revisar logs.

## Errores Comunes y Soluciones

### Error: "El email ya está registrado"
**Causa:** Usuario intentando registrarse con email duplicado
**Solución:** Usar otro email o recuperar contraseña

### Error: "Error al configurar el rol de usuario"
**Causa:** Tabla `roles` vacía o rol 'client' no existe
**Solución:** `python fix_production_roles.py`

### Error: "Error al guardar en la base de datos"
**Causa:** Problemas de conexión o constraints de BD
**Solución:** Revisar logs detallados, verificar conexión PostgreSQL

### Error: Formulario no se envía (sin mensaje)
**Causa:** CSRF token inválido o cookies bloqueadas
**Solución:** 
1. Verificar SECRET_KEY en Railway
2. Probar con `FORCE_HTTPS=false`
3. Limpiar cookies del navegador

### Error: "Validation error" en logs
**Causa:** Campos del formulario no pasan validación
**Solución:** Revisar que:
- Username: 3-80 caracteres
- Email: formato válido
- Password: mínimo 8 caracteres
- Password confirm: coincide con password

## Monitoreo Post-Fix

Después de aplicar los fixes, monitorear:

1. **Logs de Railway** - Buscar:
   - "Nuevo usuario registrado:"
   - "Usuario guardado en BD:"
   - Cualquier error con "Error crítico en registro:"

2. **Base de Datos** - Verificar:
   ```sql
   SELECT COUNT(*) FROM users WHERE created_at > NOW() - INTERVAL '1 hour';
   ```

3. **Emails de Verificación** - Confirmar que se generan tokens

## Contacto de Soporte

Si después de seguir todos los pasos el problema persiste:

1. Exportar logs de Railway
2. Ejecutar `python check_production_db.py` y guardar output
3. Capturar screenshot del error en navegador
4. Revisar consola del navegador (F12) para errores JavaScript

---

**Última actualización:** 2026-01-19
**Versión:** 1.0
