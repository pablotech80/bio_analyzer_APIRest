# 🚀 CoachBodyFit360 - Roadmap Fases 3 y 4

**Continuación de**: [ROADMAP.md](./ROADMAP.md)

---

## 🔄 FASE 3: Migración a API REST + FitMaster Agent

**Estado**: ⏳ **Pendiente**  
**Duración estimada**: 3-4 semanas  
**Objetivo**: Desacoplar backend, frontend y FitMaster AI

### 3.1 Convertir Flask a API REST Pura

#### Estructura de Carpetas

```
app/
├── api/
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── auth.py          # Login, register, JWT
│   │   ├── users.py         # CRUD usuarios
│   │   ├── analyses.py      # CRUD análisis biométricos
│   │   ├── fitmaster.py     # Endpoints para FitMaster Agent
│   │   └── admin.py         # Endpoints admin
│   └── v2/                  # Futuras versiones
├── models/                  # Sin cambios
├── services/                # Sin cambios
└── middleware/              # JWT, CORS, rate limiting
```

#### Endpoints API REST v1

```python
# Autenticación
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
POST   /api/v1/auth/logout

# Usuarios
GET    /api/v1/users/me
PUT    /api/v1/users/me
DELETE /api/v1/users/me

# Análisis
GET    /api/v1/analyses              # Historial
POST   /api/v1/analyses              # Crear análisis
GET    /api/v1/analyses/:id          # Detalle
DELETE /api/v1/analyses/:id          # Eliminar
GET    /api/v1/analyses/progress     # Gráficas evolución

# FitMaster (para el Agent)
POST   /api/v1/fitmaster/analyze     # Agent solicita análisis
GET    /api/v1/fitmaster/user/:id    # Agent obtiene datos usuario
POST   /api/v1/fitmaster/save        # Agent guarda resultados

# Admin
GET    /api/v1/admin/users           # Lista usuarios
GET    /api/v1/admin/analyses        # Todos los análisis
GET    /api/v1/admin/stats           # Estadísticas
```

#### Autenticación JWT

```python
# app/middleware/jwt_auth.py
from functools import wraps
from flask import request, jsonify
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token missing'}), 401
        
        try:
            token = token.split(' ')[1]  # Bearer <token>
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], 
                            algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'error': 'Token invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated
```

#### Documentación con Swagger

```python
# pip install flasgger

from flasgger import Swagger

swagger = Swagger(app, template={
    "info": {
        "title": "CoachBodyFit360 API",
        "version": "1.0.0",
        "description": "API REST para análisis biométrico con IA"
    }
})
```

### 3.2 Crear FitMaster como OpenAI Agent

#### Arquitectura del Agent

```
FitMaster Agent (OpenAI Platform)
├── Instructions (Prompt del agent)
├── Tools/Functions:
│   ├── get_user_data(user_id)      → Llama a API
│   ├── get_analysis(analysis_id)   → Llama a API
│   ├── save_fitmaster_result()     → Llama a API
│   └── calculate_nutrition()       → Función interna
└── Model: gpt-4o-mini
```

#### Configuración del Agent en OpenAI

```json
{
  "name": "FitMaster",
  "instructions": "Eres FitMaster AI, un entrenador personal experto...",
  "model": "gpt-4o-mini",
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_user_biometric_data",
        "description": "Obtiene datos biométricos del usuario desde la API",
        "parameters": {
          "type": "object",
          "properties": {
            "user_id": {"type": "string"},
            "analysis_id": {"type": "string"}
          }
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "save_analysis_result",
        "description": "Guarda el resultado del análisis en la API",
        "parameters": {
          "type": "object",
          "properties": {
            "analysis_id": {"type": "string"},
            "interpretation": {"type": "string"},
            "nutrition_plan": {"type": "object"},
            "training_plan": {"type": "object"}
          }
        }
      }
    }
  ]
}
```

#### Ventajas del Agent

- ✅ Desacoplado del backend
- ✅ Escalable independientemente
- ✅ Más fácil de actualizar
- ✅ Puede tener conversaciones (futuro chatbot)
- ✅ OpenAI maneja la infraestructura

### 3.3 Estrategia de Migración

**Coexistencia temporal:**
1. Mantener templates mientras desarrollas React
2. API y templates funcionan en paralelo
3. Una vez React esté listo, eliminar templates
4. Mantener solo API REST

---

## 🎨 FASE 4: Frontend React + SaaS Completo

**Estado**: ⏳ **Pendiente**  
**Duración estimada**: 4-6 semanas  
**Objetivo**: Frontend profesional con dos roles y sistema de pagos

### 4.1 Stack Tecnológico Frontend

```
Frontend Stack:
├── Framework: Next.js 14 (App Router)
├── UI Library: shadcn/ui + Tailwind CSS
├── State Management: Zustand o React Context
├── API Client: Axios + React Query
├── Auth: JWT + Refresh tokens
├── Charts: Recharts o Chart.js
├── Forms: React Hook Form + Zod
└── Deploy: Vercel
```

### 4.2 Estructura del Proyecto React

```
coachbodyfit360-frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   └── register/
│   ├── (dashboard)/
│   │   ├── cliente/
│   │   │   ├── analisis/
│   │   │   ├── progreso/
│   │   │   └── planes/
│   │   └── admin/
│   │       ├── usuarios/
│   │       ├── analisis/
│   │       └── estadisticas/
│   └── (public)/
│       ├── page.tsx          # Landing
│       ├── precios/
│       └── contacto/
├── components/
│   ├── ui/                   # shadcn components
│   ├── charts/
│   ├── forms/
│   └── layout/
├── lib/
│   ├── api.ts               # Axios instance
│   ├── auth.ts              # JWT handling
│   └── utils.ts
└── hooks/
    ├── useAuth.ts
    ├── useAnalyses.ts
    └── useFitMaster.ts
```

### 4.3 Dashboards por Rol

#### Dashboard Cliente

- Crear nuevo análisis
- Ver historial de análisis
- Gráficas de progreso
- Planes nutricionales actuales
- Planes de entrenamiento
- Configuración de perfil

#### Dashboard Admin (Entrenador)

- Lista de todos los clientes
- Análisis de todos los usuarios
- Estadísticas globales
- Gestión de mensajes
- Métricas de uso de FitMaster AI
- Configuración de planes (FREE vs PREMIUM)

### 4.4 Sistema de Suscripciones

#### Planes

```typescript
// Plan FREE
{
  name: "Free",
  price: 0,
  features: [
    "1 análisis al mes",
    "Interpretación básica",
    "Historial limitado (últimos 3)"
  ]
}

// Plan PREMIUM
{
  name: "Premium",
  price: 9.99,
  currency: "EUR",
  interval: "month",
  features: [
    "Análisis ilimitados",
    "FitMaster AI completo",
    "Planes personalizados",
    "Seguimiento de progreso",
    "Soporte prioritario",
    "Comparativas históricas"
  ]
}
```

#### Integración Stripe

```python
# Backend: app/api/v1/subscriptions.py
import stripe

@subscriptions_bp.route('/create-checkout-session', methods=['POST'])
@token_required
def create_checkout_session(current_user):
    session = stripe.checkout.Session.create(
        customer_email=current_user.email,
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_XXXXXXXXX',  # Stripe Price ID
            'quantity': 1,
        }],
        mode='subscription',
        success_url='https://app.coachbodyfit360.com/success',
        cancel_url='https://app.coachbodyfit360.com/cancel',
    )
    return jsonify({'sessionId': session.id})
```

---

## 📅 Timeline Estimado

```
┌─────────────────────────────────────────────────────┐
│ FASE 2: COMPLETAR BIOANALYZE                        │
│ Duración: 2-3 semanas                               │
│ ├── Semana 1: UI/UX + Landing + Legal              │
│ ├── Semana 2: Sistema de progreso + Gráficas       │
│ └── Semana 3: Testing + Optimizaciones             │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ LANZAMIENTO MVP (Soft Launch)                       │
│ Duración: 1 semana                                  │
│ └── Usuarios beta + Feedback + Correcciones        │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ FASE 3: API REST + FITMASTER AGENT                  │
│ Duración: 3-4 semanas                               │
│ ├── Semana 1-2: Convertir a API REST + JWT         │
│ ├── Semana 3: Crear FitMaster Agent en OpenAI      │
│ └── Semana 4: Testing + Documentación Swagger      │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ FASE 4: FRONTEND REACT + SAAS                       │
│ Duración: 4-6 semanas                               │
│ ├── Semana 1-2: Setup Next.js + Componentes base   │
│ ├── Semana 3-4: Dashboards (Cliente + Admin)       │
│ ├── Semana 5: Integración Stripe + Suscripciones   │
│ └── Semana 6: Testing + Deploy + Lanzamiento       │
└─────────────────────────────────────────────────────┘

TOTAL: 10-14 semanas (~3 meses)
```

---

## 🛠️ Stack Tecnológico Completo

### Backend (Fase 1-3)

```
Flask==3.1.2
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-Migrate==4.1.0
Flask-JWT-Extended==4.7.1
Flask-CORS==6.0.1
openai==2.2.0
psycopg2-binary==2.9.9
gunicorn==23.0.0
flasgger==0.9.7
```

### Frontend (Fase 4)

```
Next.js 14
React 18
TypeScript
Tailwind CSS
shadcn/ui
React Query
Axios
Recharts
Stripe.js
```

### Infraestructura

```
Backend: Railway
Frontend: Vercel
Database: PostgreSQL (Railway)
AI Agent: OpenAI Platform
DNS: Cloudflare
Payments: Stripe
```

---

## 🎯 Próximos Pasos Inmediatos

### Esta Semana (Fase 2)

1. **Landing Page** (2-3 días)
   - Hero section atractivo
   - Sección de características
   - CTA claro

2. **Legal Básico** (1 día)
   - Política de Privacidad
   - Términos y Condiciones
   - Disclaimer médico

3. **Sistema de Progreso** (3-4 días)
   - Página de evolución
   - Gráficas básicas
   - Comparativa de análisis

### Próximo Mes (Fase 3)

1. Documentar API REST con Swagger
2. Implementar autenticación JWT
3. Crear FitMaster Agent en OpenAI
4. Testing completo de API

### Próximos 2-3 Meses (Fase 4)

1. Setup proyecto Next.js
2. Implementar dashboards
3. Integrar Stripe
4. Lanzamiento SaaS completo

---

## 📊 Métricas de Éxito

### MVP (Fase 2)
- 🎯 50-100 registros
- 🎯 200-500 análisis completados
- 🎯 20-30% uso de FitMaster AI
- 🎯 5-10 testimonios positivos

### SaaS (Fase 4)
- 🎯 500+ usuarios registrados
- 🎯 50+ suscriptores premium
- 🎯 MRR: €500+
- 🎯 Churn rate: <10%

---

## 💡 Recomendaciones

1. **Enfócate en Fase 2 ahora**: Completa el MVP antes de migrar
2. **Lanza temprano**: No esperes perfección
3. **Itera basándote en feedback**: Usuarios reales > Suposiciones
4. **Documenta todo**: Facilitará la migración a API REST
5. **Mantén código limpio**: Aplicar propuestas pendientes

---

**Volver a**: [ROADMAP.md](./ROADMAP.md)
