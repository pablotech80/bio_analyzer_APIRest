from .constantes_enum import Enum

# ---------------------------
# ENUMS
# ---------------------------


class Sexo(str, Enum):
    HOMBRE = "h"
    MUJER = "m"


class Objetivo(str, Enum):
    DEFINICION = "definicion"
    MANTENIMIENTO = "mantenimiento"
    VOLUMEN = "volumen"


# ---------------------------
# MACROS
# ---------------------------


class Macronutrientes:
    PROTEIN_DIVISOR = 4
    CARB_DIVISOR = 4
    FAT_DIVISOR = 9


# Exportar divisores como variables de módulo para import directo
PROTEIN_DIVISOR = Macronutrientes.PROTEIN_DIVISOR
CARB_DIVISOR = Macronutrientes.CARB_DIVISOR
FAT_DIVISOR = Macronutrientes.FAT_DIVISOR

# ---------------------------
# PORCENTAJE DE GRASA (%)
# ---------------------------


class GrasaCorporal:
    ALTA_HOMBRES = 25
    BAJA_HOMBRES = 6
    ALTA_MUJERES = 32
    BAJA_MUJERES = 16


# ---------------------------
# RELACIÓN CINTURA-CADERA (RCC)
# ---------------------------


class RCC:
    ALTO_HOMBRES = 0.95
    MODERADO_HOMBRES = 0.90
    ALTO_MUJERES = 0.85
    MODERADO_MUJERES = 0.80


# ---------------------------
# RATIO CINTURA-ALTURA
# ---------------------------


class RatioCinturaAltura:
    ALTO_RIESGO = 0.6
    MODERADO_RIESGO = 0.5


# ---------------------------
# FFMI (Fat-Free Mass Index)
# ---------------------------


class FFMI:
    UMBRAL_HOMBRES = [18, 19, 20, 21, 22.5, 24, 25.5, 27, 29]
    UMBRAL_MUJERES = [13.5, 14.5, 16, 17, 18.5, 20, 21, 22, 23]
