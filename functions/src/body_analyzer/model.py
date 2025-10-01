from enum import Enum


class Sexo(Enum):
    HOMBRE = "h"
    MUJER = "m"


class ObjetivoNutricional(Enum):
    MANTENER_PESO = "mantener peso"
    PERDER_GRASA = "perder grasa"
    GANAR_MASA_MUSCULAR = "ganar masa muscular"
