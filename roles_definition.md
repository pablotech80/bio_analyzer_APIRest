# 📜 Definición de Roles por Defecto (Fase 0)

**Proyecto**: CoachBodyFit360 - Evolución a Plataforma SaaS Multi-Tenant  
**Owner**: Pablo Techera

---

## 🎯 Objetivo

Definir los roles predeterminados que se crearán para cada nueva `Organization`. Estos roles agrupan los `Permissions` definidos en `permissions_definition.md` y sirven como plantillas que los administradores de la organización pueden personalizar.

---

## 🏛️ Roles por Defecto

### 1. Rol: `Admin`
**Propósito**: Gestión completa de la organización. Asignado por defecto al `owner` de la organización y a otros usuarios de confianza. **Este es el rol que gestiona la facturación y suscripción de la organización con la plataforma.**

**Permisos Incluidos**:
- **Gestión de Clientes:**
  - `clients.view_client`, `clients.edit_client`, `clients.assign_client`, `clients.remove_client`, `clients.view_client_progress`
- **Gestión de Planes (CRUD Completo):**
  - `plans.view_nutritionplan`, `plans.create_nutritionplan`, `plans.edit_nutritionplan`, `plans.delete_nutritionplan`, `plans.assign_nutritionplan`, `plans.duplicate_nutritionplan`
  - `plans.view_trainingplan`, `plans.create_trainingplan`, `plans.edit_trainingplan`, `plans.delete_trainingplan`, `plans.assign_trainingplan`, `plans.duplicate_trainingplan`
- **Gestión de Análisis (CRUD Completo):**
  - `analyses.view_analysis`, `analyses.create_analysis`, `analyses.delete_analysis`, `analyses.request_ai_interpretation`
- **Gestión de Blog (CRUD Completo):**
  - `blog.view_blogpost`, `blog.create_blogpost`, `blog.edit_blogpost`, `blog.delete_blogpost`, `blog.publish_blogpost`
- **Gestión de la Organización (Permisos Clave):**
  - `organization.manage_members`
  - `organization.manage_roles`
  - `organization.edit_settings`
  - `organization.view_billing`
  - `organization.manage_billing`

### 2. Rol: `Entrenador`
**Propósito**: Rol profesional enfocado en la gestión del entrenamiento de los clientes. Tiene acceso de lectura a planes de nutrición para una visión 360°, pero no puede editarlos.

**Permisos Incluidos**:
- **Gestión de Clientes:**
  - `clients.view_client`, `clients.edit_client`, `clients.view_client_progress`
- **Gestión de Planes de Entrenamiento (CRUD Completo):**
  - `plans.view_trainingplan`, `plans.create_trainingplan`, `plans.edit_trainingplan`, `plans.delete_trainingplan`, `plans.assign_trainingplan`, `plans.duplicate_trainingplan`
- **Gestión de Planes de Nutrición (Solo Lectura):**
  - `plans.view_nutritionplan`
- **Gestión de Análisis:**
  - `analyses.view_analysis`, `analyses.create_analysis`
- **Gestión de Blog (para su propio contenido):**
  - `blog.create_blogpost`, `blog.edit_blogpost`, `blog.delete_blogpost`, `blog.publish_blogpost`

### 3. Rol: `Nutricionista`
**Propósito**: Rol profesional enfocado en la gestión nutricional de los clientes. Tiene acceso de lectura a planes de entrenamiento.

**Permisos Incluidos**:
- **Gestión de Clientes:**
  - `clients.view_client`, `clients.edit_client`, `clients.view_client_progress`
- **Gestión de Planes de Nutrición (CRUD Completo):**
  - `plans.view_nutritionplan`, `plans.create_nutritionplan`, `plans.edit_nutritionplan`, `plans.delete_nutritionplan`, `plans.assign_nutritionplan`, `plans.duplicate_nutritionplan`
- **Gestión de Planes de Entrenamiento (Solo Lectura):**
  - `plans.view_trainingplan`
- **Gestión de Análisis:**
  - `analyses.view_analysis`, `analyses.create_analysis`
- **Gestión de Blog (para su propio contenido):**
  - `blog.create_blogpost`, `blog.edit_blogpost`, `blog.delete_blogpost`, `blog.publish_blogpost`

### 4. Rol: `Profesional Completo` (Ejemplo de Rol Personalizado)
**Propósito**: Un rol para profesionales multidisciplinarios como tú. Combina los permisos de Entrenador y Nutricionista. Las organizaciones podrán crear roles como este.

**Permisos Incluidos**:
- Todos los permisos de `Entrenador`.
- Todos los permisos de `Nutricionista`.
- (No incluye permisos de `organization.*`).

---

## 💡 Aclaración sobre Facturación

- **Facturación de la Plataforma**: Los permisos `organization.view_billing` y `organization.manage_billing` están **reservados para el rol `Admin`**. Esto es intencional.
- **Caso de Uso del Profesional Autónomo**: Un entrenador, fisio o nutricionista autónomo que necesite gestionar su propia facturación y suscripción a la plataforma, simplemente será el `owner` y `Admin` de su **propia `Organization`**.
- **Colaboración**: Si ese mismo profesional colabora con un gimnasio, será un `Member` en la `Organization` del gimnasio con el rol `Entrenador` (o el que corresponda), y correctamente **no tendrá acceso a la facturación del gimnasio**.

Esta arquitectura de "espacios de trabajo" (organizaciones) independientes es la que utilizan las grandes plataformas SaaS y nos da la máxima flexibilidad y seguridad.