# 📋 Estructura JSON para Planes de Nutrición y Entrenamiento

## 🍽️ Plan Nutricional - Campo `meals` (JSON)

### Estructura Base

```json
[
  {
    "name": "Nombre de la comida",
    "time": "HH:MM (opcional)",
    "foods": ["Alimento 1", "Alimento 2", "..."],
    "description": "Descripción alternativa (opcional)"
  }
]
```

### Ejemplo Completo

```json
[
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
]
```

### Campos del Formulario Web

Cuando crees el plan desde el dashboard admin, necesitas estos campos:

**Campos Obligatorios:**
- `title` (texto): Título del plan
- `user_id` (número): ID del usuario (se selecciona del dashboard)

**Campos Opcionales:**
- `description` (texto largo): Descripción general
- `goal` (texto): Objetivo (ej: "Pérdida de grasa", "Ganancia muscular")
- `daily_calories` (número): Calorías diarias
- `protein_grams` (número): Proteínas en gramos
- `carbs_grams` (número): Carbohidratos en gramos
- `fats_grams` (número): Grasas en gramos
- `meals` (JSON): Array de comidas (ver estructura arriba)
- `supplements` (texto largo): Suplementación recomendada
- `notes` (texto largo): Notas del entrenador
- `start_date` (fecha): Fecha de inicio
- `end_date` (fecha): Fecha de fin
- `analysis_id` (número): ID del análisis relacionado (opcional)

---

## 🏋️ Plan de Entrenamiento - Campo `workouts` (JSON)

### Estructura Base

```json
[
  {
    "day": "Día de la semana",
    "name": "Nombre del entrenamiento",
    "exercises": [
      {
        "name": "Nombre del ejercicio",
        "sets": 4,
        "reps": "8-10",
        "rest": "90s",
        "notes": "Notas opcionales"
      }
    ]
  }
]
```

### Ejemplo Completo

```json
[
  {
    "day": "Lunes",
    "name": "Push (Pecho/Hombros/Tríceps)",
    "exercises": [
      {
        "name": "Press banca",
        "sets": 4,
        "reps": "8-10",
        "rest": "90s"
      },
      {
        "name": "Press inclinado mancuernas",
        "sets": 3,
        "reps": "10-12",
        "rest": "75s"
      },
      {
        "name": "Aperturas cable alto",
        "sets": 3,
        "reps": "12-15",
        "rest": "60s"
      },
      {
        "name": "Press militar",
        "sets": 4,
        "reps": "8-10",
        "rest": "90s"
      },
      {
        "name": "Elevaciones laterales",
        "sets": 3,
        "reps": "12-15",
        "rest": "60s"
      },
      {
        "name": "Fondos tríceps",
        "sets": 3,
        "reps": "10-12",
        "rest": "60s"
      }
    ]
  },
  {
    "day": "Miércoles",
    "name": "Pull (Espalda/Bíceps)",
    "exercises": [
      {
        "name": "Dominadas",
        "sets": 4,
        "reps": "8-10",
        "rest": "90s"
      },
      {
        "name": "Remo con barra",
        "sets": 4,
        "reps": "8-10",
        "rest": "90s"
      },
      {
        "name": "Jalón al pecho",
        "sets": 3,
        "reps": "10-12",
        "rest": "75s"
      },
      {
        "name": "Curl barra Z",
        "sets": 3,
        "reps": "10-12",
        "rest": "60s"
      }
    ]
  },
  {
    "day": "Viernes",
    "name": "Legs (Piernas)",
    "exercises": [
      {
        "name": "Sentadilla",
        "sets": 4,
        "reps": "8-10",
        "rest": "120s"
      },
      {
        "name": "Prensa 45°",
        "sets": 4,
        "reps": "10-12",
        "rest": "90s"
      },
      {
        "name": "Peso muerto rumano",
        "sets": 3,
        "reps": "10-12",
        "rest": "90s"
      },
      {
        "name": "Extensión cuádriceps",
        "sets": 3,
        "reps": "12-15",
        "rest": "60s"
      }
    ]
  }
]
```

### Campos del Formulario Web

**Campos Obligatorios:**
- `title` (texto): Título del plan
- `user_id` (número): ID del usuario

**Campos Opcionales:**
- `description` (texto largo): Descripción general
- `goal` (texto): Objetivo (ej: "Hipertrofia", "Fuerza", "Resistencia")
- `frequency` (texto): Frecuencia semanal (ej: "4 días/semana")
- `routine_type` (texto): Tipo de rutina (ej: "Push/Pull/Legs", "Torso/Pierna")
- `duration_weeks` (número): Duración en semanas
- `workouts` (JSON): Array de entrenamientos (ver estructura arriba)
- `warm_up` (texto largo): Calentamiento recomendado
- `cool_down` (texto largo): Enfriamiento/estiramiento
- `notes` (texto largo): Notas del entrenador
- `start_date` (fecha): Fecha de inicio
- `end_date` (fecha): Fecha de fin
- `analysis_id` (número): ID del análisis relacionado (opcional)

---

## 💡 Consejos para el Dashboard Admin

### Opción 1: Editor JSON Directo
- Campo de texto grande donde pegas el JSON
- Validación automática del JSON
- Preview del plan antes de guardar

### Opción 2: Formulario Dinámico
- Botones para agregar/quitar comidas o ejercicios
- Campos individuales que se convierten a JSON automáticamente
- Más user-friendly pero más complejo de implementar

### Opción 3: Plantillas Predefinidas
- Guardar plantillas de planes comunes
- Seleccionar plantilla y personalizar
- Rápido para planes similares

---

## 🎯 Ejemplo de Uso en Dashboard

```python
# En el formulario del dashboard, tendrías:

# PLAN NUTRICIONAL
title = "Plan Definición Juan"
daily_calories = 2200
protein_grams = 165
carbs_grams = 220
fats_grams = 73

# Campo JSON (textarea grande):
meals_json = '''
[
  {
    "name": "Desayuno",
    "time": "08:00",
    "foods": ["Avena 80g", "Claras 4u", "Plátano 1u"]
  },
  {
    "name": "Comida",
    "time": "14:00",
    "foods": ["Pollo 200g", "Arroz 100g", "Verduras"]
  }
]
'''

# Al guardar, el sistema convierte el texto JSON a objeto Python
import json
meals = json.loads(meals_json)

# Y crea el plan
plan = NutritionPlan(
    user_id=user_id,
    created_by=current_user.id,
    title=title,
    daily_calories=daily_calories,
    protein_grams=protein_grams,
    carbs_grams=carbs_grams,
    fats_grams=fats_grams,
    meals=meals  # ← Aquí va el JSON parseado
)
```

---

## ✅ Validación JSON

El dashboard debe validar que el JSON sea correcto antes de guardar:

```python
import json

def validate_meals_json(meals_str):
    """Valida que el JSON de comidas sea correcto"""
    try:
        meals = json.loads(meals_str)
        
        # Verificar que sea un array
        if not isinstance(meals, list):
            return False, "El JSON debe ser un array []"
        
        # Verificar estructura de cada comida
        for meal in meals:
            if 'name' not in meal:
                return False, "Cada comida debe tener 'name'"
            if 'foods' not in meal and 'description' not in meal:
                return False, "Cada comida debe tener 'foods' o 'description'"
        
        return True, meals
    except json.JSONDecodeError as e:
        return False, f"JSON inválido: {str(e)}"
```

---

## 📱 Vista del Usuario

El usuario verá los planes renderizados de forma bonita en:
- `/nutricion/mis-planes` - Lista de planes
- `/nutricion/plan/<id>` - Detalle con comidas en accordion
- `/entrenamiento/mis-planes` - Lista de rutinas
- `/entrenamiento/plan/<id>` - Detalle con ejercicios organizados por día

**No verán el JSON**, solo la información formateada y fácil de leer.
