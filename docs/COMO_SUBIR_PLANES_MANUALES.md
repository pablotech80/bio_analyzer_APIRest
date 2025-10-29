# 📝 Cómo Subir Planes Nutricionales y de Entrenamiento Manualmente

## 🎯 Resumen

Este sistema te permite como **admin/entrenador** crear y gestionar planes personalizados para tus clientes de forma manual. Los usuarios solo verán sus planes asignados.

---

## 🗄️ Estructura de Base de Datos

### Tabla `nutrition_plans`
Almacena planes nutricionales personalizados.

**Campos principales:**
- `title`: Título del plan (ej: "Plan Definición Marzo 2025")
- `description`: Descripción general
- `goal`: Objetivo (pérdida de grasa, ganancia muscular, etc)
- `daily_calories`: Calorías diarias objetivo
- `protein_grams`, `carbs_grams`, `fats_grams`: Macros diarios
- `meals`: JSON con array de comidas
- `notes`: Notas del entrenador
- `supplements`: Suplementación recomendada
- `start_date`, `end_date`: Vigencia del plan
- `is_active`: Plan activo o archivado

### Tabla `training_plans`
Almacena planes de entrenamiento personalizados.

**Campos principales:**
- `title`: Título del plan (ej: "Rutina Hipertrofia 4 días")
- `description`: Descripción general
- `goal`: Objetivo (hipertrofia, fuerza, resistencia)
- `frequency`: Frecuencia semanal (ej: "4 días/semana")
- `routine_type`: Tipo de rutina (PPL, Torso/Pierna, Full Body)
- `duration_weeks`: Duración en semanas
- `workouts`: JSON con array de entrenamientos
- `notes`: Notas del entrenador
- `warm_up`, `cool_down`: Calentamiento y enfriamiento
- `start_date`, `end_date`: Vigencia del plan
- `is_active`: Plan activo o archivado

---

## 🚀 Pasos para Implementar

### 1. Aplicar Migración

```bash
# Aplicar la migración para crear las tablas
flask db upgrade
```

### 2. Crear Planes desde Python Shell

```bash
# Abrir shell de Flask
flask shell
```

#### Ejemplo: Crear Plan Nutricional

```python
from app import db
from app.models.nutrition_plan import NutritionPlan
from app.models.user import User
from datetime import date

# Obtener usuario (cliente)
user = User.query.filter_by(email="cliente@example.com").first()

# Obtener admin (tú)
admin = User.query.filter_by(email="coachbodyfit@gmail.com").first()

# Crear plan nutricional
plan = NutritionPlan(
    user_id=user.id,
    created_by=admin.id,
    title="Plan Definición Marzo 2025",
    description="Plan personalizado para pérdida de grasa manteniendo masa muscular",
    goal="Pérdida de grasa corporal",
    daily_calories=2200,
    protein_grams=165,
    carbs_grams=220,
    fats_grams=73,
    meals=[
        {
            "name": "Desayuno",
            "time": "08:00",
            "foods": [
                "Avena 80g",
                "Claras de huevo 4u",
                "Plátano 1u",
                "Café con leche desnatada"
            ]
        },
        {
            "name": "Media Mañana",
            "time": "11:00",
            "foods": [
                "Yogur griego 0% 200g",
                "Frutos secos 30g",
                "Manzana 1u"
            ]
        },
        {
            "name": "Comida",
            "time": "14:00",
            "foods": [
                "Pechuga de pollo 200g",
                "Arroz integral 100g (peso cocido)",
                "Verduras al vapor",
                "Aceite de oliva 10ml"
            ]
        },
        {
            "name": "Merienda Pre-Entreno",
            "time": "17:00",
            "foods": [
                "Pan integral 60g",
                "Pavo 80g",
                "Plátano 1u"
            ]
        },
        {
            "name": "Cena",
            "time": "21:00",
            "foods": [
                "Salmón 180g",
                "Patata cocida 150g",
                "Ensalada variada",
                "Aceite de oliva 10ml"
            ]
        }
    ],
    supplements="- Proteína Whey: 1 scoop post-entreno\n- Creatina: 5g diarios\n- Omega 3: 2g diarios\n- Vitamina D: 2000 UI diarios",
    notes="Importante:\n- Beber mínimo 3L de agua al día\n- Ajustar carbos según actividad\n- Día de descanso: reducir carbos 20%\n- Pesarse cada lunes en ayunas",
    start_date=date(2025, 3, 1),
    end_date=date(2025, 4, 30),
    is_active=True
)

db.session.add(plan)
db.session.commit()

print(f"✅ Plan nutricional creado con ID: {plan.id}")
```

#### Ejemplo: Crear Plan de Entrenamiento

```python
from app.models.training_plan import TrainingPlan

# Crear plan de entrenamiento
plan = TrainingPlan(
    user_id=user.id,
    created_by=admin.id,
    title="Rutina Hipertrofia 4 días - PPL",
    description="Rutina Push/Pull/Legs enfocada en hipertrofia muscular",
    goal="Hipertrofia muscular",
    frequency="4 días por semana",
    routine_type="Push/Pull/Legs",
    duration_weeks=8,
    workouts=[
        {
            "day": "Lunes",
            "name": "Push (Pecho/Hombros/Tríceps)",
            "exercises": [
                {"name": "Press banca", "sets": 4, "reps": "8-10", "rest": "90s"},
                {"name": "Press inclinado mancuernas", "sets": 3, "reps": "10-12", "rest": "75s"},
                {"name": "Aperturas cable alto", "sets": 3, "reps": "12-15", "rest": "60s"},
                {"name": "Press militar", "sets": 4, "reps": "8-10", "rest": "90s"},
                {"name": "Elevaciones laterales", "sets": 3, "reps": "12-15", "rest": "60s"},
                {"name": "Fondos tríceps", "sets": 3, "reps": "10-12", "rest": "60s"},
                {"name": "Extensión tríceps polea", "sets": 3, "reps": "12-15", "rest": "60s"}
            ]
        },
        {
            "day": "Miércoles",
            "name": "Pull (Espalda/Bíceps)",
            "exercises": [
                {"name": "Dominadas", "sets": 4, "reps": "8-10", "rest": "90s"},
                {"name": "Remo con barra", "sets": 4, "reps": "8-10", "rest": "90s"},
                {"name": "Jalón al pecho", "sets": 3, "reps": "10-12", "rest": "75s"},
                {"name": "Remo mancuerna", "sets": 3, "reps": "10-12", "rest": "75s"},
                {"name": "Face pulls", "sets": 3, "reps": "15-20", "rest": "60s"},
                {"name": "Curl barra Z", "sets": 3, "reps": "10-12", "rest": "60s"},
                {"name": "Curl martillo", "sets": 3, "reps": "12-15", "rest": "60s"}
            ]
        },
        {
            "day": "Viernes",
            "name": "Legs (Piernas)",
            "exercises": [
                {"name": "Sentadilla", "sets": 4, "reps": "8-10", "rest": "120s"},
                {"name": "Prensa 45°", "sets": 4, "reps": "10-12", "rest": "90s"},
                {"name": "Peso muerto rumano", "sets": 3, "reps": "10-12", "rest": "90s"},
                {"name": "Extensión cuádriceps", "sets": 3, "reps": "12-15", "rest": "60s"},
                {"name": "Curl femoral", "sets": 3, "reps": "12-15", "rest": "60s"},
                {"name": "Elevación gemelos", "sets": 4, "reps": "15-20", "rest": "60s"}
            ]
        },
        {
            "day": "Domingo",
            "name": "Upper (Torso completo)",
            "exercises": [
                {"name": "Press banca inclinado", "sets": 3, "reps": "10-12", "rest": "75s"},
                {"name": "Remo gironda", "sets": 3, "reps": "10-12", "rest": "75s"},
                {"name": "Press Arnold", "sets": 3, "reps": "10-12", "rest": "75s"},
                {"name": "Jalón agarre cerrado", "sets": 3, "reps": "10-12", "rest": "75s"},
                {"name": "Fondos en paralelas", "sets": 3, "reps": "10-12", "rest": "75s"},
                {"name": "Curl inclinado", "sets": 3, "reps": "12-15", "rest": "60s"}
            ]
        }
    ],
    warm_up="- 5 min cardio ligero\n- Movilidad articular 5 min\n- Series de aproximación con peso ligero",
    cool_down="- Estiramientos estáticos 10 min\n- Foam roller grupos trabajados\n- Respiración profunda 3 min",
    notes="Importante:\n- Progresar peso cada semana si completas todas las reps\n- Descanso adecuado entre sesiones\n- Técnica perfecta antes de aumentar peso\n- Registrar pesos y reps en cada sesión",
    start_date=date(2025, 3, 1),
    end_date=date(2025, 4, 30),
    is_active=True
)

db.session.add(plan)
db.session.commit()

print(f"✅ Plan de entrenamiento creado con ID: {plan.id}")
```

### 3. Asociar Plan a un Análisis Biométrico (Opcional)

```python
# Si quieres vincular el plan a un análisis específico
from app.models.biometric_analysis import BiometricAnalysis

analysis = BiometricAnalysis.query.filter_by(user_id=user.id).order_by(BiometricAnalysis.created_at.desc()).first()

plan.analysis_id = analysis.id
db.session.commit()

print(f"✅ Plan vinculado al análisis {analysis.id}")
```

---

## 📱 Vista del Usuario

Los usuarios verán sus planes en:
- **Nutrición**: `/nutricion/mis-planes`
- **Entrenamiento**: `/entrenamiento/mis-planes`

Solo verán planes donde `user_id` coincida con su ID y `is_active=True`.

---

## 🔧 Gestión de Planes

### Desactivar un Plan

```python
plan = NutritionPlan.query.get(1)
plan.is_active = False
db.session.commit()
```

### Editar un Plan

```python
plan = NutritionPlan.query.get(1)
plan.daily_calories = 2400
plan.protein_grams = 180
db.session.commit()
```

### Listar Planes de un Usuario

```python
user = User.query.filter_by(email="cliente@example.com").first()

# Planes nutricionales
nutrition_plans = NutritionPlan.query.filter_by(user_id=user.id, is_active=True).all()
for p in nutrition_plans:
    print(f"- {p.title} ({p.daily_calories} kcal)")

# Planes de entrenamiento
training_plans = TrainingPlan.query.filter_by(user_id=user.id, is_active=True).all()
for p in training_plans:
    print(f"- {p.title} ({p.frequency})")
```

---

## 🚀 Próximos Pasos (Futuro)

1. **Panel Admin Web**: Crear interfaz gráfica para gestionar planes sin usar shell
2. **Plantillas de Planes**: Guardar plantillas reutilizables
3. **Copiar Planes**: Duplicar planes entre usuarios
4. **Historial de Cambios**: Tracking de modificaciones
5. **Notificaciones**: Avisar al usuario cuando se le asigna un plan nuevo
6. **Exportar a PDF**: Generar PDFs de los planes
7. **Integración FitMaster**: Generar planes automáticamente con IA

---

## ✅ Checklist de Implementación

- [x] Modelos `NutritionPlan` y `TrainingPlan` creados
- [x] Migración generada
- [ ] Aplicar migración: `flask db upgrade`
- [ ] Crear primer plan nutricional de prueba
- [ ] Crear primer plan de entrenamiento de prueba
- [ ] Verificar que el usuario ve sus planes
- [ ] Documentar estructura JSON de meals/workouts para tu equipo

---

## 📞 Soporte

Si necesitas ayuda para crear planes o tienes dudas sobre la estructura JSON, consulta los ejemplos en este documento o contacta al equipo de desarrollo.
