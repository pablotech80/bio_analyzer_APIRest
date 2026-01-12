# 🚀 FASE 0: Plan de Migración Estratégica a Django SaaS

**Proyecto**: CoachBodyFit360 - Evolución a Plataforma SaaS Multi-Tenant  
**Fecha de Inicio**: [Fecha Actual]  
**Owner**: Pablo Techera (Entrenador, Nutriólogo, Backend Dev, GenAI Engineer)  
**Asistente IA**: Gemini Code Assist

---

## 🎯 Objetivo de la Fase 0

Definir el **plano arquitectónico completo** de la nueva plataforma SaaS. Esta fase es 100% estratégica y de diseño. No se escribe código de producción, pero se sientan las bases para que las Fases 1, 2 y 3 sean rápidas y eficientes.

**Resultado Esperado**: Un conjunto de documentos y diagramas validados que describen el QUÉ y el CÓMO vamos a construir.

---

## 📚 Capas de Trabajo y Tareas

### 1. Capa de Negocio y Lógica SaaS (Tu Expertise)

**Objetivo**: Traducir tu experiencia de 20 años en un modelo de negocio SaaS claro.

**Tareas Clave:**

- [x] **Definir el Modelo Multi-Tenant y Colaboración:**
  - **Decisión Clave**: ¿Cómo se agrupan los datos?
  - **Decisión Tomada (v2)**: Se usará un modelo de **Membresías** (`Membership`) para conectar `Users` y `Organizations` a través de una relación **Muchos-a-Muchos explícita**.
    - Un `User` puede tener múltiples `Membership` en diferentes `Organization`.
    - Cada `Membership` define el `role` del usuario dentro de esa organización específica (Cliente, Entrenador, Admin, etc.).
    - Esto permite la colaboración entre organizaciones (un cliente de un gimnasio puede ser paciente de una clínica) manteniendo el aislamiento de datos.
    - Cada `Organization` tiene un `org_type` (Gimnasio, Clínica, Entrenador, etc.).
  - **Estado**: ✅ **Validado por experto**.

- [x] **Definir Roles y Permisos Detallados:**
  - **Arquitectura de Permisos**: Se ha adoptado un modelo de **Roles Compuestos** con permisos granulares.
    - `Permission`: La acción atómica (ej: `plans.create_nutritionplan`).
    - `Role`: Un conjunto de `Permission`, personalizable por `Organization`.
    - `Membership`: Asigna uno o más `Role` a un `User` dentro de una `Organization`.
  - **Definición de Permisos**: La lista inicial de permisos CRUD ha sido definida.
    - **Ver Documento**: `docs/django_migration/permissions_definition.md`
  - **Estado**: ✅ **Validado**.

- [ ] **Estructurar Planes de Suscripción (Monetización):**
  - **Planes Propuestos**: `Free` (para clientes), `Pro` (para entrenadores individuales), `Business` (para gimnasios).
  - **Tu Decisión**: ¿Qué funcionalidades exactas limitan cada plan?
    - `Free`: ¿Cuántos análisis? ¿Acceso a IA limitado?
    - `Pro`: ¿Cuántos clientes? ¿Acceso a IA ilimitado? ¿Blog personal?
    - `Business`: ¿Cuántos entrenadores? ¿Dashboard de métricas del gimnasio?

---

### 2. Capa de Arquitectura y Modelo de Datos (Colaboración)

**Objetivo**: Diseñar el esquema de la base de datos en Django que soporte la lógica de negocio definida.

**Tareas Clave:**

- [ ] **Diseñar los Modelos de Django:**
  - **Mi Propuesta**: Generaré el código inicial de `models.py` para cada app de Django (`users`, `organizations`, `plans`, `analytics`, `blog`).
  - **Progreso**:
    - ✅ `docs/django_migration/models/organization_models.py`
    - ✅ `docs/django_migration/models/user_models.py`
  - **Tu Validación**: Revisarás cada campo, cada relación (`ForeignKey`, `ManyToManyField`) para asegurar que refleja la realidad de tu trabajo.

- [ ] **Diagrama Entidad-Relación (ERD):**
  - **Mi Tarea**: Generaré un diagrama visual (usando Mermaid.js) a partir de los modelos definidos.
  - **Tu Tarea**: Validarás visualmente que las conexiones entre `Entrenadores`, `Clientes`, `Planes` y `Gimnasios` son correctas.

- [ ] **Definir la Arquitectura de la API (DRF):**
  - **Mi Propuesta**: Esbozar la estructura de endpoints de la API con Django REST Framework, siguiendo un patrón como `/api/v1/organizations/{org_id}/clients/{client_id}/`.
  - **Tu Tarea**: Validar que los endpoints son lógicos y cubren las necesidades de un frontend moderno.

---

### 3. Capa de Tecnología y Despliegue (Decisión Estratégica)

**Objetivo**: Seleccionar el stack tecnológico final y la estrategia de despliegue para máxima escalabilidad.

**Tareas Clave:**

- [ ] **Confirmar el Stack Tecnológico:**
  - **Backend**: Django, DRF, PostgreSQL, Celery, Redis. (Propuesta firme)
  - **Frontend**: **Next.js (React)** con TypeScript. (Propuesta firme por su rendimiento y SEO).
  - **Tu Decisión**: ¿Estás de acuerdo con este stack? ¿Tienes alguna preferencia o experiencia con alternativas que debamos considerar?

- [x] **Definir la Arquitectura de Despliegue:**
  - **Decisión Tomada**: **Construir en Azure desde el Día 1**. Se prioriza la escalabilidad y la integración nativa con Azure OpenAI Service.
  - **Arquitectura Definida**: La arquitectura detallada para Azure está especificada en un nuevo documento.
    - **Ver Documento**: `docs/django_migration/azure_architecture.md`
  - **Estado**: ✅ **Validado por experto**.

---

### 4. Capa de Documentación y Agentes (Nuestro Contrato)

**Objetivo**: Actualizar los documentos clave para que reflejen la nueva visión y sirvan de guía para todo el desarrollo.

**Tareas Clave:**

- [x] **Actualizar `ssd.md` (System Specification Document):**
  - **Tarea**: Modificar el `ssd.md` para que la arquitectura objetivo sea Django + Next.js en Azure.
  - **Estado**: ✅ **Completado**.

- [x] **Actualizar `docs/AGENTS.md`:**
  - **Tarea**: Adaptar la sección de arquitectura, modelos y stack tecnológico a Django y Azure.
  - **Estado**: ✅ **Completado**.

- [x] **Definir el Rol del Agente `FitMaster AI` en la Nueva Arquitectura:**
  - **Propuesta**: `FitMaster AI` (el agente de OpenAI) ya no será llamado directamente desde el backend. Se convertirá en una "Tool" que consume la nueva API REST.
  - **Arquitectura Desacoplada**:
    1. El frontend (Next.js) se comunica con el `FitMaster AI` (OpenAI Assistants API).
    2. `FitMaster AI`, para obtener datos (`get_user_analysis`), llamará a nuestra API REST de Django (`GET /api/v1/clients/...`).
    3. Esto es crucial para que la IA sea un componente independiente y no una carga para el servidor principal.
  - **Estado**: ✅ **Validado por experto**.

---

## ✅ Checklist de Validación de la Fase 0

Al final de esta fase, debemos poder responder "SÍ" a todo lo siguiente:

- [x] ¿Tenemos un modelo de negocio SaaS (roles, permisos, planes) claramente definido?
- [x] ¿Los modelos de datos de Django reflejan fielmente la lógica del negocio del fitness?
- [x] ¿El diagrama ERD es correcto y está validado?
- [x] ¿El stack tecnológico (Django, Next.js, Azure) está confirmado?
-- [x] ¿La estrategia de despliegue está decidida?
- [x] ¿El rol y la arquitectura de `FitMaster AI` están claros?
- [x] ¿Los documentos `ssd.md` y `AGENTS.md` están actualizados y reflejan la nueva visión?

---

## 🚀 Próximo Paso

**FASE 0 COMPLETADA.**

El próximo paso es iniciar la **Fase 1: Construcción del Núcleo del Backend en Django**.

¡Vamos a construir la mejor herramienta del mercado!