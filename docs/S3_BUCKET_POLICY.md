# 🔒 Configurar Permisos Públicos en S3 (Sin ACLs)

Tu bucket S3 tiene deshabilitadas las ACLs (Access Control Lists), que es la configuración recomendada por AWS. En su lugar, necesitas usar una **Bucket Policy**.

## 📝 Paso 1: Ir a la Configuración del Bucket

1. Ve a AWS Console: https://s3.console.aws.amazon.com
2. Click en tu bucket: `coach360-media`
3. Ve a la pestaña **"Permissions"**

## 🔓 Paso 2: Configurar Bucket Policy

1. Scroll hasta **"Bucket policy"**
2. Click en **"Edit"**
3. Pega esta política:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::coach360-media/*"
        }
    ]
}
```

4. Click en **"Save changes"**

## ✅ Qué Hace Esta Política

- **Permite**: Lectura pública de todos los objetos en el bucket
- **No permite**: Escritura, eliminación o listado del bucket
- **Seguro**: Solo tu aplicación (con credenciales) puede subir archivos
- **Público**: Cualquiera puede ver las imágenes subidas

## 🔍 Verificar Configuración

Después de aplicar la política, verifica:

1. **Block Public Access**: Debe estar configurado así:
   - ❌ Block all public access: **OFF**
   - ✅ Block public access to buckets and objects granted through new access control lists (ACLs): **ON**
   - ✅ Block public access to buckets and objects granted through any access control lists (ACLs): **ON**
   - ❌ Block public access to buckets and objects granted through new public bucket or access point policies: **OFF**
   - ❌ Block public and cross-account access to buckets and objects through any public bucket or access point policies: **OFF**

2. **Object Ownership**: Debe estar en:
   - ✅ **Bucket owner enforced** (ACLs disabled)

## 🧪 Probar

Después de configurar la política:

1. Reinicia tu servidor Flask
2. Sube una imagen de prueba
3. Copia la URL de la imagen
4. Ábrela en una ventana de incógnito del navegador
5. Debería verse la imagen sin problemas

## 🔐 Seguridad

Esta configuración es **segura** porque:
- ✅ Solo lectura pública (nadie puede subir archivos sin credenciales)
- ✅ Tu app usa credenciales IAM para subir
- ✅ No hay ACLs (más simple y seguro)
- ✅ Política de bucket controlada centralmente

## 📚 Más Información

- [AWS S3 Bucket Policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html)
- [Blocking Public Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)

---

**Nota**: Si prefieres mantener el bucket completamente privado y usar URLs firmadas (signed URLs), avísame y te ayudo a implementarlo.
