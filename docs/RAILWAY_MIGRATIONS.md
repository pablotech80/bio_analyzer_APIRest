# Ejecutar Migraciones en Railway (PostgreSQL)

## Problema
Las columnas de fotos (`front_photo_url`, `back_photo_url`, `side_photo_url`) no existen en la base de datos de producción, causando errores SQL.

## Solución: Ejecutar Migraciones Pendientes

### Opción 1: Desde Railway CLI (Recomendado)

```bash
# 1. Instalar Railway CLI (si no lo tienes)
npm i -g @railway/cli

# 2. Login a Railway
railway login

# 3. Conectar al proyecto
railway link

# 4. Ejecutar migraciones
railway run flask db upgrade

# 5. Verificar migración actual
railway run flask db current
```

### Opción 2: Desde Railway Dashboard (Web)

1. Ve a tu proyecto en Railway: https://railway.app
2. Selecciona tu servicio Flask
3. Ve a la pestaña **"Variables"**
4. Agrega una variable temporal:
   ```
   RUN_MIGRATIONS=true
   ```
5. Modifica tu `run.py` o crea un script de inicio que ejecute:
   ```python
   if os.getenv('RUN_MIGRATIONS') == 'true':
       from flask_migrate import upgrade
       upgrade()
   ```
6. Redeploy el servicio
7. **IMPORTANTE**: Elimina la variable `RUN_MIGRATIONS` después

### Opción 3: Conectar Directamente a PostgreSQL

```bash
# 1. Obtener DATABASE_URL de Railway
# Dashboard → Service → Variables → DATABASE_URL

# 2. Conectar con psql
psql "postgresql://postgres:password@host:port/railway"

# 3. Verificar columnas actuales
\d biometric_analyses

# 4. Ejecutar migraciones manualmente (si es necesario)
# Copiar SQL de migrations/versions/c18eb18a660c_add_photo_url_fields_to_biometric_.py
```

## Después de Ejecutar Migraciones

### 1. Descomentar Columnas en el Modelo

Edita `app/models/biometric_analysis.py`:

```python
# ========== 📸 PHOTO URLS (S3 Storage) ==========
front_photo_url = db.Column(
    db.String(255),
    nullable=True,
    comment="URL of front body photo stored in S3"
)
back_photo_url = db.Column(
    db.String(255),
    nullable=True,
    comment="URL of back body photo stored in S3"
)
side_photo_url = db.Column(
    db.String(255),
    nullable=True,
    comment="URL of side body photo stored in S3"
)
```

### 2. Commit y Push

```bash
git add app/models/biometric_analysis.py
git commit -m "feat: Habilitar columnas de fotos después de migración en Railway"
git push origin main
```

### 3. Verificar en Producción

```bash
# Verificar que no hay errores SQL
curl https://app.coachbodyfit360.com/auth/profile
curl https://app.coachbodyfit360.com/historial
```

## Migraciones Pendientes

Según el historial local, estas son las migraciones que deben ejecutarse en Railway:

1. ✅ `fa12d24e9741` - initial_schema_postgresql
2. ✅ `8d34854ebd24` - add_photo_fields_to_biometric_analysis (vacía, solo índices)
3. ❌ `c18eb18a660c` - **add_photo_url_fields_to_biometric_analysis** (CRÍTICA)
4. ✅ `581cd9ed2c74` - add_nutrition_and_training_plans_tables (HEAD)

## Verificar Estado Actual en Railway

```bash
# Ver migración actual en producción
railway run flask db current

# Ver historial completo
railway run flask db history

# Ver migraciones pendientes
railway run flask db heads
```

## Troubleshooting

### Error: "Can't locate revision identified by 'xxxxx'"
- La base de datos está en un estado inconsistente
- Solución: `railway run flask db stamp head` (con precaución)

### Error: "Target database is not up to date"
- Hay migraciones pendientes
- Solución: `railway run flask db upgrade`

### Error: "Multiple heads"
- Hay ramas de migración sin mergear
- Solución: Ya está resuelto con `b5aba5737320_merge_all_heads_after_repair.py`

## Notas Importantes

⚠️ **Backup**: Railway hace backups automáticos, pero verifica antes de ejecutar migraciones
⚠️ **Downtime**: Las migraciones pueden causar breve downtime (segundos)
⚠️ **Reversión**: Si algo falla, usa `flask db downgrade` con precaución
