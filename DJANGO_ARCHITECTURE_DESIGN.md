# ARQUITECTURA DJANGO + SSD INTEGRADO
## CoachBodyFit360 - Diseño Multi-Tenant con AI Governance

**Versión:** 1.0.0  
**Fecha:** 20 Enero 2026  
**Estado:** Diseño aprobado para implementación

---

## 📋 DECISIONES ARQUITECTÓNICAS CLAVE

### 1. SSD desde el Inicio
✅ **Decisión:** Implementar SSD (Guardrails & Agent Governance) desde el día 1  
✅ **Nivel:** Mínimo obligatorio (L2 + L5 + L6) + esqueleto L0/L1/L4  
✅ **Enfoque:** Framework genérico para agentes, implementado inicialmente con FitMaster

### 2. Multi-Tenancy
✅ **Estrategia:** Row-level (campo `organization_id`)  
✅ **Razón:** Simplicidad + escalabilidad sin complejidad de schemas

### 3. Stack Tecnológico

**Backend:**
- Django 5.0+
- Django REST Framework (DRF) 3.14+
- PostgreSQL 15+
- Celery + Redis (tareas async)
- Pydantic v2 (validación L2/L5)

**AI Governance:**
- OpenTelemetry (telemetría neutral)
- Pydantic (validación de contratos)
- Sentry (errores + traces)
- Prometheus/Grafana (métricas agregadas)

**Frontend (Futuro):**
- Next.js 14 + React
- TailwindCSS + shadcn/ui

---

## 🏗️ ESTRUCTURA DEL PROYECTO

```
coachbodyfit_django/
├── manage.py
├── pyproject.toml
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
│
├── config/                          # Configuración Django
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── testing.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                            # Django Apps (Bounded Contexts)
│   │
│   ├── core/                        # 🔵 Shared Kernel
│   │   ├── domain/                  # Lógica de dominio pura
│   │   │   ├── biometrics/          # ✅ body_analysis/ de Flask
│   │   │   │   ├── calculators.py   # TMB, grasa, IMC, etc
│   │   │   │   ├── constants.py     # Enums, distribuciones macros
│   │   │   │   ├── interpretations.py
│   │   │   │   └── validators.py
│   │   │   └── nutrition/
│   │   │       └── macros.py
│   │   ├── infrastructure/
│   │   │   ├── storage/
│   │   │   │   └── s3_service.py    # ✅ Reutilizado de Flask
│   │   │   ├── email/
│   │   │   │   └── email_service.py # ⚠️ Adaptado de Flask
│   │   │   └── cache/
│   │   │       └── redis_client.py
│   │   └── utils/
│   │       ├── markdown.py          # ✅ Reutilizado
│   │       ├── file_upload.py       # ✅ Reutilizado
│   │       └── helpers.py
│   │
│   ├── accounts/                    # 🟢 Autenticación y Usuarios
│   │   ├── models.py                # User, Role, Permission
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── services.py
│   │   ├── permissions.py
│   │   └── tests/
│   │
│   ├── organizations/               # 🟡 Multi-Tenant (Gimnasios)
│   │   ├── models.py                # Organization, Membership
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── middleware.py            # Tenant isolation
│   │   ├── services.py
│   │   └── tests/
│   │
│   ├── biometrics/                  # 🔴 Análisis Biométricos
│   │   ├── models.py                # BiometricAnalysis
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── services/
│   │   │   ├── analysis_service.py  # ⚠️ Adaptado de Flask
│   │   │   └── calculator_service.py
│   │   └── tests/
│   │
│   ├── nutrition/                   # 🟠 Planes Nutricionales
│   │   ├── models.py                # NutritionPlan
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── services/
│   │   │   └── plan_service.py
│   │   └── tests/
│   │
│   ├── training/                    # 🟣 Planes de Entrenamiento
│   │   ├── models.py                # TrainingPlan
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── services/
│   │   │   └── plan_service.py
│   │   └── tests/
│   │
│   ├── messaging/                   # 💬 Comunicación
│   │   ├── models.py                # ContactMessage, Notification
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── tests/
│   │
│   ├── blog/                        # 📝 Contenido Educativo
│   │   ├── models.py                # BlogPost, MediaFile
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── tests/
│   │
│   ├── subscriptions/               # 💳 Pagos y Suscripciones
│   │   ├── models.py                # Plan, Subscription
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── services/
│   │   │   └── stripe_service.py
│   │   └── tests/
│   │
│   └── ai_governance/               # 🤖 AI Governance (SSD)
│       ├── __init__.py
│       ├── models.py                # Agent, AgentExecution, AgentAlert
│       ├── serializers.py
│       ├── views.py                 # Admin endpoints
│       │
│       ├── core/                    # L0: Principios
│       │   ├── agent_spec.py        # Contratos por agente
│       │   ├── agent_runner.py      # Pipeline genérico
│       │   └── policy_engine.py     # Enforcement de políticas
│       │
│       ├── guardrails/              # L2 + L5: Validación
│       │   ├── input_validator.py   # L2: Validación + normalización
│       │   ├── injection_detector.py # L2: Prompt injection
│       │   ├── pii_redactor.py      # L2: PII masking
│       │   ├── output_validator.py  # L5: JSON Schema + repair
│       │   └── content_filter.py    # L5: Seguridad contenido
│       │
│       ├── policies/                # L1 + L4: Políticas
│       │   ├── agent_policy.py      # L1: Contratos por agente
│       │   ├── tool_policy.py       # L4: Allowlist herramientas
│       │   └── budget_policy.py     # L4: Límites tokens/coste
│       │
│       ├── telemetry/               # L6: Observabilidad
│       │   ├── tracker.py           # Métricas OpenTelemetry
│       │   ├── auditor.py           # Auditoría de ejecuciones
│       │   └── alerting.py          # Alertas (coste, latencia, errores)
│       │
│       ├── agents/                  # Implementaciones de agentes
│       │   ├── fitmaster/
│       │   │   ├── agent.py         # FitMasterAgent
│       │   │   ├── schemas.py       # Pydantic schemas
│       │   │   ├── policy.py        # FitMasterPolicy
│       │   │   ├── prompt.txt       # ✅ Reutilizado de Flask
│       │   │   └── service.py       # ✅ Adaptado de Flask
│       │   └── base.py              # BaseAgent (interfaz)
│       │
│       └── tests/
│           ├── test_runner.py
│           ├── test_validators.py
│           └── test_policies.py
│
├── api/                             # API REST (DRF)
│   ├── v1/
│   │   ├── urls.py
│   │   ├── routers.py
│   │   ├── permissions.py
│   │   └── throttling.py
│   └── docs/                        # OpenAPI/Swagger
│
├── tasks/                           # Celery Tasks
│   ├── __init__.py
│   ├── ai_tasks.py                  # FitMaster async
│   ├── email_tasks.py
│   └── cleanup_tasks.py
│
└── tests/                           # Tests globales
    ├── integration/
    ├── e2e/
    └── fixtures/
```

---

## 🤖 ARQUITECTURA AI GOVERNANCE (SSD)

### Flujo de Ejecución de un Agente

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT REQUEST                           │
│          POST /api/v1/biometrics/analyze                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  DRF VIEW/VIEWSET                           │
│  - Autenticación JWT                                        │
│  - Permisos (IsAuthenticated + TenantIsolation)            │
│  - Serialización inicial                                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              BIOMETRIC SERVICE LAYER                        │
│  - Lógica de negocio                                        │
│  - Cálculos biométricos (core/domain)                      │
│  - Decisión: ¿Solicitar FitMaster AI?                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   AGENT RUNNER                              │
│  (ai_governance/core/agent_runner.py)                      │
│                                                             │
│  1. Load AgentSpec (FitMaster v1.0.0)                      │
│  2. Validate Input (L2)                                     │
│     ├─ JSON Schema validation                              │
│     ├─ Normalize units                                      │
│     ├─ Detect prompt injection                             │
│     └─ Redact PII                                           │
│                                                             │
│  3. Check Policies (L4)                                     │
│     ├─ Budget policy (tokens/coste)                        │
│     ├─ Rate limit (user/tenant)                            │
│     └─ Tool allowlist                                       │
│                                                             │
│  4. Build Context (L3)                                      │
│     ├─ Minimize context                                     │
│     ├─ Fetch only necessary data                           │
│     └─ Mask internal IDs                                    │
│                                                             │
│  5. Execute Agent (FitMaster)                               │
│     ├─ Build prompt from template                          │
│     ├─ Call OpenAI API (GPT-4o-mini)                       │
│     └─ Handle errors/timeouts                              │
│                                                             │
│  6. Validate Output (L5)                                    │
│     ├─ JSON Schema validation                              │
│     ├─ Content filter (dangerous content)                  │
│     ├─ Repair attempt (1 retry)                            │
│     └─ Fallback if invalid                                 │
│                                                             │
│  7. Track Telemetry (L6)                                    │
│     ├─ Log execution (tokens, latency, cost)               │
│     ├─ Audit payload/output                                │
│     ├─ Emit metrics (OpenTelemetry)                        │
│     └─ Check alerts (spike detection)                      │
│                                                             │
│  8. Return Result                                           │
│     └─ Structured response + metadata                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              BIOMETRIC SERVICE LAYER                        │
│  - Store result in BiometricAnalysis.fitmaster_data        │
│  - Update analysis status                                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  DRF SERIALIZER                             │
│  - Format response                                          │
│  - Return JSON                                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT RESPONSE                          │
│  {                                                          │
│    "status": "success",                                     │
│    "data": { ... },                                         │
│    "ai_metadata": {                                         │
│      "agent": "fitmaster",                                  │
│      "version": "1.0.0",                                    │
│      "confidence": "high",                                  │
│      "tokens_used": 1234                                    │
│    }                                                        │
│  }                                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 MODELOS DJANGO

### 1. AI Governance Models

```python
# apps/ai_governance/models.py

from django.db import models
from django.contrib.postgres.fields import JSONField
from apps.accounts.models import User

class Agent(models.Model):
    """
    L1: Catálogo de agentes con contratos y políticas
    """
    name = models.CharField(max_length=100, unique=True)
    version = models.CharField(max_length=20)  # Semver: 1.0.0
    description = models.TextField()
    
    # Contratos (JSON Schemas)
    input_schema = models.JSONField()
    output_schema = models.JSONField()
    
    # Políticas L4
    tool_allowlist = models.JSONField(default=list)
    max_tokens = models.IntegerField(default=2000)
    timeout_seconds = models.IntegerField(default=30)
    max_cost_per_request = models.DecimalField(max_digits=10, decimal_places=6)
    
    # Rollout (L8)
    is_active = models.BooleanField(default=False)
    rollout_percentage = models.IntegerField(default=0)  # 0-100
    
    # Metadata
    model_name = models.CharField(max_length=100)  # gpt-4o-mini
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ai_agents'
        unique_together = [['name', 'version']]
        indexes = [
            models.Index(fields=['name', 'is_active']),
        ]


class AgentExecution(models.Model):
    """
    L6: Telemetría y auditoría de ejecuciones
    """
    OUTCOME_CHOICES = [
        ('success', 'Success'),
        ('degraded', 'Degraded'),
        ('blocked', 'Blocked'),
        ('error', 'Error'),
    ]
    
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)
    
    # Input/Output (sanitizado)
    input_payload = models.JSONField()
    output_payload = models.JSONField(null=True)
    
    # Resultado
    outcome = models.CharField(max_length=20, choices=OUTCOME_CHOICES)
    reason_code = models.CharField(max_length=100, null=True)  # validation_failed, injection_detected, etc
    error_message = models.TextField(null=True)
    
    # Métricas
    prompt_tokens = models.IntegerField(default=0)
    completion_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    latency_ms = models.IntegerField()
    
    # Metadata
    model_used = models.CharField(max_length=100)
    request_id = models.UUIDField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ai_agent_executions'
        indexes = [
            models.Index(fields=['agent', 'created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['outcome', 'created_at']),
            models.Index(fields=['organization', 'created_at']),
        ]


class AgentAlert(models.Model):
    """
    L6: Alertas de anomalías
    """
    ALERT_TYPES = [
        ('cost_spike', 'Cost Spike'),
        ('latency_spike', 'Latency Spike'),
        ('error_rate', 'Error Rate'),
        ('invalid_output', 'Invalid Output'),
        ('injection_detected', 'Injection Detected'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    message = models.TextField()
    metadata = models.JSONField(default=dict)
    
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ai_agent_alerts'
        indexes = [
            models.Index(fields=['agent', 'is_resolved', 'created_at']),
        ]
```

### 2. Core Business Models (Migrados de Flask)

```python
# apps/accounts/models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Usuario con multi-tenant"""
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    # Multi-tenant
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)
    
    # Perfil
    profile_picture = models.ImageField(upload_to='profiles/', null=True)
    is_verified = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True)


# apps/biometrics/models.py
class BiometricAnalysis(models.Model):
    """Análisis biométrico completo"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)
    
    # Datos de entrada
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    neck = models.DecimalField(max_digits=5, decimal_places=2)
    waist = models.DecimalField(max_digits=5, decimal_places=2)
    hip = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    # Medidas musculares bilaterales
    biceps_left = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    biceps_right = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    thigh_left = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    thigh_right = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    calf_left = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    calf_right = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    # Métricas calculadas
    bmi = models.DecimalField(max_digits=5, decimal_places=2)
    bmr = models.DecimalField(max_digits=7, decimal_places=2)
    tdee = models.DecimalField(max_digits=7, decimal_places=2)
    body_fat_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    lean_mass = models.DecimalField(max_digits=5, decimal_places=2)
    fat_mass = models.DecimalField(max_digits=5, decimal_places=2)
    
    # FitMaster AI (JSON consolidado)
    fitmaster_data = models.JSONField(null=True)
    # Estructura:
    # {
    #   "interpretation": "...",
    #   "nutrition_plan": {...},
    #   "training_plan": {...},
    #   "generated_at": "ISO timestamp",
    #   "agent_version": "1.0.0",
    #   "confidence": "high"
    # }
    
    # Fotos S3
    front_photo_url = models.URLField(null=True)
    side_photo_url = models.URLField(null=True)
    back_photo_url = models.URLField(null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

---

## 🔐 CONTRATOS Y SCHEMAS (Pydantic)

```python
# apps/ai_governance/agents/fitmaster/schemas.py

from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from decimal import Decimal

class FitMasterInput(BaseModel):
    """
    L2: Contrato de entrada para FitMaster
    Validación estricta con Pydantic
    """
    # Datos básicos
    weight: Decimal = Field(..., gt=0, le=300, description="Peso en kg")
    height: Decimal = Field(..., gt=0, le=250, description="Altura en cm")
    age: int = Field(..., gt=0, le=120, description="Edad en años")
    gender: Literal["male", "female", "other"]
    
    # Medidas corporales
    neck: Decimal = Field(..., gt=0, le=100)
    waist: Decimal = Field(..., gt=0, le=200)
    hip: Optional[Decimal] = Field(None, gt=0, le=200)
    
    # Medidas musculares (opcionales)
    biceps_left: Optional[Decimal] = None
    biceps_right: Optional[Decimal] = None
    thigh_left: Optional[Decimal] = None
    thigh_right: Optional[Decimal] = None
    calf_left: Optional[Decimal] = None
    calf_right: Optional[Decimal] = None
    
    # Contexto
    activity_level: Literal["sedentary", "light", "moderate", "active", "very_active"]
    goal: Literal["lose_fat", "maintain", "gain_muscle"]
    
    # Métricas calculadas (pre-computed)
    bmi: Decimal
    bmr: Decimal
    tdee: Decimal
    body_fat_percentage: Decimal
    
    @validator('hip')
    def hip_required_for_females(cls, v, values):
        if values.get('gender') == 'female' and v is None:
            raise ValueError('Hip measurement required for females')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "weight": 75.5,
                "height": 175,
                "age": 30,
                "gender": "male",
                "neck": 38,
                "waist": 85,
                "activity_level": "moderate",
                "goal": "lose_fat",
                "bmi": 24.7,
                "bmr": 1750,
                "tdee": 2450,
                "body_fat_percentage": 18.5
            }
        }


class NutritionPlanOutput(BaseModel):
    """Plan nutricional generado por FitMaster"""
    daily_calories: int = Field(..., gt=0)
    protein_grams: int = Field(..., gt=0)
    carbs_grams: int = Field(..., gt=0)
    fats_grams: int = Field(..., gt=0)
    meals: list[dict]
    supplements: Optional[list[str]] = None


class TrainingPlanOutput(BaseModel):
    """Plan de entrenamiento generado por FitMaster"""
    frequency: str
    routine_type: str
    workouts: list[dict]
    warm_up: Optional[str] = None
    cool_down: Optional[str] = None


class FitMasterOutput(BaseModel):
    """
    L5: Contrato de salida para FitMaster
    Validación estricta del output de OpenAI
    """
    interpretation: str = Field(..., min_length=50, max_length=5000)
    nutrition_plan: NutritionPlanOutput
    training_plan: TrainingPlanOutput
    
    # Metadata
    confidence: Literal["low", "medium", "high"] = "medium"
    assumptions: list[str] = []
    disclaimers: list[str] = [
        "Esta es una recomendación orientativa.",
        "Consulta con un profesional sanitario antes de cambios drásticos."
    ]
    next_steps: list[str] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "interpretation": "Basado en tu análisis...",
                "nutrition_plan": {...},
                "training_plan": {...},
                "confidence": "high",
                "assumptions": ["Nivel de actividad declarado es preciso"],
                "next_steps": ["Seguir plan durante 4 semanas", "Re-evaluar progreso"]
            }
        }
```

---

## 🎯 AGENT RUNNER (Pipeline Genérico)

```python
# apps/ai_governance/core/agent_runner.py

from typing import Dict, Any, Optional
from pydantic import BaseModel, ValidationError
import uuid
import time
from opentelemetry import trace

from .agent_spec import AgentSpec
from .policy_engine import PolicyEngine
from ..guardrails.input_validator import InputValidator
from ..guardrails.output_validator import OutputValidator
from ..telemetry.tracker import TelemetryTracker
from ..models import AgentExecution

tracer = trace.get_tracer(__name__)


class AgentRunner:
    """
    Pipeline genérico para ejecutar agentes con SSD enforceado
    """
    
    def __init__(self, agent_spec: AgentSpec, policy_engine: PolicyEngine):
        self.agent_spec = agent_spec
        self.policy_engine = policy_engine
        self.input_validator = InputValidator(agent_spec)
        self.output_validator = OutputValidator(agent_spec)
        self.telemetry = TelemetryTracker()
    
    def execute(
        self,
        input_data: Dict[str, Any],
        user_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Ejecuta el agente con guardrails completos (L2-L6)
        
        Returns:
            {
                "status": "success" | "degraded" | "blocked",
                "data": {...},
                "metadata": {...}
            }
        """
        request_id = uuid.uuid4()
        start_time = time.time()
        
        with tracer.start_as_current_span("agent_execution") as span:
            span.set_attribute("agent.name", self.agent_spec.name)
            span.set_attribute("agent.version", self.agent_spec.version)
            span.set_attribute("request.id", str(request_id))
            
            try:
                # L2: Validate Input
                validated_input = self._validate_input(input_data, span)
                
                # L4: Check Policies
                self._check_policies(user_context, span)
                
                # L3: Build Context (minimize)
                context = self._build_context(validated_input, user_context)
                
                # Execute Agent
                raw_output = self._execute_agent(context, span)
                
                # L5: Validate Output
                validated_output = self._validate_output(raw_output, span)
                
                # L6: Track Telemetry
                latency_ms = int((time.time() - start_time) * 1000)
                self._track_execution(
                    request_id=request_id,
                    input_data=validated_input,
                    output_data=validated_output,
                    outcome="success",
                    latency_ms=latency_ms,
                    user_context=user_context
                )
                
                return {
                    "status": "success",
                    "data": validated_output,
                    "metadata": {
                        "agent": self.agent_spec.name,
                        "version": self.agent_spec.version,
                        "request_id": str(request_id),
                        "latency_ms": latency_ms
                    }
                }
                
            except ValidationError as e:
                return self._handle_validation_error(e, request_id, start_time)
            except PolicyViolation as e:
                return self._handle_policy_violation(e, request_id, start_time)
            except Exception as e:
                return self._handle_error(e, request_id, start_time)
    
    def _validate_input(self, input_data: Dict, span) -> BaseModel:
        """L2: Validación de entrada"""
        span.add_event("validating_input")
        return self.input_validator.validate(input_data)
    
    def _check_policies(self, user_context: Dict, span):
        """L4: Enforcement de políticas"""
        span.add_event("checking_policies")
        self.policy_engine.enforce(
            agent=self.agent_spec,
            user=user_context.get('user'),
            organization=user_context.get('organization')
        )
    
    def _build_context(self, validated_input: BaseModel, user_context: Dict) -> Dict:
        """L3: Construcción de contexto mínimo"""
        return {
            "input": validated_input.dict(),
            "user_id": user_context.get('user_id'),
            # NO incluir datos sensibles
        }
    
    def _execute_agent(self, context: Dict, span) -> Dict:
        """Ejecución del agente específico"""
        span.add_event("executing_agent")
        # Delegar a la implementación específica del agente
        return self.agent_spec.agent_instance.execute(context)
    
    def _validate_output(self, raw_output: Dict, span) -> BaseModel:
        """L5: Validación de salida con retry"""
        span.add_event("validating_output")
        return self.output_validator.validate_with_repair(raw_output)
    
    def _track_execution(self, **kwargs):
        """L6: Telemetría"""
        self.telemetry.track(**kwargs)
        AgentExecution.objects.create(**kwargs)
```

---

## 📊 TELEMETRÍA Y OBSERVABILIDAD

### OpenTelemetry Setup

```python
# config/telemetry.py

from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

def setup_telemetry():
    """Configurar OpenTelemetry para AI Governance"""
    
    # Traces
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter())
    )
    
    # Metrics
    metrics.set_meter_provider(MeterProvider())
    meter = metrics.get_meter(__name__)
    
    # Métricas custom para AI
    ai_request_counter = meter.create_counter(
        "ai.requests.total",
        description="Total AI agent requests"
    )
    
    ai_tokens_counter = meter.create_counter(
        "ai.tokens.total",
        description="Total tokens consumed"
    )
    
    ai_cost_counter = meter.create_counter(
        "ai.cost.total",
        description="Total estimated cost in USD"
    )
    
    ai_latency_histogram = meter.create_histogram(
        "ai.latency.ms",
        description="AI request latency in milliseconds"
    )
    
    return {
        "request_counter": ai_request_counter,
        "tokens_counter": ai_tokens_counter,
        "cost_counter": ai_cost_counter,
        "latency_histogram": ai_latency_histogram
    }
```

---

## 🚀 ROADMAP DE IMPLEMENTACIÓN

### R1: MVP Parity (4-6 semanas)

**Semana 1-2: Setup + Core**
- [ ] Crear proyecto Django con estructura propuesta
- [ ] Configurar PostgreSQL + Redis
- [ ] Migrar modelos: User, Organization, BiometricAnalysis
- [ ] Copiar `body_analysis/` (calculators) sin cambios
- [ ] Setup OpenTelemetry básico

**Semana 3-4: AI Governance (L2 + L5 + L6)**
- [ ] Implementar AgentSpec + AgentRunner
- [ ] Crear FitMasterAgent con schemas Pydantic
- [ ] Implementar InputValidator (L2)
- [ ] Implementar OutputValidator con repair (L5)
- [ ] Implementar TelemetryTracker (L6)
- [ ] Modelos: Agent, AgentExecution

**Semana 5-6: API REST + Tests**
- [ ] Endpoints DRF: análisis biométricos
- [ ] Integración FitMaster con AgentRunner
- [ ] Tests unitarios (validators, policies)
- [ ] Tests integración (flujo completo)
- [ ] Documentación OpenAPI

### R2: Multi-Tenant + Suscripciones (3-4 semanas)

- [ ] Middleware tenant isolation
- [ ] Modelos: NutritionPlan, TrainingPlan
- [ ] Endpoints planes (CRUD)
- [ ] Integración Stripe
- [ ] PolicyEngine con budgets por tenant
- [ ] Alerting (L6)

### R3: Evaluación + Rollout (2-3 semanas)

- [ ] Test suites adversariales (L7)
- [ ] Métricas de calidad
- [ ] Canary rollout (L8)
- [ ] Feature flags
- [ ] Dashboard admin para AI Governance

---

## ✅ CHECKLIST MÍNIMO OBLIGATORIO (SSD)

### L2: Guardrails de Entrada
- [x] JSON Schema validation con Pydantic
- [x] Normalización de unidades
- [ ] Detección básica de prompt injection
- [ ] Redacción de PII en logs

### L5: Guardrails de Salida
- [x] JSON Schema validation con Pydantic
- [x] Retry con repair (1 intento)
- [ ] Content filter (dangerous content)
- [x] Fallback seguro

### L6: Telemetría
- [x] Log de ejecuciones (AgentExecution model)
- [x] Métricas: tokens, latency, cost
- [x] Outcome + reason_code
- [ ] Alertas básicas (spike detection)

### L0/L1/L4: Esqueleto
- [x] AgentSpec (contratos)
- [x] AgentRunner (pipeline)
- [ ] PolicyEngine (budgets + rate limits)
- [ ] Tool allowlist

---

## 📝 PRÓXIMOS PASOS

1. **Crear estructura inicial Django** en `django_backend/`
2. **Implementar modelos core** (User, Organization, BiometricAnalysis)
3. **Copiar `body_analysis/`** directamente
4. **Implementar FitMasterAgent** con schemas Pydantic
5. **Crear AgentRunner** con validación L2 + L5
6. **Setup telemetría** básica (L6)
7. **Primer endpoint funcional:** `POST /api/v1/biometrics/analyze`

**¿Autorización para proceder con Paso 1?**
