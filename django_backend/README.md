# CoachBodyFit360 - Django Backend

Backend Django para la plataforma SaaS multi-tenant de análisis biométrico, nutrición y entrenamiento.

## 🏗️ Arquitectura

### Estructura del Proyecto

```
django_backend/
├── core/                      # Configuración principal Django
│   ├── settings.py           # Configuración (desarrollo/producción)
│   ├── urls.py               # URLs principales
│   └── wsgi.py               # WSGI para producción
├── apps/                      # Aplicaciones modulares
│   ├── users/                # Usuarios y autenticación
│   ├── organizations/        # Organizaciones multi-tenant
│   ├── permissions/          # Roles y permisos
│   ├── bioanalyze/          # Análisis biométrico
│   ├── nutrition/           # Planes nutricionales
│   └── training/            # Planes de entrenamiento
├── scripts/                  # Scripts de utilidad
├── static/                   # Archivos estáticos
├── media/                    # Archivos subidos por usuarios
├── logs/                     # Logs de la aplicación
└── manage.py                # CLI de Django

```

### Modelos Implementados

#### **Users** (`apps.users`)
- `User`: Usuario personalizado (AbstractUser) con campos adicionales
  - Email verification
  - Avatar
  - Biografía
  - Timestamps

#### **Organizations** (`apps.organizations`)
- `Organization`: Organizaciones multi-tenant
  - Tipos: Individual, Gym, Nutritionist, Trainer, Corporate
  - Planes de suscripción: Free, Premium, Pro, Business
- `Membership`: Relación User ↔ Organization con Role

#### **Permissions** (`apps.permissions`)
- `Permission`: Permisos granulares del sistema (32 permisos)
- `Role`: Roles del sistema (5 roles predefinidos)
  - Client
  - Trainer
  - Nutritionist
  - Admin
  - SuperAdmin

#### **BioAnalyze** (`apps.bioanalyze`)
- `BiometricAnalysis`: Análisis corporal completo
  - Medidas básicas (peso, altura, edad, género)
  - Circunferencias (cuello, cintura, cadera)
  - Medidas musculares bilaterales (bíceps, muslos, gemelos)
  - Métricas calculadas (IMC, TMB, TDEE, % grasa, etc.)
  - Datos FitMaster AI (JSON)
  - URLs de fotos (Azure Blob Storage)

#### **Nutrition** (`apps.nutrition`)
- `NutritionPlan`: Planes nutricionales personalizados

#### **Training** (`apps.training`)
- `TrainingPlan`: Planes de entrenamiento personalizados

---

## 🚀 Setup y Desarrollo

### 1. Requisitos Previos

- Python 3.13+
- PostgreSQL (producción) o SQLite (desarrollo)
- pip

### 2. Instalación

```bash
# Navegar al directorio del proyecto Django
cd django_backend

# Instalar dependencias
pip install -r requirements.txt

# Copiar archivo de configuración
cp .env.example .env

# Editar .env con tus configuraciones
nano .env
```

### 3. Configurar Base de Datos

**Desarrollo (SQLite):**
```bash
# Ya configurado por defecto en .env
DATABASE_URL=sqlite:///db.sqlite3
```

**Producción (PostgreSQL):**
```bash
# Editar .env
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

### 4. Ejecutar Migraciones

```bash
# Generar migraciones (si hay cambios en modelos)
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

### 5. Poblar Base de Datos con Datos Iniciales

```bash
# Crear permisos, roles y usuario SuperAdmin
python manage.py seed_data
```

**Credenciales SuperAdmin:**
- Email: `admin@coachbodyfit360.com`
- Password: `Admin123!`

⚠️ **IMPORTANTE**: Cambiar esta contraseña en producción.

### 6. Ejecutar Servidor de Desarrollo

```bash
python manage.py runserver 8000
```

Acceder a:
- **Admin Panel**: http://localhost:8000/admin/
- **API Docs**: http://localhost:8000/api/docs/
- **API Schema**: http://localhost:8000/api/schema/

---

## 🔐 Sistema de Permisos

### Permisos por Módulo

**BioAnalyze (7 permisos):**
- `bioanalyze.view_own` / `view_all`
- `bioanalyze.create`
- `bioanalyze.update_own` / `update_all`
- `bioanalyze.delete_own` / `delete_all`

**Nutrition (7 permisos):**
- `nutrition.view_own` / `view_all`
- `nutrition.create`
- `nutrition.update_own` / `update_all`
- `nutrition.delete_own` / `delete_all`

**Training (7 permisos):**
- `training.view_own` / `view_all`
- `training.create`
- `training.update_own` / `update_all`
- `training.delete_own` / `delete_all`

**Users (6 permisos):**
- `users.view_own` / `view_all`
- `users.update_own` / `update_all`
- `users.invite` / `remove`

**Organization (4 permisos):**
- `organization.view` / `update`
- `organization.manage_members` / `manage_roles`

**System (1 permiso):**
- `system.admin` (acceso total)

### Roles Predefinidos

| Role | Permisos | Descripción |
|------|----------|-------------|
| **Client** | 11 permisos | Usuario básico (solo datos propios) |
| **Trainer** | 28 permisos | Entrenador (gestiona clientes) |
| **Nutritionist** | 22 permisos | Nutricionista (enfoque en nutrición) |
| **Admin** | 31 permisos | Administrador de organización |
| **SuperAdmin** | 32 permisos | Administrador del sistema |

---

## 📊 Panel de Administración Django

### Acceso
http://localhost:8000/admin/

### Funcionalidades

- **Users**: Gestión completa de usuarios
  - Filtros: activo, staff, superuser, email verificado, género
  - Búsqueda: email, username, nombre, teléfono
  - Campos personalizados: avatar, biografía, verificación de email

- **Organizations**: Gestión de organizaciones
  - Inline: Memberships (usuarios de la organización)
  - Filtros: tipo, plan de suscripción, activo
  - Búsqueda: nombre, slug, email, ciudad, país

- **Memberships**: Relaciones User-Organization-Role
  - Autocomplete: user, organization, role
  - Filtros: activo, rol, fecha de creación

- **Roles**: Gestión de roles
  - Filter horizontal para permisos
  - Contador de permisos asignados
  - Protección de roles del sistema

- **Permissions**: Permisos del sistema
  - Filtros: módulo, acción
  - Búsqueda: nombre, descripción

- **BiometricAnalysis**: Análisis biométricos
  - Filtros: género, nivel de actividad, objetivo
  - Búsqueda: email de usuario, nombre de organización
  - Secciones colapsables: medidas bilaterales, métricas calculadas, FitMaster AI

- **NutritionPlan**: Planes nutricionales
- **TrainingPlan**: Planes de entrenamiento

---

## 🔧 Comandos Útiles

### Gestión de Base de Datos

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Revertir migraciones
python manage.py migrate app_name migration_name

# Ver SQL de una migración
python manage.py sqlmigrate app_name migration_number

# Verificar problemas
python manage.py check
```

### Usuarios

```bash
# Crear superusuario manualmente
python manage.py createsuperuser

# Cambiar contraseña
python manage.py changepassword username
```

### Shell Interactivo

```bash
# Django shell
python manage.py shell

# Django shell con IPython
python manage.py shell -i ipython
```

### Testing

```bash
# Ejecutar todos los tests
python manage.py test

# Ejecutar tests de una app específica
python manage.py test apps.users

# Con coverage
coverage run --source='.' manage.py test
coverage report
```

### Archivos Estáticos

```bash
# Recolectar archivos estáticos para producción
python manage.py collectstatic --noinput
```

---

## 🌐 API REST (Futuro - Fase 2)

### Endpoints Planeados

```
/api/v1/
├── auth/
│   ├── register/          POST   - Registro de usuario
│   ├── login/             POST   - Login (JWT)
│   ├── logout/            POST   - Logout
│   ├── refresh/           POST   - Refresh token
│   └── verify-email/      POST   - Verificar email
├── users/
│   ├── me/                GET    - Perfil actual
│   ├── me/                PATCH  - Actualizar perfil
│   └── {id}/              GET    - Ver usuario (permisos)
├── organizations/
│   ├── /                  GET    - Listar organizaciones
│   ├── /                  POST   - Crear organización
│   ├── {id}/              GET    - Detalle organización
│   ├── {id}/members/      GET    - Miembros
│   └── {id}/invite/       POST   - Invitar usuario
├── bioanalyze/
│   ├── /                  GET    - Listar análisis
│   ├── /                  POST   - Crear análisis
│   ├── {id}/              GET    - Detalle análisis
│   ├── {id}/              PATCH  - Actualizar análisis
│   └── {id}/              DELETE - Eliminar análisis
├── nutrition/
│   └── ... (similar a bioanalyze)
└── training/
    └── ... (similar a bioanalyze)
```

---

## 🚢 Deploy a Azure (Fase 3)

### Servicios Azure Requeridos

- **Azure Container Apps**: Aplicación Django
- **Azure Database for PostgreSQL**: Base de datos
- **Azure Blob Storage**: Archivos multimedia
- **Azure OpenAI Service**: FitMaster AI
- **Azure Communication Services**: Emails
- **Azure Container Registry**: Imágenes Docker

### Variables de Entorno Producción

```bash
DJANGO_SECRET_KEY=<secret-key-production>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=api.coachbodyfit360.com
DJANGO_ENVIRONMENT=production

DATABASE_URL=postgresql://user:pass@host.postgres.database.azure.com:5432/dbname

AZURE_STORAGE_ACCOUNT_NAME=<storage-account>
AZURE_STORAGE_ACCOUNT_KEY=<storage-key>
AZURE_STORAGE_CONTAINER_NAME=media

AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=<api-key>
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

EMAIL_HOST=smtp.azurecomm.net
EMAIL_HOST_USER=<email>
EMAIL_HOST_PASSWORD=<password>

CORS_ALLOWED_ORIGINS=https://app.coachbodyfit360.com
```

---

## 📝 Próximos Pasos (Roadmap)

### ✅ Fase 1: Backend Django Core (COMPLETADA)
- [x] Estructura modular con apps
- [x] Modelos de datos multi-tenant
- [x] Sistema de permisos granular
- [x] Django Admin configurado
- [x] Migraciones iniciales
- [x] Seeding de datos

### 🔄 Fase 2: API REST con DRF (En Progreso)
- [ ] Serializers para todos los modelos
- [ ] ViewSets y endpoints CRUD
- [ ] Autenticación JWT
- [ ] Permisos personalizados
- [ ] Documentación Swagger/OpenAPI
- [ ] Tests de integración

### 📅 Fase 3: Deploy Azure
- [ ] Dockerfile y docker-compose
- [ ] Terraform para infraestructura
- [ ] CI/CD con GitHub Actions
- [ ] Integración con Azure OpenAI
- [ ] Monitoreo y logs

### 📅 Fase 4: Frontend Next.js
- [ ] Consumo de API REST
- [ ] Dashboard multi-tenant
- [ ] Sistema de suscripciones
- [ ] Integración de pagos

---

## 🤝 Contribución

Este proyecto sigue las mejores prácticas de Django y está diseñado para ser escalable y mantenible.

### Convenciones de Código

- **PEP 8**: Estilo de código Python
- **Black**: Formateador automático
- **isort**: Ordenamiento de imports
- **Flake8**: Linting
- **Mypy**: Type checking

### Commits Semánticos

```
feat: Nueva funcionalidad
fix: Corrección de bug
docs: Documentación
style: Formato de código
refactor: Refactorización
test: Tests
chore: Mantenimiento
```

---

## 📄 Licencia

Propietario: Pablo Techera  
Proyecto: CoachBodyFit360

---

## 📞 Soporte

Para dudas o problemas, contactar al equipo de desarrollo.
