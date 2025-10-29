# Configurar Bucket S3 como Público

**Bucket:** `coach360-media`  
**Región:** `eu-north-1`

---

## Problema Resuelto

❌ **Error anterior:** `AccessControlListNotSupported`  
✅ **Solución:** Eliminar `ACL: 'public-read'` del código

---

## Configuración Necesaria en AWS S3

### Opción 1: Bucket Policy (Recomendado)

1. Ve a AWS Console → S3 → `coach360-media`
2. Pestaña **"Permissions"**
3. Sección **"Bucket policy"** → Click **"Edit"**
4. Pega esta política:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::coach360-media/biometric_photos/*"
    }
  ]
}
```

5. Click **"Save changes"**

**Esto hace que:**
- Solo la carpeta `biometric_photos/` sea pública
- Otras carpetas permanecen privadas
- Los archivos son accesibles vía URL directa

---

### Opción 2: Block Public Access (Menos Seguro)

1. Ve a AWS Console → S3 → `coach360-media`
2. Pestaña **"Permissions"**
3. Sección **"Block public access (bucket settings)"** → Click **"Edit"**
4. **Desmarca** todas las opciones:
   - [ ] Block all public access
   - [ ] Block public access to buckets and objects granted through new access control lists (ACLs)
   - [ ] Block public access to buckets and objects granted through any access control lists (ACLs)
   - [ ] Block public access to buckets and objects granted through new public bucket or access point policies
   - [ ] Block public and cross-account access to buckets and objects through any public bucket or access point policies
5. Click **"Save changes"**
6. Confirma escribiendo "confirm"

**⚠️ Advertencia:** Esto hace TODO el bucket público, no solo `biometric_photos/`

---

## Verificar que Funciona

### 1. Sube un archivo de prueba:

```bash
aws s3 cp test.jpg s3://coach360-media/biometric_photos/test.jpg
```

### 2. Accede vía URL:

```
https://coach360-media.s3.eu-north-1.amazonaws.com/biometric_photos/test.jpg
```

Si ves la imagen, ✅ está configurado correctamente.

---

## Alternativa: CloudFront (Producción)

Para mejor rendimiento y seguridad, considera usar CloudFront:

1. Crear distribución CloudFront
2. Origen: `coach360-media.s3.eu-north-1.amazonaws.com`
3. Configurar cache
4. Usar URL tipo: `https://d123456.cloudfront.net/biometric_photos/test.jpg`

**Beneficios:**
- ✅ CDN global (más rápido)
- ✅ HTTPS automático
- ✅ Cache en edge locations
- ✅ Menor costo de transferencia

---

## Resumen

**Cambio en código:** ✅ Eliminado `ACL: 'public-read'`  
**Configuración AWS:** ⏳ Pendiente agregar Bucket Policy  
**Resultado:** URLs públicas funcionarán después de configurar AWS

**Próximo paso:** Configurar Bucket Policy en AWS Console
