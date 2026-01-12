# 🚀 FASE 1: Construcción del Núcleo del Backend en Django

**Proyecto**: CoachBodyFit360 - Evolución a Plataforma SaaS Multi-Tenant  
**Owner**: Pablo Techera

---

## 🎯 Objetivo de la Fase 1

Tener un **backend Django funcional** con la nueva estructura de datos, un panel de administración operativo y los cimientos para la futura API. Esta fase se enfoca en construir el "motor" de la nueva plataforma.

**Resultado Esperado**: Un proyecto Django con modelos implementados, migraciones ejecutadas y un panel de admin funcional para gestionar `Organizations`, `Users`, `Roles` y `Permissions`.

---

## 📚 Capas de Trabajo y Tareas

### 1. Capa de Proyecto y Configuración (Semana 1)

**Objetivo**: Crear la estructura del proyecto y configurar el entorno de desarrollo.

- [ ] **Crear la estructura de directorios del proyecto Django.**
  - Seguir las mejores prácticas, separando la configuración (`core`) de las aplicaciones (`apps`).

- [ ] **Configurar el entorno de desarrollo.**
  - `pyproject.toml` o `requirements.txt` con dependencias de Django.
  - Configuración de variables de entorno para `development` y `production` (`python-decouple` o `django-environ`).

- [ ] **Crear el modelo de Usuario Personalizado.**
  - Crear una app `users` y definir el `User` personalizado que herede de `AbstractUser`.
  - Configurar `AUTH_USER_MODEL` en `settings.py`.

### 2. Capa de Modelos y Datos (Semana 1-2)

**Objetivo**: Implementar el esquema de base de datos que diseñamos en la Fase 0.

- [ ] **Implementar los modelos de la Fase 0 en código Django.**
  - Crear apps `organizations`, `permissions`, `plans`, etc.
  - Escribir el código de los modelos `Organization`, `Membership`, `Role`, `Permission`, `NutritionPlan`, `TrainingPlan`, etc.

- [ ] **Generar y ejecutar las migraciones iniciales.**
  - `python manage.py makemigrations`
  - `python manage.py migrate`
  - Verificar que el esquema de la base de datos se crea correctamente en PostgreSQL.

- [ ] **Crear un script de "seeding" (datos iniciales).**
  - Crear los `Permissions` base definidos en `permissions_definition.md`.
  - Crear un usuario `SuperAdmin`.

### 3. Capa de Administración (Semana 2-3)

**Objetivo**: Tener un panel de control funcional para gestionar la plataforma desde el día 1.

- [ ] **Registrar los modelos en el Django Admin.**
  - Crear `admin.py` en cada app.
  - Registrar `User`, `Organization`, `Membership`, `Role`, `Permission`, etc.

- [ ] **Personalizar el Django Admin para una mejor usabilidad.**
  - Usar `list_display`, `search_fields`, `list_filter` e `inlines`.
  - Ejemplo: En la vista de `Organization`, mostrar sus `Memberships` como un inline.
  - Ejemplo: En la vista de `User`, poder asignar `Roles` a su `Membership` directamente.

---

## ✅ Checklist de Validación de la Fase 1

Al final de esta fase, debemos poder responder "SÍ" a todo lo siguiente:

- [ ] ¿El proyecto Django está estructurado y configurado correctamente?
- [ ] ¿El modelo de usuario personalizado está funcionando?
- [ ] ¿Todos los modelos de la Fase 0 están implementados en código?
- [ ] ¿Las migraciones se han ejecutado sin errores en PostgreSQL?
- [ ] ¿Puedo crear, ver, editar y eliminar `Organizations`, `Users` y `Roles` desde el panel de admin de Django?
- [ ] ¿Puedo asignar `Permissions` a un `Role` y `Roles` a un `User` a través de su `Membership` en el admin?