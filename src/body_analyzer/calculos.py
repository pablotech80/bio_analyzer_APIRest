import math

from .constantes import CARB_DIVISOR, FAT_DIVISOR, PROTEIN_DIVISOR
from .model import ObjetivoNutricional, Sexo


# Funciones Lógicas
def calcular_porcentaje_grasa(
    cintura: float,
    cuello: float,
    altura: float,
    genero: Sexo,
    cadera: float = None,  # Opcional solo para hombres, obligatorio para mujeres
) -> float:
    """
    Calcula el porcentaje de grasa corporal utilizando la fórmula de la Marina de los EE.UU.

    Args:
        cintura (float): Circunferencia de la cintura en cm.
        cuello (float): Circunferencia del cuello en cm.
        altura (float): Altura en cm.
        genero (Sexo): Género de la persona, Sexo.HOMBRE o Sexo.MUJER.
        cadera (float, opcional): Circunferencia de la cadera en cm, solo para mujeres.

    Returns:
        float: Porcentaje de grasa corporal redondeado a dos decimales.

    Raises:
        ValueError: Si los valores de las medidas no son válidos o si faltan datos para mujeres.
    """

    # Validación del género

    if not isinstance(genero, Sexo):
        raise ValueError("El valor de 'genero' debe ser Sexo.HOMBRE o Sexo.MUJER.")

    # Cálculo para hombres
    if genero == Sexo.HOMBRE:
        if cintura <= cuello:
            raise ValueError("La cintura debe ser mayor que el cuello para hombres.")
        porcentaje_grasa = (
            495
            / (
                1.0324
                - 0.19077 * math.log10(cintura - cuello)
                + 0.15456 * math.log10(altura)
            )
            - 450
        )

    # Cálculo para mujeres
    elif genero == Sexo.MUJER:
        if cadera is None:
            raise ValueError("Para mujeres, la cadera debe ser especificada.")
        if cintura + cadera <= cuello:
            raise ValueError(
                "La suma de cintura y cadera debe ser mayor que el cuello para mujeres."
            )
        porcentaje_grasa = (
            495
            / (
                1.29579
                - 0.35004 * math.log10(cintura + cadera - cuello)
                + 0.22100 * math.log10(altura)
            )
            - 450
        )

    return round(porcentaje_grasa, 2)


def calcular_tmb(peso: float, altura: float, edad: int, genero: Sexo) -> float:
    """Calcula la tasa Metabólica Basal(TMB) usando la fórmula de Harris-Benedict.

    Args:
        peso: Peso en kg.(float)
        altura: Altura en cm.(float, int)
        edad: Edad del usuario en años (int)
        genero: (Literal) 'h' para hombre y 'm' para mujer.

    Returns: float: TMB calculada.
    """
    # Validaciones de entrada
    if not isinstance(genero, Sexo):
        raise ValueError(
            "El valor de 'genero' debe ser 'h' para 'hombre' o 'm' para 'mujer'."
        )

    if peso <= 0 or altura <= 0 or edad <= 0:
        raise ValueError("Peso, altura y edad deben ser valores positivos.")

    if genero == Sexo.HOMBRE:
        tmb = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * edad)
    elif genero == Sexo.MUJER:
        tmb = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * edad)
    else:
        raise ValueError("El valor de 'genero' debe ser 'h' o 'm'.")
    return round(tmb, 2)


def calcular_imc(peso: float, altura: float) -> float:
    """Calcula el Índice de Masa Corporal (IMC).
    Args:
        peso: Peso en kg.(float) Peso del usuario en kg.
        altura: Altura en cm.(float, int) Altura del usuario se convierte internamente de metros a cm.
    Returns: float: IMC calculada, y devuelto en dos decimales.
    """
    # Validaciones de entrada
    if peso <= 0 or altura <= 0:
        raise ValueError("Peso y altura deben ser valores positivos.")

    altura_m = altura / 100  # Esta variable convierte la altura de metros a cm.
    imc = peso / (altura_m**2)
    return round(imc, 2)


def calcular_agua_total(peso: float, altura: float, edad: int, genero: Sexo) -> float:
    """
    Calcula el agua total del cuerpo usando una fórmula simplificada basada en el peso, altura y edad del usuario.

    Args:
        peso (float): Peso del usuario en kilogramos.
        altura (float): Altura del usuario en centímetros.
        edad (int): Edad del usuario en años.
        genero (Literal['h', 'm']): Género del usuario, 'h' para hombre y 'm' para mujer, se utiliza Enum para evitar errores.

    Returns:
        float: Agua total estimada en el cuerpo, en litros.
    """
    # Validaciones de entrada
    if not isinstance(genero, Sexo):
        raise ValueError(
            "El valor de 'genero' debe ser 'h' para 'hombre' o 'm' para 'mujer'."
        )

    if peso <= 0 or altura <= 0 or edad <= 0:
        raise ValueError("Peso, altura y edad deben ser valores positivos.")

    if genero == Sexo.HOMBRE:
        agua_total = 2.447 - (0.09156 * edad) + (0.1074 * altura) + (0.3362 * peso)
    elif genero == Sexo.MUJER:
        agua_total = -2.097 + (0.1069 * altura) + (0.2466 * peso)
    else:
        raise ValueError("El valor de 'genero' debe ser 'h' o 'm'.")
    return round(agua_total, 2)


def calcular_peso_saludable(altura: float) -> tuple:
    """
    Calcula el rango de peso saludable basado en la altura utilizando el rango de IMC saludable.

    Args:
        altura (float): Altura del usuario en centímetros.

    Returns:
        tuple: Peso mínimo y peso máximo dentro del rango de IMC saludable, en kilogramos.
    """
    # Convertir la altura de centímetros a metros
    altura_m = altura / 100

    # Calcular el peso mínimo con IMC 18.5
    peso_min = 18.5 * (altura_m**2)

    # Calcular el peso máximo con IMC 24.9
    peso_max = 24.9 * (altura_m**2)

    return round(peso_min, 2), round(peso_max, 2)


def calcular_sobrepeso(peso: float, altura: float) -> float:  #
    """
    Calcula el sobrepeso comparando el peso actual con el peso máximo saludable.

    Args:
        peso (float): Peso actual del usuario en kilogramos.
        altura (float): Altura del usuario en centímetros.

    Returns:
        float: Sobrepeso calculado en kilogramos. Si no hay sobrepeso, se devuelve 0.
    """

    # Obtener solo el peso máximo saludable de la función calcular_peso_saludable
    _, peso_max = calcular_peso_saludable(altura)

    # Calcular el sobrepeso, si lo hay
    sobrepeso = max(0, peso - peso_max)

    return round(sobrepeso, 2)


def calcular_masa_muscular(
    peso: float,
    porcentaje_grasa: float,
) -> float:
    """
    Calcula la masa muscular (masa magra) del cuerpo descontando el porcentaje de grasa corporal.

    Args:
        peso (float): Peso total del usuario en kilogramos.
        porcentaje_grasa (float): Porcentaje de grasa corporal del usuario (entre 0 y 100).

    Returns:
        float: Masa muscular calculada en kilogramos, redondeada a dos decimales.
    """

    if peso <= 0 or porcentaje_grasa <= 0:
        raise ValueError(
            "Peso y porcentaje de grasa corporal deben ser valores positivos."
        )
    if not (0 <= porcentaje_grasa <= 100):
        raise ValueError("Porcentaje de grasa corporal debe estar entre 0 y 100.")

    masa_muscular = peso * ((100 - porcentaje_grasa) / 100)
    return round(masa_muscular, 2)


def calcular_ffmi(
    masa_muscular: float,
    altura: float,
) -> float:
    """
    Calcula el Índice de Masa Libre de Grasa (FFMI).

    El FFMI es una medida de la masa libre de grasa del cuerpo
    que ajusta el IMC para reflejar mejor la musculatura
    de una persona.

    Args:
        masa_muscular (float): Masa muscular del usuario en kilogramos.
        altura (float): Altura del usuario en centímetros (se convierte internamente a metros).

    Returns:
        float: El FFMI calculado basado en la masa muscular y la altura, redondeado a dos decimales.
    """

    if masa_muscular <= 0 or altura <= 0:
        raise ValueError("La masa muscular y la altura deben ser valores positivos.")
    altura_m = altura / 100
    ffmi = masa_muscular / (altura_m**2)
    return round(ffmi, 2)


def calcular_rcc(
    cintura: float,  # TODO: No es necesario que sea un int
    cadera: float,
) -> float:
    """
    Calcula la relación cintura-cadera, un indicador de la,
    distribución de grasa corporal en la zona abdominal.

    Args:
        cintura (float): Medida de la cintura en centímetros.
        cadera (float): Medida de la cadera en centímetros.

    Returns:
        float: Relación cintura-cadera calculada, redondeada a dos decimales.

    Raises:
        ValueError: Si alguno de los valores es negativo o igual a cero.
    """

    if cintura <= 0 or cadera is None or cadera <= 0:
        raise ValueError("La cintura y la cadera deben ser valores positivos.")

    rcc = cintura / cadera
    return round(rcc, 2)


def calcular_ratio_cintura_altura(cintura: float, altura: float) -> float:
    """
    Calcula el ratio cintura-altura, un indicador de riesgo de salud metabólica.

    El ratio cintura-altura es utilizado para evaluar la distribución de grasa corporal
    y el riesgo de problemas de salud
    relacionados con la obesidad.

    Args:
        cintura (float): Medida de la cintura en centímetros.
        altura (float): Altura del usuario en centímetros.

    Returns:
        float: Ratio cintura-altura calculado, redondeado a dos decimales.

    Raises:
        ValueError: Si alguno de los valores es negativo o igual a cero.
    """

    if cintura <= 0 or altura <= 0:
        raise ValueError("La cintura y la altura deben ser valores positivos.")

    return round(cintura / altura, 2)


def calcular_calorias_diarias(
    tmb: float,
    objetivo: ObjetivoNutricional,
) -> float:
    """
    Calcula las calorías diarias necesarias basadas en la TMB y el objetivo nutricional.

    Args:
        tmb (float): Tasa Metabólica Basal calculada.
        objetivo (ObjetivoNutricional): Objetivo nutricional
        ('mantener peso', 'perder grasa' o 'ganar masa muscular').

    Returns:
        float: Calorías diarias ajustadas según el objetivo, redondeadas a dos decimales.

    Raises:
        ValueError: Si el objetivo no es uno de los valores esperados.
    """
    if not isinstance(objetivo, ObjetivoNutricional):
        raise ValueError(
            "El objetivo debe ser una instancia de ObjetivoNutricional: 'mantener peso', 'perder grasa' o 'ganar masa muscular'."
        )

    if objetivo == ObjetivoNutricional.MANTENER_PESO:
        calorias = tmb * 1.2
    elif objetivo == ObjetivoNutricional.PERDER_GRASA:
        calorias = tmb * 1.2 * 0.8  # 20% de reducción calórica
    elif objetivo == ObjetivoNutricional.GANAR_MASA_MUSCULAR:
        calorias = tmb * 1.2 * 1.2  # 20% de aumento calórico

    return round(calorias, 2)


def calcular_macronutrientes(calorias: float, objetivo: ObjetivoNutricional) -> tuple:
    """
    Calcula la distribución de macronutrientes basada en las calorías diarias y el objetivo nutricional.

    Args:
        calorias (float): Calorías diarias recomendadas.
        objetivo (ObjetivoNutricional): Objetivo nutricional ('mantener peso', 'perder grasa', 'ganar masa muscular').

    Returns:
        tuple: Una tupla con la cantidad de macronutrientes recomendados
        (gramos de proteínas, gramos de carbohidratos, gramos de grasas), redondeados a dos decimales.
    """
    if not isinstance(objetivo, ObjetivoNutricional):
        raise ValueError(
            "El valor de 'objetivo' debe ser una instancia de ObjetivoNutricional: 'mantener peso', 'perder grasa' o 'ganar masa muscular'."
        )

    # Asignación de macronutrientes según el objetivo
    if objetivo == ObjetivoNutricional.MANTENER_PESO:
        proteinas = (calorias * 0.30) / PROTEIN_DIVISOR
        carbohidratos = (calorias * 0.40) / CARB_DIVISOR
        grasas = (calorias * 0.30) / FAT_DIVISOR
    elif objetivo == ObjetivoNutricional.PERDER_GRASA:
        proteinas = (calorias * 0.40) / PROTEIN_DIVISOR
        carbohidratos = (calorias * 0.40) / CARB_DIVISOR
        grasas = (calorias * 0.20) / FAT_DIVISOR
    elif objetivo == ObjetivoNutricional.GANAR_MASA_MUSCULAR:
        proteinas = (calorias * 0.30) / PROTEIN_DIVISOR
        carbohidratos = (calorias * 0.50) / CARB_DIVISOR
        grasas = (calorias * 0.20) / FAT_DIVISOR

    # Redondeo de cada macronutriente a dos decimales antes de devolverlos
    return round(proteinas, 2), round(carbohidratos, 2), round(grasas, 2)


def calcular_peso_grasa_corporal(peso: float, porcentaje_grasa: float) -> float:
    """
    Calcula el peso de la grasa corporal en kilogramos.

    Args:
        peso (float): Peso total de la persona en kilogramos.
        porcentaje_grasa (float): Porcentaje de grasa corporal (entre 0 y 100).

    Returns:
        float: Peso de la grasa corporal en kilogramos.

    Raises:
        ValueError: Si los valores de peso o porcentaje de grasa no son correctos.
    """

    # Validaciones de entrada
    if peso <= 0:
        raise ValueError("El peso debe ser un número positivo.")
    if not (0 <= porcentaje_grasa <= 100):
        raise ValueError("El porcentaje de grasa corporal debe estar entre 0 y 100.")

    # Cálculo del peso de la grasa corporal
    peso_grasa_corporal = peso * (porcentaje_grasa / 100)

    return round(peso_grasa_corporal, 2)


def calcular_macronutrientes_porcentajes(
        calorias: float, porcentaje_proteinas: float, porcentaje_carbohidratos: float, porcentaje_grasas: float
        ):
    """
    Calcula los gramos diarios de proteínas, carbohidratos y grasas a partir del reparto porcentual de calorías.

    Args:
        calorias (float):
        Calorías totales diarias.
        porcentaje_proteinas (float): % de proteínas.
        porcentaje_carbohidratos (float): % de carbohidratos.
        porcentaje_grasas (float): % de grasas.

    Returns:
        tuple: (proteinas_gramos, carbohidratos_gramos, grasas_gramos)
    """
    if calorias <= 0:
        raise ValueError("Las calorías deben ser un número positivo.")

    if (porcentaje_proteinas + porcentaje_carbohidratos + porcentaje_grasas) != 100:
        raise ValueError("La suma de los porcentajes debe ser igual a 100%.")

    proteinas = (calorias * (porcentaje_proteinas / 100)) / 4
    carbohidratos = (calorias * (porcentaje_carbohidratos / 100)) / 4
    grasas = (calorias * (porcentaje_grasas / 100)) / 9

    return proteinas, carbohidratos, grasas

def calcular_edad_metabolica_avanzada(tmb, genero, edad_cronologica, imc, porcentaje_grasa, ratio_cintura_altura):
    """
        Calcula la edad metabólica ajustada clínicamente con un límite de penalización para evitar interpretaciones médicas incorrectas.
        """
    # Tabla de TMB promedio
    tmb_por_edad_hombre = {
        18: 1660, 25: 1600, 30: 1550, 35: 1500, 40: 1450, 45: 1400, 50: 1350, 55: 1300, 60: 1250
        }
    tmb_por_edad_mujer = {
        18: 1450, 25: 1400, 30: 1350, 35: 1300, 40: 1250, 45: 1200, 50: 1150, 55: 1100, 60: 1050
        }

    tabla = tmb_por_edad_hombre if genero == "hombre" else tmb_por_edad_mujer
    edad_metabolica_base = min(tabla.keys(), key = lambda edad: abs(tmb - tabla[edad]))

    penalizacion = 0

    if 25 <= imc < 30:
        penalizacion += 3
    elif 30 <= imc < 35:
        penalizacion += 7
    elif 35 <= imc < 40:
        penalizacion += 10
    elif imc >= 40:
        penalizacion += 15

    if (genero == "hombre" and porcentaje_grasa >= 25) or (genero == "mujer" and porcentaje_grasa >= 32):
        penalizacion += 5

    if ratio_cintura_altura > 0.5:
        penalizacion += 3

    # Limitar penalización máxima a +20 años
    penalizacion = min(penalizacion, 20)

    edad_metabolica_ajustada = edad_metabolica_base + penalizacion

    return edad_metabolica_ajustada
