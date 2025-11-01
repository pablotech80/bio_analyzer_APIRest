# 🚀 Guía Completa: Configurar AWS S3 + CloudFront

**Objetivo**: Almacenamiento escalable y CDN global para imágenes del blog  
**Tiempo estimado**: 30-45 minutos  
**Costo**: ~$5-10/mes (Free Tier: primeros 12 meses gratis)

---

## 📋 REQUISITOS PREVIOS

- [ ] Cuenta de AWS (crear en https://aws.amazon.com)
- [ ] Tarjeta de crédito (para verificación, no se cobra si estás en Free Tier)
- [ ] Acceso a Railway para configurar variables de entorno

---

## 🎯 PASO 1: Crear Bucket en S3 (10 minutos)

### 1.1 Acceder a S3

1. Ir a AWS Console: https://console.aws.amazon.com
2. Buscar "S3" en la barra de búsqueda
3. Click en "Create bucket"

### 1.2 Configurar Bucket

**Nombre del bucket**:
```
coachbodyfit360-media
```
> ⚠️ El nombre debe ser único globalmente. Si está tomado, usa: `coachbodyfit360-media-prod`

**Región**:
```
US East (N. Virginia) us-east-1
```
> 💡 Recomendado: Elige la región más cercana a tus usuarios

**Object Ownership**:
- ✅ Seleccionar: **ACLs enabled**
- ✅ Seleccionar: **Bucket owner preferred**

**Block Public Access settings**:
- ❌ **DESMARCAR** "Block all public access"
- ✅ Confirmar que entiendes que el bucket será público

**Bucket Versioning**:
- ⚪ Disabled (no necesario para imágenes)

**Default encryption**:
- ✅ Enable
- ✅ Amazon S3 managed keys (SSE-S3)

**Click en "Create bucket"**

### 1.3 Configurar Política de Bucket (Acceso Público)

1. Click en el bucket recién creado
2. Ir a la pestaña **"Permissions"**
3. Scroll hasta **"Bucket policy"**
4. Click en **"Edit"**
5. Pegar esta política:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::coachbodyfit360-media/*"
        }
    ]
}
```

> ⚠️ Reemplaza `coachbodyfit360-media` con el nombre de tu bucket

6. Click en **"Save changes"**

### 1.4 Configurar CORS

1. En la pestaña **"Permissions"**
2. Scroll hasta **"Cross-origin resource sharing (CORS)"**
3. Click en **"Edit"**
4. Pegar esta configuración:

```json
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET",
            "PUT",
            "POST",
            "DELETE"
        ],
        "AllowedOrigins": [
            "https://app.coachbodyfit360.com",
            "https://coachbodyfit360.com",
            "http://localhost:5000",
            "http://localhost:5001"
        ],
        "ExposeHeaders": [
            "ETag"
        ],
        "MaxAgeSeconds": 3000
    }
]
```

5. Click en **"Save changes"**

---

## 🌐 PASO 2: Configurar CloudFront CDN (15 minutos)

### 2.1 Crear Distribución de CloudFront

1. Ir a AWS Console
2. Buscar "CloudFront"
3. Click en **"Create distribution"**

### 2.2 Configurar Origen (Origin)

**Origin domain**:
- Seleccionar tu bucket S3 de la lista desplegable
- Ejemplo: `coachbodyfit360-media.s3.us-east-1.amazonaws.com`

**Origin path**: (dejar vacío)

**Name**: (auto-generado, dejar como está)

**Origin access**:
- ✅ Seleccionar: **Public**

### 2.3 Configurar Comportamiento (Default Cache Behavior)

**Viewer protocol policy**:
- ✅ Seleccionar: **Redirect HTTP to HTTPS**

**Allowed HTTP methods**:
- ✅ Seleccionar: **GET, HEAD, OPTIONS**

**Cache key and origin requests**:
- ✅ Seleccionar: **Cache policy and origin request policy (recommended)**

**Cache policy**:
- ✅ Seleccionar: **CachingOptimized**

**Origin request policy**:
- ✅ Seleccionar: **CORS-S3Origin**

### 2.4 Configurar Distribución (Settings)

**Price class**:
- ✅ Seleccionar: **Use all edge locations (best performance)**
- 💡 O si quieres ahorrar: **Use only North America and Europe**

**Alternate domain name (CNAME)**: (dejar vacío por ahora)

**Custom SSL certificate**: (dejar por defecto)

**Default root object**: (dejar vacío)

**Click en "Create distribution"**

### 2.5 Esperar Deployment (5-10 minutos)

- El status cambiará de "Deploying" a "Enabled"
- Mientras tanto, copia el **Distribution domain name**
- Ejemplo: `d1234abcd5678.cloudfront.net`

---

## 🔑 PASO 3: Crear Credenciales IAM (10 minutos)

### 3.1 Crear Usuario IAM

1. Ir a AWS Console
2. Buscar "IAM"
3. Click en **"Users"** en el menú lateral
4. Click en **"Create user"**

**User name**:
```
coachbodyfit360-s3-uploader
```

**Access type**:
- ✅ Seleccionar: **Programmatic access**

Click en **"Next: Permissions"**

### 3.2 Asignar Permisos

**Attach existing policies directly**:
- ✅ Buscar y seleccionar: **AmazonS3FullAccess**

> 💡 Para producción, es mejor crear una política personalizada con permisos mínimos

Click en **"Next: Tags"** (opcional, puedes saltar)

Click en **"Next: Review"**

Click en **"Create user"**

### 3.3 Guardar Credenciales

⚠️ **MUY IMPORTANTE**: Esta es la única vez que verás estas credenciales

Copiar y guardar en un lugar seguro:
- **Access key ID**: `AKIA...` (20 caracteres)
- **Secret access key**: `...` (40 caracteres)

> 💡 Recomendación: Guardar en un gestor de contraseñas (1Password, LastPass, etc.)

---

## ⚙️ PASO 4: Configurar Variables de Entorno

### 4.1 En Local (.env)

Editar el archivo `.env`:

```bash
# AWS S3 Configuration
AWS_BUCKET_NAME=coachbodyfit360-media
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
CLOUDFRONT_DOMAIN=d1234abcd5678.cloudfront.net
```

> ⚠️ **NUNCA** commitear el archivo `.env` al repositorio

### 4.2 En Railway (Producción)

1. Ir a Railway Dashboard
2. Seleccionar tu proyecto
3. Click en **"Variables"**
4. Agregar las siguientes variables:

```
AWS_BUCKET_NAME=coachbodyfit360-media
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
CLOUDFRONT_DOMAIN=d1234abcd5678.cloudfront.net
```

5. Click en **"Save"**
6. Railway reiniciará automáticamente la aplicación

---

## 🧪 PASO 5: Probar la Configuración (5 minutos)

### 5.1 Test Local

```bash
# Iniciar servidor
flask run

# Abrir navegador
http://localhost:5000/blog/admin

# Crear nuevo post
# Subir una imagen
# Verificar que se sube correctamente
```

### 5.2 Verificar en S3

1. Ir a AWS Console → S3
2. Abrir tu bucket
3. Deberías ver la carpeta `blog/` con la imagen subida

### 5.3 Verificar CDN

1. Copiar la URL de la imagen del post
2. Debería ser algo como: `https://d1234abcd5678.cloudfront.net/blog/imagen_abc123.webp`
3. Abrir en navegador
4. Debería cargar rápidamente

### 5.4 Test de Performance

Usar herramientas online:
- https://tools.pingdom.com
- https://gtmetrix.com

**Resultado esperado**:
- ✅ Tiempo de carga de imagen: < 500ms
- ✅ Tamaño de imagen optimizado (WebP)
- ✅ Cache headers correctos (1 año)

---

## 📊 PASO 6: Monitoreo y Costos

### 6.1 Free Tier de AWS (Primeros 12 meses)

**S3**:
- ✅ 5 GB de almacenamiento
- ✅ 20,000 GET requests
- ✅ 2,000 PUT requests

**CloudFront**:
- ✅ 50 GB de transferencia de datos
- ✅ 2,000,000 HTTP/HTTPS requests

### 6.2 Costos Después del Free Tier

**S3** (por mes):
- Almacenamiento: $0.023/GB
- GET requests: $0.0004 por 1,000 requests
- PUT requests: $0.005 por 1,000 requests

**CloudFront** (por mes):
- Transferencia: $0.085/GB (primeros 10 TB)
- Requests: $0.0075 por 10,000 requests

**Ejemplo para blog mediano**:
- 10 GB de imágenes en S3: $0.23
- 100 GB de transferencia CDN: $8.50
- **Total: ~$9/mes**

### 6.3 Configurar Alertas de Costo

1. Ir a AWS Console → Billing
2. Click en **"Budgets"**
3. Click en **"Create budget"**
4. Configurar alerta cuando el costo supere $10/mes

---

## 🔧 TROUBLESHOOTING

### Problema: "Access Denied" al subir imagen

**Solución**:
1. Verificar que la política del bucket permite `s3:PutObject`
2. Verificar que el usuario IAM tiene permisos `AmazonS3FullAccess`
3. Verificar que las credenciales en `.env` son correctas

### Problema: Imagen no se ve (403 Forbidden)

**Solución**:
1. Verificar que la política del bucket permite `s3:GetObject` público
2. Verificar que "Block Public Access" está deshabilitado
3. Verificar que el ACL del objeto es `public-read`

### Problema: CloudFront no sirve la imagen

**Solución**:
1. Esperar 10-15 minutos después de crear la distribución
2. Verificar que el origen está configurado correctamente
3. Invalidar cache de CloudFront si es necesario

### Problema: Imágenes muy pesadas

**Solución**:
- El `StorageService` ya optimiza automáticamente
- Verifica que `optimize=True` en el upload
- Las imágenes se convierten a WebP (mejor compresión)

---

## 🎯 PRÓXIMOS PASOS

Una vez configurado S3 + CloudFront:

### 1. Migrar Imágenes Existentes (si las hay)

Crear script de migración:

```python
# scripts/migrate_images_to_s3.py
from app import create_app, db
from app.models import MediaFile
from app.services.storage_service import storage_service

app = create_app('production')

with app.app_context():
    # Obtener todas las imágenes locales
    media_files = MediaFile.query.filter_by(file_type='image').all()
    
    for media in media_files:
        # Leer archivo local
        with open(media.file_path, 'rb') as f:
            # Subir a S3
            result = storage_service.upload_image(f, folder='blog')
            
            # Actualizar BD
            media.file_url = result['url']
            media.file_path = result['s3_key']
        
        db.session.commit()
        print(f"✅ Migrado: {media.filename}")
```

### 2. Configurar Lifecycle Policies

Para eliminar automáticamente archivos temporales:

1. Ir a S3 → Tu bucket → Management → Lifecycle rules
2. Crear regla para eliminar objetos en `temp/` después de 7 días

### 3. Habilitar Versionado (Opcional)

Para mantener historial de cambios:

1. Ir a S3 → Tu bucket → Properties
2. Bucket Versioning → Enable

### 4. Configurar Dominio Personalizado (Opcional)

Para usar `cdn.coachbodyfit360.com` en lugar de `d1234.cloudfront.net`:

1. Crear registro CNAME en tu DNS:
   ```
   cdn.coachbodyfit360.com → d1234abcd5678.cloudfront.net
   ```

2. Solicitar certificado SSL en AWS Certificate Manager

3. Actualizar distribución de CloudFront con el dominio personalizado

---

## 📚 RECURSOS ADICIONALES

### Documentación Oficial
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [CloudFront Documentation](https://docs.aws.amazon.com/cloudfront/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

### Tutoriales
- [S3 Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
- [CloudFront Performance](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/ConfiguringCaching.html)

### Herramientas Útiles
- [S3 Browser](https://s3browser.com/) - Cliente GUI para S3
- [Cyberduck](https://cyberduck.io/) - Cliente FTP/S3
- [AWS CLI](https://aws.amazon.com/cli/) - Línea de comandos

---

## ✅ CHECKLIST FINAL

- [ ] Bucket S3 creado
- [ ] Política de bucket configurada (acceso público)
- [ ] CORS configurado
- [ ] Distribución de CloudFront creada y activa
- [ ] Usuario IAM creado con permisos
- [ ] Credenciales guardadas de forma segura
- [ ] Variables de entorno configuradas en local
- [ ] Variables de entorno configuradas en Railway
- [ ] Test de upload exitoso
- [ ] Imagen se sirve desde CloudFront
- [ ] Performance verificada (< 500ms)
- [ ] Alertas de costo configuradas

---

## 🎉 ¡FELICITACIONES!

Tu blog ahora tiene:
- ✅ Almacenamiento escalable (S3)
- ✅ CDN global (CloudFront)
- ✅ Optimización automática de imágenes (WebP)
- ✅ Thumbnails automáticos
- ✅ Cache de 1 año
- ✅ Carga ultra rápida (< 500ms)

**Próximo paso**: Implementar TinyMCE para editor WYSIWYG profesional

---

**Última actualización**: 2025-11-01  
**Autor**: CoachBodyFit360 Team  
**Versión**: 1.0
