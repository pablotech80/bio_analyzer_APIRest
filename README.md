# **Bio•Analyze API** 

<img src="app/static/img/default_profile.png" alt="Logo" width="300" title="Bioanalyze"/>

[![Versión](https://img.shields.io/badge/version-1.0.0--beta-blue)]()
[![Estado](https://img.shields.io/badge/build-passing-brightgreen)]()
[![Licencia](https://img.shields.io/badge/license-MIT-yellow)]()  
[![Desplegado en Railway](https://img.shields.io/badge/Railway-Live-orange)](https://bioanalyze.up.railway.app/informe_web)

> **API para análisis de composición corporal y recomendaciones nutricionales. Ideal para entrenadores personales, 
> nutricionistas y profesionales de la salud.**

---

## Índice

1. [Descripción](#descripción)
2. [Funciones principales](#funciones-principales)
3. [Requisitos](#requisitos)
4. [Instalación y uso](#instalación-y-uso)
5. [Pruebas locales](#pruebas-locales)
6. [Endpoints disponibles](#endpoints-disponibles)
7. [Diagrama de flujo](#diagrama-de-flujo)
8. [Producción](#producción)
9. [Notas finales](#notas-finales)
10. [Contribuciones](#contribuciones)
11. [Licencia](#licencia)

---

## Descripción

**Bio•Analyze** es una API que permite realizar cálculos biométricos avanzados y obtener recomendaciones iniciales de nutrición. Diseñada como herramienta backend para integrarse con formularios web o aplicaciones.

Pensado para:
- Entrenadores personales
- Nutricionistas y dietistas
- Profesionales del bienestar y salud

Puedes probar la versión beta en producción: 🌐 [Bio Analyze API en Railway](https://bioanalyze.up.railway.app/informe_web)

---

## Funciones principales

1. **Cálculos precisos y automáticos**:
   - IMC (con interpretación contextualizada)
   - Porcentaje de grasa corporal
   - TMB (Tasa Metabólica Basal) y calorías recomendadas
   - Agua total, masa muscular estimada, sobrepeso

2. **Objetivos personalizables**:
   - Perder grasa
   - Mantener peso
   - Ganar masa muscular

3. **Macronutrientes sugeridos** (proteínas, grasas, carbohidratos)

4. **Interpretaciones inteligentes**:
   - Basadas en fórmulas científicas
   - Incluyen riesgos cardiovasculares (ratio cintura-altura, RCC)
   - Diagnóstico visual inmediato

5. **Frontend moderno y responsive**:
   - Formularios claros
   - Visualización detallada en tarjetas
   - Compatible con móvil y escritorio

---

## Requisitos

- Python 3.11+
- Librerías listadas en `pyproject.toml`

---

## Instalación y uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu_usuario/bioanalyze.git
cd bioanalyze
```
### 2. Instalar Dependencias
```bash
pip install .
# o usando Makefile:
make install
```
### 3. Ejecuta la API localmente
```bash
python run.py
```
Disponible en: http://127.0.0.1:5000

## Pruebas locales

Puedes probar la API con Postman, cURL u otra herramienta HTTP.

Ejemplo con cURL:
```bash
curl -X POST http://127.0.0.1:5000/informe_completo \
-H "Content-Type: application/json" \
-d '{
  "peso": 90,
  "altura": 165,
  "edad": 44,
  "genero": "h",
  "cuello": 41,
  "cintura": 99,
  "cadera": 105,
  "objetivo": "perder grasa"
}'
```

Respuesta esperada:
```bash
{
  "interpretaciones": {
    "ffmi": "Muy cerca del máximo potencial.",
    "imc": "El IMC es alto, pero puede estar influenciado por una alta masa muscular.",
    "porcentaje_grasa": "Alto",
    "ratio_cintura_altura": "Alto riesgo",
    "rcc": "N/A"
  },
  "resultados": {
    "agua_total": 46.4,
    "calorias_diarias": 1762.69,
    "ffmi": 24.28,
    "imc": 33.06,
    "macronutrientes": {
      "carbohidratos": 176.27,
      "grasas": 39.17,
      "proteinas": 176.27
    },
    "masa_muscular": 66.105,
    "peso_saludable": {
      "max": 67.79,
      "min": 50.37
    },
    "porcentaje_grasa": 26.55,
    "ratio_cintura_altura": 0.6,
    "rcc": "N/A",
    "sobrepeso": 22.21,
    "tmb": 1836.14
  }
}
```
---

## Endpoints disponibles

| Método | Ruta                                   | Descripción                          |
|:-------|:---------------------------------------|:-------------------------------------|
| GET    | `/`                                    | Verifica que el servidor esté activo |
| POST   | `/informe_completo`                    | Genera informe completo              |
| POST   | `/calcular_imc`                        | Calcula el IMC                       |
| POST   | `/calcular_porcentaje_grasa`           | Grasa corporal (kg)                  |
| POST   | `/calcular_calorias_diarias`           | Calorías diarias recomendadas        |
| POST   | `/calcular_macronutrientes_porcentaje` | Reparto de macronutrientes           |
| ...    | *Ver archivo `calculos.py`*            | Más funciones disponibles            |

---

## Diagrama de flujo

Este diagrama representa cómo se procesa la información dentro de la API Bio•Analyze desde la entrada del usuario hasta la entrega del informe:

1. **Inicio**  
   El usuario completa un formulario con sus datos físicos y biométricos (edad, peso, altura, género, etc.).

2. **Validación de datos**  
   Se comprueba que todos los campos requeridos sean válidos. Si hay errores, se muestra un mensaje al usuario.

3. **Procesamiento de datos en backend**  
   Se realizan cálculos biométricos como IMC, TMB, FFMI, porcentaje de grasa corporal, masa muscular, agua corporal y otros indicadores.

4. **Generación de interpretaciones**  
   Se aplican reglas personalizadas para interpretar los resultados y brindar contexto útil (por ejemplo, si un IMC alto se debe a masa muscular).

5. **Cálculo de macronutrientes**  
   Basado en el objetivo del usuario (perder grasa, mantener, ganar masa muscular), se ajustan los gramos de proteínas, grasas y carbohidratos diarios.

6. **Informe final**  
   Todos los resultados se presentan al usuario en formato visual con tarjetas informativas. 
7. Próximamente podrá exportarse en PDF.


[![](https://mermaid.ink/img/pako:eNptkUtOwzAQhq9ied1eIAskRCsEElBRYIG8GewhsYg90dhGgqYHYsGKI-RiOE7UglSv5h9_895JTQZlJWuGrhEPK-VFfo8hAVsSy-VZv_bvwzcIA5GCuN7e3fbifHM1cdkozBO01sxMLyal7fDjJ-yPo-AXxIw6Ui82TBoDOIs-0gT_cxX8Ej0yCMaQ2ggmt_FiyQ1fka0e690fPqYMRz0PEBnrMV6TQz82Qh6D6JAD-dzaJxjIaeahT7e8ZiYupbqEIULRysuFdMgOrMk73I2hSsYGHSpZZdMAvymp_D5zkCJtP7yWVeSEC8mU6kZWr9CGrFKXl4crC_kQ7uDtwD8THTUaG4lvppOVy-1_AZSnoCA?type=png)](https://mermaid.live/edit#pako:eNptkUtOwzAQhq9ied1eIAskRCsEElBRYIG8GewhsYg90dhGgqYHYsGKI-RiOE7UglSv5h9_895JTQZlJWuGrhEPK-VFfo8hAVsSy-VZv_bvwzcIA5GCuN7e3fbifHM1cdkozBO01sxMLyal7fDjJ-yPo-AXxIw6Ui82TBoDOIs-0gT_cxX8Ej0yCMaQ2ggmt_FiyQ1fka0e690fPqYMRz0PEBnrMV6TQz82Qh6D6JAD-dzaJxjIaeahT7e8ZiYupbqEIULRysuFdMgOrMk73I2hSsYGHSpZZdMAvymp_D5zkCJtP7yWVeSEC8mU6kZWr9CGrFKXl4crC_kQ7uDtwD8THTUaG4lvppOVy-1_AZSnoCA)

---

##  Producción

La API está desplegada actualmente en Railway (versión beta):  
🌐 https://bioanalyze.up.railway.app/informe_web

Puedes utilizar los mismos endpoints mencionados anteriormente, 
solo debes reemplazar `http://127.0.0.1:5000` por la URL en producción.

---

## Notas finales

**Próximas versiones incluirán:**
- Implementación de autenticación.
- Integración con base de datos para guardar historiales.
- Integración con FitMasterAI (GPT personalizado)
- Exportación de informes en PDF.
- Frontend para facilitar el uso desde móvil y escritorio.

---

## Contribuciones

¡Este proyecto está abierto a contribuciones! Si deseas participar:

1. Haz un fork del repositorio.
2. Crea una nueva rama para tus cambios:
```bash
git checkout -b feature/nueva-funcionalidad
```

Realiza tus cambios y agrega un commit descriptivo:

```bash 
git commit -m "Agregado nuevo cálculo para ..."
```

Envía un pull request explicando lo que has modificado.
Asegúrate de seguir las buenas prácticas de programación y, 
si es posible, añade pruebas unitarias para cualquier nueva funcionalidad.

## Licencia

Copyright © 2024 Pablo Techera Sosa.

1. Permisos
Se otorgan los siguientes permisos bajo las siguientes condiciones:

Uso personal y educativo:
Puedes usar este proyecto libremente para fines de aprendizaje o educación.
Modificaciones y colaboraciones:
Puedes modificar el código y colaborar mediante pull requests.
Las contribuciones serán revisadas y aprobadas por los mantenedores del proyecto.

Redistribución:
Si redistribuyes una versión modificada, debes incluir esta misma licencia.
El uso comercial del proyecto está prohibido sin autorización explícita del autor.

2. Restricciones
Derechos de autor:
Este proyecto es propiedad intelectual de Pablo Techera Sosa.
Todas las contribuciones aceptadas se considerarán licenciadas para el uso dentro del proyecto original.

Uso comercial:
Prohibido el uso comercial sin permiso expreso y por escrito.

Limitación de responsabilidad:
Este software se proporciona "tal cual", sin garantías.
Los autores no serán responsables de daños derivados del uso del proyecto.

3. Cómo contribuir
Haz un fork del repositorio.
Crea una nueva rama para tus modificaciones.
Envía un pull request explicando claramente los cambios.

4. Nota final
Al contribuir en este proyecto, aceptas que tus aportaciones pueden ser utilizadas y distribuidas bajo esta licencia.