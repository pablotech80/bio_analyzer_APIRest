# Guía de Contribución - CoachBodyFit360

## 📋 Tabla de Contenidos
1. [Estructura de Ramas](#estructura-de-ramas)
2. [Flujo de Trabajo](#flujo-de-trabajo)
3. [Convenciones de Commits](#convenciones-de-commits)
4. [Pull Requests](#pull-requests)
5. [Protección de Ramas](#protección-de-ramas)
6. [CODEOWNERS](#codeowners)
7. [Checks Automáticos Pre-Merge](#checks-automáticos-pre-merge)
8. [Entornos de Deploy](#entornos-de-deploy)

---

## 🌳 Estructura de Ramas

### Ramas Permanentes

#### `main` - Producción
- **Propósito**: Código en producción (app.coachbodyfit360.com)
- **Protección**: Máxima - Solo merge via Pull Request
- **Deploy**: Automático a Railway (producción)
- **Regla**: NUNCA hacer push directo

#### `develop` - Desarrollo/Staging
- **Propósito**: Integración de nuevas features
- **Protección**: Media - Requiere Pull Request
- **Deploy**: Automático a entorno staging
- **Regla**: Rama base para crear features

### Ramas Temporales

#### `feature/*` - Nuevas Funcionalidades
```bash
Ejemplos:
- feature/stripe-integration
- feature/admin-dashboard
- feature/user-notifications
```
- **Origen**: Se crea desde `develop`
- **Destino**: Merge a `develop` via PR
- **Duración**: Se elimina después del merge

#### `bugfix/*` - Corrección de Bugs
```bash
Ejemplos:
- bugfix/contact-form-validation
- bugfix/fitmaster-timeout
```
- **Origen**: Se crea desde `develop`
- **Destino**: Merge a `develop` via PR

#### `hotfix/*` - Correcciones Urgentes en Producción
```bash
Ejemplos:
- hotfix/security-vulnerability
- hotfix/critical-api-error
```
- **Origen**: Se crea desde `main`
- **Destino**: Merge a `main` Y `develop`
- **Uso**: Solo para emergencias en producción

#### `release/*` - Preparación de Release
```bash
Ejemplos:
- release/v1.2.0
- release/v2.0.0
```
- **Origen**: Se crea desde `develop`
- **Destino**: Merge a `main` y `develop`
- **Propósito**: Testing final, ajustes de versión

---

## 🔄 Flujo de Trabajo

### 1️⃣ Trabajar en una Nueva Feature

```bash
# Paso 1: Actualizar develop
git checkout develop
git pull origin develop

# Paso 2: Crear rama de feature
git checkout -b feature/nombre-descriptivo

# Paso 3: Desarrollar (hacer commits frecuentes)
git add .
git commit -m "feat: descripción del cambio"

# Paso 4: Push a remoto
git push origin feature/nombre-descriptivo

# Paso 5: Crear Pull Request en GitHub
# - Base: develop
# - Compare: feature/nombre-descriptivo
# - Agregar descripción detallada
# - Asignar reviewers si aplica

# Paso 6: Después del merge, limpiar
git checkout develop
git pull origin develop
git branch -d feature/nombre-descriptivo
```

### 2️⃣ Corregir un Bug

```bash
# Similar a feature, pero con prefijo bugfix/
git checkout develop
git pull origin develop
git checkout -b bugfix/descripcion-del-bug

# ... desarrollar fix ...

git add .
git commit -m "fix: descripción de la corrección"
git push origin bugfix/descripcion-del-bug

# Crear PR a develop
```

### 3️⃣ Hotfix Urgente en Producción

```bash
# Paso 1: Crear desde main
git checkout main
git pull origin main
git checkout -b hotfix/descripcion-urgente

# Paso 2: Fix rápido
git add .
git commit -m "hotfix: descripción del fix crítico"

# Paso 3: Push y PR a main
git push origin hotfix/descripcion-urgente

# Paso 4: Crear PR a main (URGENTE)
# Paso 5: Después del merge, también actualizar develop
git checkout develop
git pull origin develop
git merge main
git push origin develop
```

### 4️⃣ Crear un Release

```bash
# Paso 1: Crear rama de release desde develop
git checkout develop
git pull origin develop
git checkout -b release/v1.2.0

# Paso 2: Actualizar versión y changelog
# Editar VERSION, CHANGELOG.md, etc.
git add VERSION CHANGELOG.md
git commit -m "chore: Bump version to 1.2.0"

# Paso 3: Testing exhaustivo en staging

# Paso 4: PR a main
git push origin release/v1.2.0
# Crear PR: release/v1.2.0 → main

# Paso 5: Después del merge, crear tag
git checkout main
git pull origin main
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin main --tags

# Paso 6: Merge de vuelta a develop
git checkout develop
git merge main
git push origin develop

# Paso 7: Eliminar rama release
git branch -d release/v1.2.0
```

---

## 📝 Convenciones de Commits

Usamos **Conventional Commits** para mantener un historial claro:

### Tipos de Commit

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| `feat` | Nueva funcionalidad | `feat: Add Stripe payment integration` |
| `fix` | Corrección de bug | `fix: Resolve FitMaster JSON parsing error` |
| `hotfix` | Corrección urgente en producción | `hotfix: Add missing 're' import` |
| `docs` | Cambios en documentación | `docs: Update API endpoints documentation` |
| `style` | Formato, espacios (no afecta lógica) | `style: Fix PEP8 indentation warnings` |
| `refactor` | Refactorización sin cambiar funcionalidad | `refactor: Extract calculations to service layer` |
| `test` | Agregar o modificar tests | `test: Add unit tests for biometric service` |
| `chore` | Tareas de mantenimiento | `chore: Update dependencies` |
| `perf` | Mejoras de performance | `perf: Optimize database queries` |
| `ci` | Cambios en CI/CD | `ci: Add GitHub Actions workflow` |

### Formato del Commit

```bash
<tipo>: <descripción corta en presente>

[Cuerpo opcional con más detalles]

[Footer opcional: referencias a issues, breaking changes]
```

### Ejemplos Completos

```bash
# Commit simple
git commit -m "feat: Add user profile page"

# Commit con cuerpo
git commit -m "fix: Resolve database connection timeout

Added retry logic with exponential backoff.
Increased connection pool size to 20.

Closes #123"

# Breaking change
git commit -m "feat!: Change API authentication to JWT

BREAKING CHANGE: Old session-based auth is deprecated.
All clients must update to use JWT tokens."
```

---

## 🔐 Protección de Ramas

### Configuración en GitHub

#### Protección de `main` (Producción)

**Ruta en GitHub:** Settings → Branches → Add branch protection rule

**Branch name pattern:** `main`

**Reglas obligatorias:**

```yaml
Require a pull request before merging
   ├─ Require approvals: 1
   ├─ Dismiss stale pull request approvals when new commits are pushed
   └─ Require review from Code Owners

Require status checks to pass before merging
   ├─ Require branches to be up to date before merging
   ├─ Status checks required:
   │  ├─ test (Python tests)
   │  ├─ lint (Code style)
   │  └─ build (Build verification)

Require conversation resolution before merging

Require signed commits (recomendado)

Require linear history (evita merge commits)

Do not allow bypassing the above settings

Allow force pushes: NEVER
Allow deletions: NEVER
```

#### Protección de `develop` (Staging)

**Branch name pattern:** `develop`

**Reglas recomendadas:**

```yaml
Require a pull request before merging
   ├─ Require approvals: 1 (opcional si trabajas solo)
   └─ Require review from Code Owners

Require status checks to pass before merging
   ├─ Status checks required:
   │  ├─ test
   │  └─ lint

Require conversation resolution before merging

Allow force pushes: Only for administrators
Allow deletions: NEVER
```

#### Protección de Ramas Temporales (Patrón)

**Branch name pattern:** `feature/*` | `bugfix/*` | `hotfix/*`

```yaml
Require status checks to pass before merging
   └─ Status checks: test, lint

Allow force pushes: Enabled (para rebase)
Allow deletions: Enabled (limpieza después de merge)
```

### Auto-Delete Branches

**Configuración en GitHub:**

1. **Settings → General → Pull Requests**
2. **Automatically delete head branches**
   - Elimina automáticamente ramas después de merge
   - Solo aplica a ramas `feature/*`, `bugfix/*`, `hotfix/*`
   - NO elimina `main` ni `develop`

**Ventajas:**
- Mantiene el repositorio limpio
- Evita confusión con ramas obsoletas
- Reduce clutter en la lista de ramas

**Limpieza manual local:**
```bash
# Sincronizar ramas eliminadas remotamente
git fetch --prune

# Ver ramas que ya no existen en remoto
git branch -vv | grep ': gone]'

# Eliminar todas las ramas locales obsoletas
git branch -vv | grep ': gone]' | awk '{print $1}' | xargs git branch -D
```

---

## 👥 CODEOWNERS

El archivo `CODEOWNERS` define quién debe revisar cambios en áreas específicas del código.

### Crear archivo `.github/CODEOWNERS`

```bash
# CODEOWNERS - CoachBodyFit360
# Documentación: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners

# Regla por defecto: el owner principal revisa todo
* @pablotech80

# Backend Core
/app/ @pablotech80
/app/services/ @pablotech80
/app/models/ @pablotech80

# FitMaster AI (crítico)
/app/services/fitmaster_service.py @pablotech80
/app/services/fitmaster_prompt.txt @pablotech80

# Configuración y Deploy
/.github/ @pablotech80
/Procfile @pablotech80
/runtime.txt @pablotech80
/requirements.txt @pablotech80

# Base de datos
/migrations/ @pablotech80
/app/models/ @pablotech80

# Documentación
/docs/ @pablotech80
/README.md @pablotech80
/CONTRIBUTING.md @pablotech80

# Seguridad (requiere revisión extra)
/.env.example @pablotech80
/app/middleware/ @pablotech80
```

### Cómo funciona CODEOWNERS

1. **PR automático:** Al crear PR que toca archivos protegidos, GitHub asigna automáticamente reviewers
2. **Revisión obligatoria:** Si está habilitado "Require review from Code Owners", el PR no se puede mergear sin aprobación
3. **Múltiples owners:** Puedes asignar varios owners separados por espacios

**Ejemplo con equipo:**
```bash
# Si tuvieras un equipo
/app/services/fitmaster_service.py @pablotech80 @ai-team
/app/blueprints/api/ @pablotech80 @backend-team
```

---

## ✅ Checks Automáticos Pre-Merge

### Checks Requeridos (GitHub Actions)

Antes de mergear un PR, estos checks deben pasar:

#### 1. **Tests Unitarios** (`test`)
```yaml
Ejecuta: pytest
Verifica:
  - Todos los tests pasan
  - Cobertura mínima: 70%
  - No hay tests skipped sin razón
```

#### 2. **Linting** (`lint`)
```yaml
Ejecuta: flake8, black --check
Verifica:
  - Código sigue PEP 8
  - Sin errores de sintaxis
  - Sin imports no usados
  - Formato consistente
```

#### 3. **Type Checking** (`type-check`)
```yaml
Ejecuta: mypy (opcional)
Verifica:
  - Type hints correctos
  - Sin errores de tipado
```

#### 4. **Security Scan** (`security`)
```yaml
Ejecuta: bandit, safety
Verifica:
  - Sin vulnerabilidades conocidas
  - Dependencias actualizadas
  - Sin secretos hardcodeados
```

#### 5. **Build Verification** (`build`)
```yaml
Ejecuta: python -m compileall
Verifica:
  - Código compila sin errores
  - Imports resuelven correctamente
  - No hay errores de sintaxis
```

#### 6. **Database Migrations** (`migrations`)
```yaml
Ejecuta: flask db check
Verifica:
  - Migraciones son válidas
  - No hay conflictos
  - Pueden aplicarse sin errores
```

### Configuración de Checks en Branch Protection

**En GitHub Settings → Branches → Edit rule:**

```
Status checks that are required:
  ☑ test
  ☑ lint
  ☑ security
  ☑ build
  ☑ migrations (solo para PRs a main)
```

### Ejecutar Checks Localmente (Antes de Push)

```bash
# 1. Tests
pytest tests/ -v --cov=app --cov-report=term-missing

# 2. Linting
flake8 app/ tests/ --max-line-length=120
black app/ tests/ --check

# 3. Security
bandit -r app/ -ll
safety check

# 4. Build
python -m compileall app/

# 5. Migrations
flask db check

# Script todo-en-uno (crear en scripts/pre-push.sh)
./scripts/pre-push.sh
```

### Pre-commit Hooks (Automático)

Instalar pre-commit para ejecutar checks antes de cada commit:

```bash
# Instalar pre-commit
pip install pre-commit

# Crear .pre-commit-config.yaml (ver sección siguiente)
pre-commit install

# Ahora se ejecuta automáticamente en cada commit
git commit -m "feat: new feature"
# → Ejecuta: black, flake8, tests, etc.
```

### Bypass de Checks (Solo Emergencias)

```bash
# ⚠️ Solo usar en emergencias críticas
git push --no-verify

# O en PR: agregar label "skip-ci"
```

---

## 🚀 Entornos de Deploy

### Producción (`main`)
- **URL**: https://app.coachbodyfit360.com
- **Deploy**: Automático al hacer merge a `main`
- **Base de datos**: PostgreSQL (Railway)
- **Variables**: Configuradas en Railway

### Staging (`develop`)
- **URL**: https://staging.coachbodyfit360.com (si está configurado)
- **Deploy**: Automático al hacer merge a `develop`
- **Base de datos**: PostgreSQL staging
- **Propósito**: Testing antes de producción

### Local (desarrollo)
```bash
# Configurar entorno local
python -m venv venv1
source venv1/bin/activate
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar migraciones
flask db upgrade

# Correr servidor
python run.py
```

---

## 🛠️ Comandos Útiles

```bash
# Ver estado de ramas
git branch -a

# Ver historial gráfico
git log --oneline --graph --all

# Actualizar rama con cambios de develop
git checkout feature/mi-feature
git fetch origin
git rebase origin/develop

# Deshacer último commit (mantener cambios)
git reset --soft HEAD~1

# Ver diferencias antes de commit
git diff

# Ver qué archivos cambiarán
git status

# Limpiar ramas eliminadas remotamente
git fetch --prune
git branch -vv | grep ': gone]' | awk '{print $1}' | xargs git branch -d
```

---

## ❓ Preguntas Frecuentes

### ¿Cuándo usar `feature/` vs `bugfix/`?
- **feature/**: Funcionalidad nueva que agrega valor
- **bugfix/**: Corrige algo que no funciona correctamente

### ¿Cuándo usar `hotfix/`?
Solo para emergencias en producción que no pueden esperar al próximo release.

### ¿Puedo hacer push directo a `develop`?
No. Siempre usa Pull Requests para mantener trazabilidad.

### ¿Cómo sincronizo mi rama con `develop`?
```bash
git checkout feature/mi-feature
git fetch origin
git rebase origin/develop
# Resolver conflictos si hay
git push origin feature/mi-feature --force-with-lease
```

### ¿Qué hago si mi PR tiene conflictos?
```bash
git checkout feature/mi-feature
git fetch origin
git merge origin/develop
# Resolver conflictos manualmente
git add .
git commit -m "chore: Resolve merge conflicts"
git push origin feature/mi-feature
```

### ¿Qué pasa si los checks fallan?
1. Revisa los logs en GitHub Actions
2. Ejecuta los checks localmente para reproducir
3. Corrige los errores
4. Push nuevamente (los checks se re-ejecutan automáticamente)

### ¿Puedo mergear sin aprobación?
No en `main`. En `develop` depende de la configuración (si trabajas solo, puedes permitirlo).

---

## 📞 Contacto

Si tienes dudas sobre el proceso de contribución:
- **Email**: coachbodyfit@gmail.com
- **Issues**: Abre un issue en GitHub con la etiqueta `question`

---

**¡Gracias por contribuir a CoachBodyFit360!** 🎉
