# Agent.md — CoachBodyFit360

> **Documento de Contexto para Desarrollo Asistido por IA**  
> Última actualización: 2025-10-01  
> Versión: 2.0.0  
> Python: 3.13 | Flask: 3.0.3

---

## 📋 Tabla de Contenidos

1. [Visión General](#1-visión-general)
2. [Alcance Funcional](#2-alcance-funcional)
3. [Alcance Técnico](#3-alcance-técnico)
4. [Arquitectura del Sistema](#4-arquitectura-del-sistema)
5. [Modelos de Base de Datos](#5-modelos-de-base-de-datos)
6. [API Endpoints](#6-api-endpoints)
7. [Autenticación y Autorización](#7-autenticación-y-autorización)
8. [FitMaster AI Integration](#8-fitmaster-ai-integration)
9. [Testing Strategy (TDD)](#9-testing-strategy-tdd)
10. [Convenciones de Código](#10-convenciones-de-código)
11. [Variables de Entorno](#11-variables-de-entorno)
12. [Setup y Desarrollo](#12-setup-y-desarrollo)
13. [Deployment](#13-deployment)
14. [Roadmap](#14-roadmap)
15. [Troubleshooting](#15-troubleshooting)

---

## 1. Visión General

**CoachBodyFit360** es una aplicación web modular desarrollada en **Flask 3.0.3** con **Python 3.13**, diseñada para ofrecer un sistema integral de análisis corporal, nutrición, entrenamiento y seguimiento del progreso físico. La plataforma combina cálculos biométricos tradicionales con capacidades de **IA (FitMaster AI)** para proporcionar recomendaciones personalizadas.

### Objetivo Estratégico
Consolidarse como un **SaaS fitness ligero, escalable y flexible**, que pueda evolucionar desde un MVP funcional hacia un ecosistema completo para usuarios individuales, entrenadores, nutricionistas y centros deportivos.

### Propuesta de Valor
- ✅ **Simplicidad de Flask**: Rápido, ligero y fácil de extender
- ✅ **Arquitectura Modular**: Blueprints independientes y desacoplados
- ✅ **API-First**: Preparado para frontend React, apps móviles o integraciones
- ✅ **FitMaster AI**: Motor de recomendaciones avanzadas mediante GPT especializado
- ✅ **Escalabilidad**: De usuario individual a centros deportivos completos

---

## 2. Alcance Funcional

### 🔹 Módulo BioAnalyze
**Propósito**: Análisis antropométrico y biométrico completo.

**Funcionalidades**:
- Ingreso de medidas corporales (peso, altura, cuello, cintura, cadera, pliegues cutáneos)
- Cálculo automático de:
  - IMC (Índice de Masa Corporal)
  - TMB (Tasa Metabólica Basal) - Fórmulas: Harris-Benedict, Mifflin-St Jeor
  - Porcentaje de grasa corporal (Método Navy, Jackson-Pollock)
  - Masa magra y masa grasa
  - Edad metabólica
  - Peso ideal y peso objetivo
- Generación de reportes en HTML (con opción futura a PDF)
- Interpretaciones automáticas generadas por **FitMaster AI**

**Estado**: ✅ Funcional (Fase 1 completada)

---

### 🔹 Módulo Nutrition
**Propósito**: Planificación nutricional personalizada basada en objetivos.

**Funcionalidades**:
- Cálculo de macros (proteínas, carbohidratos, grasas) según objetivo:
  - Pérdida de grasa
  - Mantenimiento
  - Ganancia muscular
- Estrategias nutricionales avanzadas:
  - Ciclado de hidratos de carbono
  - Dieta mediterránea adaptada
  - Ayuno intermitente
  - Dieta cetogénica
- Plan de comidas con horarios y cantidades
- Recomendaciones de suplementación
- Historial de planes por usuario
- Ajustes dinámicos según progreso

**Estado**: 🔄 En desarrollo (Fase 2)

---

### 🔹 Módulo Training
**Propósito**: Rutinas de entrenamiento personalizadas y progresivas.

**Funcionalidades**:
- Creación de rutinas por nivel:
  - Principiante (Novato)
  - Intermedio
  - Avanzado
- Organización de entrenamientos:
  - Full Body (3x semana)
  - Push/Pull/Legs (PPL)
  - Torso/Pierna
  - Weider (músculos específicos por día)
- Cardio integrado (HIIT, LISS, MISS)
- Ejercicios de core y abdominales
- Progresión automática (sobrecarga progresiva)
- Biblioteca de ejercicios con descripciones y videos
- Tracking de pesos y repeticiones

**Estado**: 🔄 En desarrollo (Fase 2)

---

### 🔹 Módulo Users (Authentication)
**Propósito**: Gestión completa de usuarios y control de acceso.

**Funcionalidades**:
- Registro de usuarios con validación de email
- Login con email + contraseña (bcrypt)
- Recuperación de contraseña vía email
- Verificación de email con tokens
- Gestión de sesiones (Flask-Login + JWT)
- Sistema de roles y permisos:
  - **Cliente**: Acceso a sus propios análisis y planes
  - **Entrenador**: Gestión de múltiples clientes
  - **Nutricionista**: Creación de planes nutricionales
  - **Admin**: Control total del sistema
- Perfil editable con:
  - Datos personales
  - Objetivos fitness
  - Foto de perfil
  - Preferencias de notificaciones
- Dashboard personalizado por rol

**Estado**: 🚧 En desarrollo (Rama actual: `feature/flask-authentication`)

---

### 🔹 Módulo Historial
**Propósito**: Seguimiento temporal del progreso del usuario.

**Funcionalidades**:
- Almacenamiento de todos los análisis biométricos
- Registro de medidas periódicas (semanal/mensual)
- Visualización de evolución:
  - Gráficos de línea (peso, % grasa, medidas)
  - Comparativas antes/después
  - Estadísticas de progreso
- Exportación de datos (CSV, Excel)
- Fotos de progreso con comparador side-by-side
- Notas y observaciones del entrenador

**Estado**: ⚠️ Básico implementado → Mejoras en Fase 3

---

### 🔹 Módulo Notificaciones (Futuro)
**Propósito**: Comunicación y recordatorios automatizados.

**Funcionalidades planeadas**:
- Recordatorios de entrenamiento
- Notificaciones de comidas
- Alertas de citas con entrenador/nutricionista
- Sistema de mensajería interna (cliente ↔ profesional)
- Notificaciones push (web y móvil)
- Emails automatizados (bienvenida, resumen semanal)

**Estado**: 📅 Fase 3

---

### 🔹 Módulo Pagos (Futuro)
**Propósito**: Monetización y gestión de suscripciones.

**Funcionalidades planeadas**:
- Integración con Stripe y/o Redsys
- Planes de suscripción:
  - **Free**: Funcionalidades básicas limitadas
  - **Premium**: Acceso completo + FitMaster AI
  - **Pro**: Para entrenadores (multi-cliente)
  - **Business**: Para gimnasios y centros deportivos
- Facturación automática
- Gestión de pagos recurrentes
- Reportes financieros para admins

**Estado**: 📅 Fase 4

---

## 3. Alcance Técnico

### Stack Tecnológico

#### Backend
```python
# Core
Python: 3.13
Flask: 3.0.3
Flask-SQLAlchemy: 3.1.1
Flask-Migrate: 4.0.5

# Autenticación y Seguridad
Flask-Login: 0.6.3
Flask-Bcrypt: 1.0.1
Flask-JWT-Extended: 4.6.0
email-validator: 2.1.0

# Formularios y Validación
Flask-WTF: 1.2.1
WTForms: 3.1.0

# API y Documentación
Flask-RESTX: 1.3.0  # Swagger UI integrado
marshmallow: 3.20.0  # Serialización

# Utilidades
python-dotenv: 1.0.0
requests: 2.31.0  # Para FitMaster AI API
celery: 5.3.4  # Tareas asíncronas (futuro)
```

#### Base de Datos
```
Desarrollo: SQLite 3
Producción: PostgreSQL 15+
ORM: SQLAlchemy 2.0+
Migraciones: Alembic (vía Flask-Migrate)
```

#### Frontend (Actual)
```
Motor de plantillas: Jinja2
CSS: Bootstrap 5.3 / Tailwind CSS (evaluando)
JavaScript: Vanilla JS + Alpine.js (componentes reactivos ligeros)
Gráficos: Chart.js / Plotly.js
```

#### Frontend (Futuro - Fase 3)
```
Framework: React 18+ / Vue 3
Estado: Redux / Pinia
Build: Vite
UI Library: shadcn/ui / Material-UI
```

#### Infraestructura
```
Desarrollo Local: Flask Dev Server
Staging: Railway / Render
Producción: AWS
  - EC2 / ECS Fargate (aplicación)
  - RDS PostgreSQL (base de datos)
  - S3 (archivos estáticos, fotos)
  - CloudFront (CDN)
  - SES (emails)
  - CloudWatch (logs y monitoreo)
```

#### DevOps y CI/CD
```
Control de versiones: Git + GitHub
CI/CD: GitHub Actions
Contenedores: Docker + Docker Compose
Linting: black, isort, flake8, mypy
Testing: pytest, coverage
Documentación: Sphinx + MkDocs
```

---

## 4. Arquitectura del Sistema

### Arquitectura de Alto Nivel

```
CoachBodyFit360/
│
├── 🌐 Frontend (Jinja2 / React futuro)
│   ├── Templates
│   ├── Static Assets
│   └── Components
│
├── 🔧 Backend (Flask Application)
│   ├── API REST (JSON)
│   ├── Blueprints (Módulos)
│   ├── Services (Lógica de negocio)
│   ├── Models (SQLAlchemy)
│   └── Middleware (Auth, CORS, etc.)
│
├── 🗄️ Base de Datos (PostgreSQL)
│   ├── Users & Auth
│   ├── BioAnalyze Data
│   ├── Nutrition Plans
│   ├── Training Routines
│   └── History & Progress
│
├── 🤖 FitMaster AI (API Externa)
│   ├── GPT Especializado
│   ├── Análisis de datos
│   └── Recomendaciones
│
└── 📦 Servicios Externos
    ├── Email (AWS SES / SendGrid)
    ├── Storage (AWS S3)
    └── Payments (Stripe)
```

### Estructura de Directorios (Propuesta)

```
coachbodyfit360/
│
├── app/
│   ├── __init__.py                 # Application Factory
│   ├── config.py                   # Configuraciones por entorno
│   │
│   ├── models/                     # SQLAlchemy Models
│   │   ├── __init__.py
│   │   ├── user.py                 # User, Role, Permission
│   │   ├── bioanalyze.py           # BiometricAnalysis
│   │   ├── nutrition.py            # NutritionPlan, Meal
│   │   ├── training.py             # Workout, Exercise
│   │   └── history.py              # ProgressEntry, Measurement
│   │
│   ├── blueprints/                 # Módulos de la aplicación
│   │   ├── __init__.py
│   │   ├── auth/                   # Autenticación
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── forms.py
│   │   │   └── services.py
│   │   │
│   │   ├── bioanalyze/             # Análisis corporal
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── forms.py
│   │   │   ├── calculators.py      # Lógica de cálculos
│   │   │   └── services.py
│   │   │
│   │   ├── nutrition/              # Nutrición
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── services.py
│   │   │   └── meal_generator.py
│   │   │
│   │   ├── training/               # Entrenamiento
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── services.py
│   │   │   └── routine_builder.py
│   │   │
│   │   ├── users/                  # Perfiles y gestión
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── services.py
│   │   │
│   │   ├── history/                # Historial
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── analytics.py
│   │   │
│   │   └── api/                    # API REST (v1)
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── bioanalyze.py
│   │       └── schemas.py          # Marshmallow schemas
│   │
│   ├── services/                   # Servicios compartidos
│   │   ├── __init__.py
│   │   ├── fitmaster_ai.py         # Cliente API FitMaster
│   │   ├── email_service.py        # Envío de emails
│   │   ├── file_upload.py          # Gestión de archivos
│   │   └── report_generator.py     # PDFs/Reportes
│   │
│   ├── utils/                      # Utilidades
│   │   ├── __init__.py
│   │   ├── decorators.py           # @login_required, @role_required
│   │   ├── validators.py           # Validaciones custom
│   │   ├── constants.py            # Constantes del sistema
│   │   └── helpers.py              # Funciones auxiliares
│   │
│   ├── middleware/                 # Middleware
│   │   ├── __init__.py
│   │   ├── auth_middleware.py
│   │   ├── cors.py
│   │   └── error_handlers.py
│   │
│   ├── templates/                  # Jinja2 Templates
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── bioanalyze/
│   │   ├── nutrition/
│   │   ├── training/
│   │   └── dashboard/
│   │
│   └── static/                     # Assets estáticos
│       ├── css/
│       ├── js/
│       ├── images/
│       └── uploads/                # Archivos de usuario
│
├── tests/                          # Test Suite (TDD)
│   ├── __init__.py
│   ├── conftest.py                 # Fixtures compartidos
│   ├── unit/                       # Tests unitarios
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_calculators.py
│   ├── integration/                # Tests de integración
│   │   ├── test_auth_flow.py
│   │   ├── test_bioanalyze_flow.py
│   │   └── test_api_endpoints.py
│   └── e2e/                        # Tests end-to-end (Selenium)
│       └── test_user_journey.py
│
├── migrations/                     # Alembic migrations
│   └── versions/
│
├── docs/                           # Documentación
│   ├── agent.md                    # Este archivo
│   ├── ARCHITECTURE.md             # Arquitectura detallada
│   ├── API.md                      # Documentación de API
│   ├── DEVELOPMENT.md              # Guía de desarrollo
│   └── DEPLOYMENT.md               # Guía de deployment
│
├── scripts/                        # Scripts útiles
│   ├── init_db.py                  # Inicializar BD
│   ├── seed_data.py                # Datos de prueba
│   └── deploy.sh                   # Script de deployment
│
├── .github/                        # GitHub Actions
│   └── workflows/
│       ├── ci.yml                  # Tests automáticos
│       └── deploy.yml              # Deploy automático
│
├── .env.example                    # Variables de entorno (template)
├── .gitignore
├── requirements.txt                # Dependencias producción
├── requirements-dev.txt            # Dependencias desarrollo
├── pytest.ini                      # Configuración pytest
├── setup.py                        # Instalación del paquete
├── Dockerfile
├── docker-compose.yml
├── README.md
└── run.py                          # Entry point de la aplicación
```

### Patrón de Diseño: Application Factory

```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Inicialización de extensiones (sin app)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name='development'):
    """
    Application Factory Pattern.
    Permite crear múltiples instancias de la app con diferentes configs.
    """
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(f'app.config.{config_name.capitalize()}Config')
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Configurar Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder.'
    
    # Registrar Blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.bioanalyze import bioanalyze_bp
    from app.blueprints.nutrition import nutrition_bp
    from app.blueprints.training import training_bp
    from app.blueprints.users import users_bp
    from app.blueprints.history import history_bp
    from app.blueprints.api import api_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(bioanalyze_bp, url_prefix='/bioanalyze')
    app.register_blueprint(nutrition_bp, url_prefix='/nutrition')
    app.register_blueprint(training_bp, url_prefix='/training')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(history_bp, url_prefix='/history')
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Registrar error handlers
    from app.middleware.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    return app
```

---

## 5. Modelos de Base de Datos

### Modelo User (Autenticación)

```python
# app/models/user.py
from datetime import datetime
from app import db, login_manager, bcrypt
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model, UserMixin):
    """
    Modelo principal de usuario.
    Soporta múltiples roles y autenticación.
    """
    __tablename__ = 'users'
    
    # Identificación
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    _password_hash = db.Column('password_hash', db.String(255), nullable=False)
    
    # Información personal
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.Enum('male', 'female', 'other', name='gender_types'))
    
    # Foto de perfil
    profile_picture = db.Column(db.String(255))  # URL o path
    
    # Estado de la cuenta
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    email_verified_at = db.Column(db.DateTime)
    
    # Rol y permisos
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', back_populates='users')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Tokens de verificación/recuperación
    verification_token = db.Column(db.String(255))
    reset_password_token = db.Column(db.String(255))
    reset_password_expires = db.Column(db.DateTime)
    
    # Relaciones
    biometric_analyses = db.relationship('BiometricAnalysis', back_populates='user', lazy='dynamic')
    nutrition_plans = db.relationship('NutritionPlan', back_populates='user', lazy='dynamic')
    workouts = db.relationship('Workout', back_populates='user', lazy='dynamic')
    progress_entries = db.relationship('ProgressEntry', back_populates='user', lazy='dynamic')
    
    # Relación entrenador-cliente (para roles de entrenador)
    clients = db.relationship(
        'User',
        secondary='trainer_client',
        primaryjoin='User.id==trainer_client.c.trainer_id',
        secondaryjoin='User.id==trainer_client.c.client_id',
        backref='trainers'
    )
    
    @hybrid_property
    def password(self):
        """No permitir leer el password."""
        raise AttributeError('La contraseña no es un atributo legible')
    
    @password.setter
    def password(self, plaintext_password):
        """Hashear password al asignarlo."""
        self._password_hash = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')
    
    def check_password(self, plaintext_password):
        """Verificar password."""
        return bcrypt.check_password_hash(self._password_hash, plaintext_password)
    
    @property
    def full_name(self):
        """Nombre completo del usuario."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def has_role(self, role_name):
        """Verificar si el usuario tiene un rol específico."""
        return self.role and self.role.name == role_name
    
    def has_permission(self, permission_name):
        """Verificar si el usuario tiene un permiso específico."""
        return self.role and self.role.has_permission(permission_name)
    
    def __repr__(self):
        return f'<User {self.username}>'


# Tabla de asociación para relación muchos-a-muchos (entrenador-cliente)
trainer_client = db.Table(
    'trainer_client',
    db.Column('trainer_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('client_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('assigned_at', db.DateTime, default=datetime.utcnow)
)


class Role(db.Model):
    """
    Sistema de roles para control de acceso.
    """
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    
    # Relaciones
    users = db.relationship('User', back_populates='role')
    permissions = db.relationship('Permission', secondary='role_permissions', back_populates='roles')
    
    def has_permission(self, permission_name):
        """Verificar si el rol tiene un permiso específico."""
        return any(p.name == permission_name for p in self.permissions)
    
    def __repr__(self):
        return f'<Role {self.name}>'


class Permission(db.Model):
    """
    Permisos granulares del sistema.
    """
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    
    # Relaciones
    roles = db.relationship('Role', secondary='role_permissions', back_populates='permissions')
    
    def __repr__(self):
        return f'<Permission {self.name}>'


# Tabla de asociación para roles y permisos
role_permissions = db.Table(
    'role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)


@login_manager.user_loader
def load_user(user_id):
    """Callback requerido por Flask-Login."""
    return User.query.get(int(user_id))
```

### Modelo BiometricAnalysis

```python
# app/models/bioanalyze.py
from datetime import datetime
from app import db

class BiometricAnalysis(db.Model):
    """
    Análisis biométrico completo del usuario.
    """
    __tablename__ = 'biometric_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Medidas antropométricas básicas
    weight = db.Column(db.Float, nullable=False)  # kg
    height = db.Column(db.Float, nullable=False)  # cm
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum('male', 'female', name='gender_types'), nullable=False)
    
    # Medidas circunferenciales
    neck_circumference = db.Column(db.Float)  # cm
    waist_circumference = db.Column(db.Float)  # cm
    hip_circumference = db.Column(db.Float)  # cm
    
    # Pliegues cutáneos (mm)
    triceps_fold = db.Column(db.Float)
    subscapular_fold = db.Column(db.Float)
    suprailiac_fold = db.Column(db.Float)
    abdominal_fold = db.Column(db.Float)
    thigh_fold = db.Column(db.Float)
    
    # Resultados calculados
    bmi = db.Column(db.Float)  # Índice de Masa Corporal
    bmr = db.Column(db.Float)  # Tasa Metabólica Basal (kcal/día)
    body_fat_percentage = db.Column(db.Float)  # %
    lean_mass = db.Column(db.Float)  # kg
    fat_mass = db.Column(db.Float)  # kg
    metabolic_age = db.Column(db.Integer)  # años
    ideal_weight = db.Column(db.Float)  # kg
    
    # Nivel de actividad física (para cálculos de calorías)
    activity_level = db.Column(db.Enum(
        'sedentary',         # 1.2
        'lightly_active',    # 1.375
        'moderately_active', # 1.55
        'very_active',       # 1.725
        'extra_active',      # 1.9
        name='activity_levels'
    ))
    
    # Calorías diarias recomendadas
    tdee = db.Column(db.Float)  # Total Daily Energy Expenditure
    
    # Interpretación AI
    ai_interpretation = db.Column(db.Text)  # Análisis de FitMaster AI
    recommendations = db.Column(db.Text)  # Recomendaciones personalizadas
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    # Relaciones
    user = db.relationship('User', back_populates='biometric_analyses')
    
    def calculate_bmi(self):
        """Calcular IMC: peso(kg) / (altura(m))^2"""
        height_m = self.height / 100
        self.bmi = round(self.weight / (height_m ** 2), 2)
        return self.bmi
    
    def calculate_bmr(self, formula='mifflin'):
        """
        Calcular Tasa Metabólica Basal.
        Fórmulas: 'harris' (Harris-Benedict) o 'mifflin' (Mifflin-St Jeor)
        """
        if formula == 'mifflin':
            # Mifflin-St Jeor (más precisa)
            if self.gender == 'male':
                bmr = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5
            else:
                bmr = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) - 161
        else:
            # Harris-Benedict
            if self.gender == 'male':
                bmr = 88.362 + (13.397 * self.weight) + (4.799 * self.height) - (5.677 * self.age)
            else:
                bmr = 447.593 + (9.247 * self.weight) + (3.098 * self.height) - (4.330 * self.age)
        
        self.bmr = round(bmr, 2)
        return self.bmr
    
    def calculate_body_fat(self, method='navy'):
        """
        Calcular porcentaje de grasa corporal.
        Métodos: 'navy' (US Navy) o 'jackson' (Jackson-Pollock)
        """
        if method == 'navy' and all([self.neck_circumference, self.waist_circumference, self.height]):
            if self.gender == 'male':
                bf = 495 / (1.0324 - 0.19077 * math.log10(
                    self.waist_circumference - self.neck_circumference
                ) + 0.15456 * math.log10(self.height)) - 450
            else:
                if self.hip_circumference:
                    bf = 495 / (1.29579 - 0.35004 * math.log10(
                        self.waist_circumference + self.hip_circumference - self.neck_circumference
                    ) + 0.22100 * math.log10(self.height)) - 450
                else:
                    return None
            
            self.body_fat_percentage = round(max(0, min(bf, 100)), 2)
        
        elif method == 'jackson' and self.triceps_fold and self.suprailiac_fold:
            # Jackson-Pollock 3 pliegues
            sum_folds = self.triceps_fold + self.suprailiac_fold + self.thigh_fold
            if self.gender == 'male':
                density = 1.10938 - (0.0008267 * sum_folds) + (0.0000016 * sum_folds**2) - (0.0002574 * self.age)
            else:
                density = 1.0994921 - (0.0009929 * sum_folds) + (0.0000023 * sum_folds**2) - (0.0001392 * self.age)
            
            bf = ((4.95 / density) - 4.5) * 100
            self.body_fat_percentage = round(bf, 2)
        
        # Calcular masa magra y grasa
        if self.body_fat_percentage:
            self.fat_mass = round(self.weight * (self.body_fat_percentage / 100), 2)
            self.lean_mass = round(self.weight - self.fat_mass, 2)
        
        return self.body_fat_percentage
    
    def calculate_tdee(self):
        """Calcular gasto energético diario total."""
        if not self.bmr or not self.activity_level:
            return None
        
        activity_multipliers = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725,
            'extra_active': 1.9
        }
        
        multiplier = activity_multipliers.get(self.activity_level, 1.2)
        self.tdee = round(self.bmr * multiplier, 2)
        return self.tdee
    
    def get_bmi_category(self):
        """Obtener categoría de IMC según OMS."""
        if not self.bmi:
            return None
        
        if self.bmi < 18.5:
            return 'Bajo peso'
        elif 18.5 <= self.bmi < 25:
            return 'Peso normal'
        elif 25 <= self.bmi < 30:
            return 'Sobrepeso'
        elif 30 <= self.bmi < 35:
            return 'Obesidad grado I'
        elif 35 <= self.bmi < 40:
            return 'Obesidad grado II'
        else:
            return 'Obesidad grado III'
    
    def __repr__(self):
        return f'<BiometricAnalysis user_id={self.user_id} date={self.created_at}>'


import math  # Añadir al inicio del archivo
```

### Modelo NutritionPlan

```python
# app/models/nutrition.py
from datetime import datetime
from app import db

class NutritionPlan(db.Model):
    """
    Plan nutricional personalizado.
    """
    __tablename__ = 'nutrition_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Información general
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # Objetivo del plan
    goal = db.Column(db.Enum(
        'weight_loss',      # Pérdida de peso
        'maintenance',      # Mantenimiento
        'muscle_gain',      # Ganancia muscular
        'body_recomp',      # Recomposición corporal
        name='nutrition_goals'
    ), nullable=False)
    
    # Estrategia nutricional
    strategy = db.Column(db.Enum(
        'standard',           # Distribución estándar
        'carb_cycling',       # Ciclado de carbohidratos
        'mediterranean',      # Dieta mediterránea
        'intermittent_fasting', # Ayuno intermitente
        'ketogenic',          # Dieta cetogénica
        'paleo',              # Dieta paleo
        name='nutrition_strategies'
    ), default='standard')
    
    # Macronutrientes diarios (gramos)
    daily_calories = db.Column(db.Float, nullable=False)
    protein_grams = db.Column(db.Float, nullable=False)
    carbs_grams = db.Column(db.Float, nullable=False)
    fat_grams = db.Column(db.Float, nullable=False)
    fiber_grams = db.Column(db.Float)
    
    # Porcentajes de macros
    protein_percentage = db.Column(db.Float)
    carbs_percentage = db.Column(db.Float)
    fat_percentage = db.Column(db.Float)
    
    # Número de comidas diarias
    meals_per_day = db.Column(db.Integer, default=5)
    
    # Preferencias alimentarias
    dietary_restrictions = db.Column(db.JSON)  # ['vegetarian', 'gluten_free', etc.]
    allergies = db.Column(db.JSON)  # ['nuts', 'dairy', etc.]
    
    # Suplementación recomendada
    supplements = db.Column(db.JSON)  # [{'name': 'Whey Protein', 'dosage': '30g', 'timing': 'post-workout'}]
    
    # Hidratación
    daily_water_ml = db.Column(db.Float)
    
    # Estado del plan
    is_active = db.Column(db.Boolean, default=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    # AI insights
    ai_recommendations = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # Nutricionista que lo creó
    
    # Relaciones
    user = db.relationship('User', foreign_keys=[user_id], back_populates='nutrition_plans')
    creator = db.relationship('User', foreign_keys=[created_by])
    meals = db.relationship('Meal', back_populates='plan', cascade='all, delete-orphan')
    
    def calculate_macro_percentages(self):
        """Calcular porcentajes de macronutrientes."""
        total_cals_from_macros = (
            (self.protein_grams * 4) +
            (self.carbs_grams * 4) +
            (self.fat_grams * 9)
        )
        
        if total_cals_from_macros > 0:
            self.protein_percentage = round((self.protein_grams * 4 / total_cals_from_macros) * 100, 1)
            self.carbs_percentage = round((self.carbs_grams * 4 / total_cals_from_macros) * 100, 1)
            self.fat_percentage = round((self.fat_grams * 9 / total_cals_from_macros) * 100, 1)
    
    def __repr__(self):
        return f'<NutritionPlan {self.name} for user_id={self.user_id}>'


class Meal(db.Model):
    """
    Comida individual dentro de un plan nutricional.
    """
    __tablename__ = 'meals'
    
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('nutrition_plans.id'), nullable=False)
    
    # Información de la comida
    name = db.Column(db.String(100), nullable=False)  # "Desayuno", "Almuerzo", etc.
    meal_number = db.Column(db.Integer)  # Orden: 1, 2, 3...
    time = db.Column(db.Time)  # Hora recomendada
    
    # Contenido nutricional
    calories = db.Column(db.Float)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fat = db.Column(db.Float)
    
    # Alimentos
    foods = db.Column(db.JSON)  # [{'food': 'Pollo', 'quantity': '200g', 'calories': 330}]
    
    # Notas adicionales
    notes = db.Column(db.Text)
    preparation_tips = db.Column(db.Text)
    
    # Relaciones
    plan = db.relationship('NutritionPlan', back_populates='meals')
    
    def __repr__(self):
        return f'<Meal {self.name} in plan_id={self.plan_id}>'
```

### Modelo Workout (Training)

```python
# app/models/training.py
from datetime import datetime
from app import db

class Workout(db.Model):
    """
    Rutina de entrenamiento completa.
    """
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Información general
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # Tipo de rutina
    workout_type = db.Column(db.Enum(
        'full_body',        # Cuerpo completo
        'upper_lower',      # Torso/Pierna
        'push_pull_legs',   # PPL
        'body_part_split',  # Weider
        'custom',           # Personalizada
        name='workout_types'
    ), nullable=False)
    
    # Nivel de dificultad
    difficulty_level = db.Column(db.Enum(
        'beginner',
        'intermediate',
        'advanced',
        'expert',
        name='difficulty_levels'
    ), nullable=False)
    
    # Objetivo
    goal = db.Column(db.Enum(
        'strength',           # Fuerza
        'hypertrophy',        # Hipertrofia
        'endurance',          # Resistencia
        'weight_loss',        # Pérdida de peso
        'athletic_performance', # Rendimiento atlético
        name='training_goals'
    ), nullable=False)
    
    # Estructura
    days_per_week = db.Column(db.Integer, nullable=False)
    duration_weeks = db.Column(db.Integer)  # Duración total del programa
    rest_days = db.Column(db.JSON)  # [3, 7] = descanso miércoles y domingo
    
    # Estado
    is_active = db.Column(db.Boolean, default=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    # AI insights
    ai_recommendations = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relaciones
    user = db.relationship('User', foreign_keys=[user_id], back_populates='workouts')
    creator = db.relationship('User', foreign_keys=[created_by])
    training_days = db.relationship('TrainingDay', back_populates='workout', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Workout {self.name} for user_id={self.user_id}>'


class TrainingDay(db.Model):
    """
    Día específico de entrenamiento dentro de una rutina.
    """
    __tablename__ = 'training_days'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    
    # Información del día
    day_number = db.Column(db.Integer, nullable=False)  # 1, 2, 3...
    name = db.Column(db.String(100))  # "Día 1: Pecho y Tríceps"
    focus = db.Column(db.String(100))  # "Upper Body", "Legs", etc.
    
    # Duración estimada
    estimated_duration_minutes = db.Column(db.Integer)
    
    # Calentamiento
    warmup = db.Column(db.JSON)  # [{'exercise': 'Cardio', 'duration': '5min'}]
    
    # Ejercicios principales
    exercises = db.Column(db.JSON)  # Lista de ejercicios con sets, reps, peso
    # Ejemplo: [
    #   {
    #     'name': 'Press Banca',
    #     'sets': 4,
    #     'reps': '8-10',
    #     'rest_seconds': 90,
    #     'notes': 'Controlar la bajada',
    #     'video_url': 'https://...'
    #   }
    # ]
    
    # Cardio
    cardio = db.Column(db.JSON)  # {'type': 'HIIT', 'duration': '15min'}
    
    # Enfriamiento
    cooldown = db.Column(db.JSON)  # [{'exercise': 'Estiramiento', 'duration': '10min'}]
    
    # Notas
    notes = db.Column(db.Text)
    
    # Relaciones
    workout = db.relationship('Workout', back_populates='training_days')
    
    def __repr__(self):
        return f'<TrainingDay {self.day_number} of workout_id={self.workout_id}>'


class Exercise(db.Model):
    """
    Biblioteca de ejercicios disponibles.
    """
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Información básica
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    # Categorización
    muscle_group = db.Column(db.Enum(
        'chest', 'back', 'shoulders', 'arms', 'legs', 'core', 'full_body',
        name='muscle_groups'
    ), nullable=False)
    
    equipment = db.Column(db.Enum(
        'barbell', 'dumbbell', 'machine', 'cable', 'bodyweight', 'other',
        name='equipment_types'
    ))
    
    difficulty = db.Column(db.Enum(
        'beginner', 'intermediate', 'advanced',
        name='exercise_difficulty'
    ))
    
    # Media
    video_url = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    
    # Instrucciones
    instructions = db.Column(db.Text)
    tips = db.Column(db.Text)
    common_mistakes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Exercise {self.name}>'
```

### Modelo ProgressEntry (History)

```python
# app/models/history.py
from datetime import datetime
from app import db

class ProgressEntry(db.Model):
    """
    Entrada de progreso/seguimiento del usuario.
    """
    __tablename__ = 'progress_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Fecha de la medición
    entry_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    
    # Medidas corporales
    weight = db.Column(db.Float)
    body_fat_percentage = db.Column(db.Float)
    
    # Medidas circunferenciales
    chest = db.Column(db.Float)
    waist = db.Column(db.Float)
    hips = db.Column(db.Float)
    biceps_left = db.Column(db.Float)
    biceps_right = db.Column(db.Float)
    thigh_left = db.Column(db.Float)
    thigh_right = db.Column(db.Float)
    calf_left = db.Column(db.Float)
    calf_right = db.Column(db.Float)
    
    # Fotos de progreso
    front_photo = db.Column(db.String(255))
    side_photo = db.Column(db.String(255))
    back_photo = db.Column(db.String(255))
    
    # Métricas de rendimiento
    max_bench_press = db.Column(db.Float)
    max_squat = db.Column(db.Float)
    max_deadlift = db.Column(db.Float)
    
    # Estado general
    energy_level = db.Column(db.Integer)  # 1-10
    mood = db.Column(db.Enum('excellent', 'good', 'neutral', 'bad', 'terrible', name='mood_types'))
    sleep_hours = db.Column(db.Float)
    stress_level = db.Column(db.Integer)  # 1-10
    
    # Adherencia
    diet_compliance = db.Column(db.Integer)  # 1-10
    training_compliance = db.Column(db.Integer)  # 1-10
    
    # Notas
    notes = db.Column(db.Text)
    trainer_notes = db.Column(db.Text)  # Notas del entrenador
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    user = db.relationship('User', back_populates='progress_entries')
    
    def __repr__(self):
        return f'<ProgressEntry user_id={self.user_id} date={self.entry_date}>'
```

---

## 6. API Endpoints

### Autenticación (`/api/v1/auth`)

```
POST   /auth/register          # Registrar nuevo usuario
POST   /auth/login             # Iniciar sesión (devuelve JWT)
POST   /auth/logout            # Cerrar sesión
POST   /auth/refresh           # Refrescar token JWT
POST   /auth/forgot-password   # Solicitar recuperación de contraseña
POST   /auth/reset-password    # Restablecer contraseña con token
POST   /auth/verify-email      # Verificar email con token
GET    /auth/me                # Obtener usuario actual
PUT    /auth/me                # Actualizar perfil
PATCH  /auth/change-password   # Cambiar contraseña
```

### BioAnalyze (`/api/v1/bioanalyze`)

```
POST   /bioanalyze             # Crear nuevo análisis
GET    /bioanalyze             # Listar análisis del usuario
GET    /bioanalyze/:id         # Obtener análisis específico
PUT    /bioanalyze/:id         # Actualizar análisis
DELETE /bioanalyze/:id         # Eliminar análisis
GET    /bioanalyze/:id/report  # Generar reporte HTML/PDF
POST   /bioanalyze/:id/ai-insights # Solicitar análisis AI
```

### Nutrition (`/api/v1/nutrition`)

```
POST   /nutrition/plans        # Crear plan nutricional
GET    /nutrition/plans        # Listar planes del usuario
GET    /nutrition/plans/:id    # Obtener plan específico
PUT    /nutrition/plans/:id    # Actualizar plan
DELETE /nutrition/plans/:id    # Eliminar plan
POST   /nutrition/plans/:id/meals  # Agregar comida al plan
GET    /nutrition/calculator   # Calcular macros recomendados
POST   /nutrition/ai-plan      # Generar plan con AI
```

### Training (`/api/v1/training`)

```
POST   /training/workouts      # Crear rutina
GET    /training/workouts      # Listar rutinas
GET    /training/workouts/:id  # Obtener rutina específica
PUT    /training/workouts/:id  # Actualizar rutina
DELETE /training/workouts/:id  # Eliminar rutina
POST   /training/workouts/:id/days  # Agregar día de entrenamiento
GET    /training/exercises     # Listar todos los ejercicios
GET    /training/exercises/:id # Obtener ejercicio específico
POST   /training/ai-routine    # Generar rutina con AI
```

### Users (`/api/v1/users`)

```
GET    /users                  # Listar usuarios (Admin/Trainer)
GET    /users/:id              # Obtener usuario específico
PUT    /users/:id              # Actualizar usuario
DELETE /users/:id              # Eliminar usuario (Admin)
GET    /users/:id/clients      # Listar clientes de un entrenador
POST   /users/:id/assign-client # Asignar cliente a entrenador
```

### History (`/api/v1/history`)

```
POST   /history/progress       # Registrar entrada de progreso
GET    /history/progress       # Listar entradas de progreso
GET    /history/progress/:id   # Obtener entrada específica
PUT    /history/progress/:id   # Actualizar entrada
DELETE /history/progress/:id   # Eliminar entrada
GET    /history/charts         # Datos para gráficos de evolución
POST   /history/photos         # Subir foto de progreso
GET    /history/comparison     # Comparar dos periodos
```

---

## 7. Autenticación y Autorización

### Estrategia de Autenticación

**Sistema Híbrido:**
- **Flask-Login**: Sesiones para aplicación web tradicional
- **JWT (JSON Web Tokens)**: Para API REST y apps móviles

### Flujo de Autenticación (Web)

```
1. Usuario envía credenciales → POST /auth/login
2. Backend valida credenciales
3. Si válido:
   - Flask-Login crea sesión (cookie)
   - Se devuelve access_token JWT
4. Requests subsecuentes:
   - Web: Cookie de sesión automática
   - API: Header Authorization: Bearer <token>
```

### Estructura del JWT

```python
# Payload del token
{
    "sub": user_id,           # Subject (ID del usuario)
    "email": "user@email.com",
    "role": "client",
    "permissions": ["read:own_data", "write:own_data"],
    "iat": 1234567890,        # Issued at
    "exp": 1234571490         # Expiration (1 hora después)
}
```

### Sistema de Roles y Permisos

**Roles disponibles:**

1. **Client** (Cliente)
   - Usuario estándar de la plataforma
   - Acceso a sus propios datos personales y análisis
   - Puede crear y ver sus análisis biométricos
   - Puede ver planes de nutrición y entrenamiento asignados
   - Puede registrar su progreso personal
   - **Permisos:**
     - `read:own_profile` - Ver su propio perfil
     - `write:own_profile` - Editar su propio perfil
     - `read:own_analyses` - Ver sus análisis biométricos
     - `write:own_analyses` - Crear nuevos análisis biométricos
     - `read:own_plans` - Ver planes nutricionales y de entrenamiento asignados
     - `read:own_progress` - Ver su historial de progreso
     - `write:own_progress` - Registrar nuevas entradas de progreso

2. **Trainer** (Entrenador Personal)
   - Todos los permisos de Client, más:
   - Gestión de múltiples clientes asignados
   - Creación y asignación de rutinas de entrenamiento
   - Visualización del progreso de sus clientes
   - Agregar notas y observaciones a los análisis de clientes
   - **Permisos adicionales:**
     - `read:clients` - Ver lista de clientes asignados
     - `write:clients` - Editar información de clientes
     - `read:client_data` - Ver análisis y progreso de clientes
     - `write:training_plans` - Crear y editar planes de entrenamiento
     - `assign:training_plans` - Asignar planes de entrenamiento a clientes
     - `write:client_notes` - Agregar notas a perfiles de clientes

3. **Nutritionist** (Nutricionista/Dietista)
   - Todos los permisos de Client, más:
   - Gestión de clientes asignados
   - Creación y asignación de planes nutricionales personalizados
   - Visualización de análisis biométricos de clientes
   - Cálculo de macronutrientes y estrategias dietéticas
   - **Permisos adicionales:**
     - `read:clients` - Ver lista de clientes asignados
     - `write:clients` - Editar información de clientes
     - `read:client_data` - Ver análisis y progreso de clientes
     - `write:nutrition_plans` - Crear y editar planes nutricionales
     - `assign:nutrition_plans` - Asignar planes nutricionales a clientes
     - `write:client_notes` - Agregar notas nutricionales a perfiles

4. **Admin** (Administrador del Sistema)
   - Acceso completo y sin restricciones a toda la plataforma
   - Gestión de usuarios (crear, editar, eliminar, suspender)
   - Asignación de roles y permisos
   - Configuración del sistema y parámetros globales
   - Acceso a reportes y estadísticas globales
   - Gestión de la base de datos de ejercicios
   - Moderación de contenido
   - **Permisos:**
     - `admin:all` - Acceso total al sistema
     - `read:all_users` - Ver todos los usuarios
     - `write:all_users` - Editar cualquier usuario
     - `delete:users` - Eliminar usuarios
     - `manage:roles` - Gestionar roles y permisos
     - `read:system_config` - Ver configuración del sistema
     - `write:system_config` - Modificar configuración del sistema
     - `read:all_data` - Acceso de lectura a todos los datos
     - `write:all_data` - Acceso de escritura a todos los datos
     - `delete:all_data` - Eliminar cualquier dato
     - `view:analytics` - Ver estadísticas y reportes globales

### Matriz de Permisos por Rol

| Funcionalidad | Client | Trainer | Nutritionist | Admin |
|--------------|--------|---------|--------------|-------|
| Ver propio perfil | ✅ | ✅ | ✅ | ✅ |
| Editar propio perfil | ✅ | ✅ | ✅ | ✅ |
| Crear análisis biométricos propios | ✅ | ✅ | ✅ | ✅ |
| Ver propios análisis | ✅ | ✅ | ✅ | ✅ |
| Registrar progreso propio | ✅ | ✅ | ✅ | ✅ |
| Ver lista de clientes | ❌ | ✅ | ✅ | ✅ |
| Ver datos de clientes | ❌ | ✅ | ✅ | ✅ |
| Crear planes de entrenamiento | ❌ | ✅ | ❌ | ✅ |
| Asignar planes de entrenamiento | ❌ | ✅ | ❌ | ✅ |
| Crear planes nutricionales | ❌ | ❌ | ✅ | ✅ |
| Asignar planes nutricionales | ❌ | ❌ | ✅ | ✅ |
| Gestionar usuarios | ❌ | ❌ | ❌ | ✅ |
| Configurar sistema | ❌ | ❌ | ❌ | ✅ |
| Ver reportes globales | ❌ | ❌ | ❌ | ✅ |
| Eliminar datos | ❌ | ❌ | ❌ | ✅ |

### Relaciones entre Roles

**Asignación Trainer ↔ Cliente:**
- Un entrenador puede tener múltiples clientes
- Un cliente puede tener múltiples entrenadores
- Relación muchos-a-muchos en tabla `trainer_client`

**Asignación Nutritionist ↔ Cliente:**
- Un nutricionista puede tener múltiples clientes
- Un cliente puede tener múltiples nutricionistas
- Misma estructura que trainer-cliente

**Jerarquía de Roles:**
- Admin (acceso total)
 - ↓
 - Trainer / Nutritionist (acceso a clientes + permisos específicos)
 - ↓
 - Client (acceso solo a datos propios)
 - 
### Notas Importantes

1. **Roles Múltiples**: Un usuario puede tener solo UN rol principal. Si alguien es Trainer y Nutritionist, debe crearse una cuenta por cada rol o usar el rol Admin.

2. **Creación de Roles**: Los roles se crean automáticamente al inicializar la base de datos mediante el script `init_roles.py`.

3. **Rol por Defecto**: Al registrarse, todos los usuarios reciben el rol `Client` por defecto.

4. **Cambio de Rol**: Solo un Admin puede cambiar el rol de un usuario.

5. **Permisos Granulares**: Los permisos se verifican a nivel de ruta usando decoradores como `@role_required` y `@permission_required`.
