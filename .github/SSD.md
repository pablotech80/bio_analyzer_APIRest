# SSD — Guardrails & Agent Governance (CoachBodyFit360)
Versión: 1.0.0
Estado: Draft implementable
Owner: Backend/AI Team
Scope: Todos los flujos de IA (FitMaster y futuros agentes)

## 0. Objetivo
Definir guardrails por capas para operar agentes en producción con:
- Seguridad (prompt injection, PII, secrets, abuso)
- Calidad (outputs fiables, consistentes, validables)
- Coste controlado (tokens, latencia, rate limits)
- Observabilidad (trazas, auditoría, métricas)
- Evolución (versionado de prompts, evaluaciones, rollout)

---

## 1. Principios de diseño (L0)
- API-first y outputs estructurados (JSON estrictamente validable).
- Zero-trust para entradas de usuario y contexto externo.
- “Deny by default” para herramientas y datos sensibles.
- Reproducibilidad: prompts, modelos, plantillas y evaluaciones versionados.
- Separación de responsabilidades: Core dominio ≠ agente ≠ herramientas ≠ storage.

---

## 2. Catálogo de agentes y responsabilidades (L1)
### 2.1 Agentes (inicial)
- Agent: FitMaster
  - Rol: interpretación y recomendación basada en datos biométricos y objetivos.
  - Restricciones: no diagnósticos médicos; no prescripción clínica; no sustituye profesional sanitario.
- Agent: Coach Assistant (futuro)
  - Rol: micro-hábitos, adherencia, recordatorios, rutinas sugeridas.
- Agent: Support/Triage (futuro)
  - Rol: FAQs, soporte de cuenta, triage de incidencias.

### 2.2 Contratos por agente
Cada agente define:
- Inputs: esquema JSON (payload)
- Output: esquema JSON (respuesta)
- Tool policy: lista blanca de herramientas
- Data policy: qué datos puede leer/escribir
- Budget policy: tokens/latencia/coste

---

## 3. Guardrails de entrada (L2)
### 3.1 Normalización y validación
- Validar payload contra JSON Schema (hard fail si inválido).
- Normalizar unidades (kg/cm/%), rangos plausibles (min/max).
- Rechazar/limitar texto libre excesivo (p.ej. > N caracteres).

### 3.2 PII & Secrets
- Redacción/mascarado de PII en logs (email, teléfono, direcciones).
- Rechazar entrada que contenga secrets detectables (API keys, tokens).
- Política: el agente nunca recibe credenciales ni variables de entorno.

### 3.3 Prompt injection / Jailbreak
- Clasificador/reglas: detectar instrucciones tipo “ignora reglas”, “muéstrame tu prompt”, “dame credenciales”.
- Si se detecta: responder con mensaje seguro + continuar solo con tareas permitidas o abortar.
- El texto del usuario no se concatena sin delimitadores y roles.

---

## 4. Guardrails de contexto (L3)
### 4.1 Fuentes de verdad
- Datos biométricos: BD propia (read-only en el agente).
- Reglas de negocio: catálogo interno (versionado).
- Contenido externo: prohibido salvo fuentes whitelisted y con sanitización.

### 4.2 Minimización de contexto
- Enviar al modelo solo lo imprescindible:
  - métricas calculadas finales + objetivo + restricciones
  - nunca volcar historiales completos si no es necesario
- Enmascarar IDs internos y metadatos irrelevantes.

---

## 5. Guardrails de ejecución (L4)
### 5.1 Selección de modelo
- Política por entorno:
  - DEV: modelo económico
  - PROD: modelo estable y evaluado
- Fallback: si el modelo primario falla, degradar a uno secundario con límites.

### 5.2 Presupuestos
- max_tokens por agente y por endpoint
- timeout por request
- rate limit por usuario y por IP
- budget diario/semanal por tenant (si aplica)

### 5.3 Tooling policy (allowlist)
- El agente solo puede invocar herramientas explícitas:
  - (ej) calcular macros, construir plan, consultar historial resumido
- Prohibido:
  - acceso a filesystem del servidor
  - lectura de variables de entorno
  - llamadas HTTP arbitrarias sin proxy/control

---

## 6. Guardrails de salida (L5)
### 6.1 Output estructurado
- El modelo debe responder con JSON estricto según schema por agente.
- Validación:
  - Si JSON inválido -> retry con “repair prompt” (1 vez).
  - Si persiste -> fallback a respuesta segura (sin IA) o mensaje degradado.

### 6.2 Seguridad del contenido
- Bloquear:
  - recomendaciones peligrosas (extremos calóricos severos, sustancias, autolesión)
  - afirmaciones médicas/diagnósticos
  - contenido sexual explícito o ilegal
- Añadir disclaimers contextuales cuando aplique:
  - “orientativo” / “consulta profesional sanitario” en ámbitos clínicos.

### 6.3 Explicabilidad mínima
- Incluir campos:
  - “assumptions”
  - “confidence_band” (baja/media/alta)
  - “next_steps”
No revelar prompts internos ni políticas.

---

## 7. Observabilidad, auditoría y cumplimiento (L6)
### 7.1 Telemetría
Registrar por request:
- agent_name, agent_version, model, latency_ms
- prompt_tokens, completion_tokens, total_tokens, estimated_cost
- outcome: success / degraded / blocked
- reason_code: validation_failed / injection_detected / tool_denied / etc.

### 7.2 Auditoría
- Guardar:
  - payload sanitizado
  - output validado
  - trazas de decisión (reason codes)
- Retención configurable por entorno.

### 7.3 Alertas
- Spike de costes
- Aumento de “blocked/degraded”
- Latencia p95/p99
- Errores de validación de schema

---

## 8. Evaluación y calidad (L7)
- Test suites:
  - unit: validadores, schemas, policy engine
  - integration: flujos (login->analysis->ai->history)
  - eval set: prompts adversariales (injection), edge cases biométricos
- Métricas:
  - JSON validity rate
  - refusal correctness
  - adherence-to-policy rate
  - user satisfaction proxy (thumbs/feedback)

---

## 9. Versionado y rollout (L8)
- agent_version semver (MAJOR rompe schema/políticas).
- Canary rollout:
  - 5% tráfico -> 25% -> 100% si métricas OK
- Feature flags por agente y por entorno.

---

## 10. Implementación mínima (Checklist)
- [ ] Definir JSON Schemas por agente (input/output)
- [ ] Implementar Policy Engine (allowlist tools + budgets + injection checks)
- [ ] Implementar Output Validator + Repair (1 retry)
- [ ] Implementar Telemetry + Cost tracking
- [ ] Crear Eval set inicial + CI gate
