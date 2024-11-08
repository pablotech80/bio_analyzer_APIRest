from src.body_analyzer.constantes import *
from src.body_analyzer.model import Sexo


def interpretar_imc(imc: float, ffmi: float, genero: Sexo) -> str:
    """
    Interpreta el resultado del IMC considerando el FFMI.

    Args:
        imc (float): Índice de Masa Corporal calculado.
        ffmi (float): Índice de Masa Libre de Grasa.
        genero (Sexo): Género del usuario (Sexo.HOMBRE o Sexo.MUJER).

    Returns:
        str: Interpretación del IMC basada en los valores de FFMI y género.

    Raises:
        ValueError: Si el valor de 'genero' no es Sexo.HOMBRE o Sexo.MUJER.
    """
    if genero not in [Sexo.HOMBRE, Sexo.MUJER]:
        raise ValueError("Género no válido. Debe ser 'Sexo.HOMBRE' o 'Sexo.MUJER'.")

    if imc > 25 and ffmi > 16:
        return (
            "El IMC es alto, pero puede estar influenciado por una alta masa muscular."
        )
    elif imc < 18.5:
        return "El IMC es bajo, se recomienda consultar con un profesional de salud."
    else:
        return "El IMC está dentro del rango normal."


def interpretar_porcentaje_grasa(porcentaje_grasa: float, genero: Sexo) -> str:
    """
    Interpreta el porcentaje de grasa corporal basándose en el género y,
    proporciona una evaluación cualitativa.

    Args:
        porcentaje_grasa (float): El porcentaje de grasa corporal calculado.
        genero (Sexo): Género del individuo (Sexo.HOMBRE para hombres, Sexo.MUJER para mujeres).

    Returns:
        str: Una cadena de texto que describe el estado del porcentaje
        de grasa corporal en términos de salud.

    Raises:
        ValueError: Si el valor de 'genero' no es Sexo.HOMBRE o Sexo.MUJER.
    """
    if genero not in [Sexo.HOMBRE, Sexo.MUJER]:
        raise ValueError("Género no válido. Debe ser 'Sexo.HOMBRE' o 'Sexo.MUJER'.")

    if genero == Sexo.HOMBRE:
        if porcentaje_grasa > GRASA_ALTA_HOMBRES:
            return "Alto"
        elif porcentaje_grasa < GRASA_BAJA_HOMBRES:
            return "Bajo"
        else:
            return "Normal"
    else:  # Sexo.MUJER
        if porcentaje_grasa > GRASA_ALTA_MUJERES:
            return "Alto"
        elif porcentaje_grasa < GRASA_BAJA_MUJERES:
            return "Bajo"
        else:
            return "Normal"


def interpretar_ffmi(ffmi: float, genero: Sexo) -> str:
    """
    Proporciona una interpretación del FFMI basado en rangos preestablecidos que varían según el género.

    Args:
        ffmi (float): Valor del FFMI a interpretar.
        genero (Sexo): Género del usuario (Sexo.HOMBRE o Sexo.MUJER).

    Returns:
        str: Descripción del nivel de forma física basado en el FFMI.

    Raises:
        ValueError: Si el valor de 'genero' no es Sexo.HOMBRE o Sexo.MUJER.
    """
    if genero not in [Sexo.HOMBRE, Sexo.MUJER]:
        raise ValueError("Género no válido. Debe ser 'Sexo.HOMBRE' o 'Sexo.MUJER'.")

    umbrales = FFMI_UMBRAL_HOMBRES if genero == Sexo.HOMBRE else FFMI_UMBRAL_MUJERES

    if ffmi < umbrales[0]:
        return "Lejos del máximo potencial (pobre forma física)"
    elif umbrales[0] <= ffmi < umbrales[1]:
        return "Cercano a la normalidad"
    elif umbrales[1] <= ffmi < umbrales[2]:
        return "Normal"
    elif umbrales[2] <= ffmi < umbrales[3]:
        return "Superior a la normalidad (buena forma física)"
    elif umbrales[3] <= ffmi < umbrales[4]:
        return "Fuerte (Muy buena forma física)"
    elif umbrales[4] <= ffmi < umbrales[5]:
        return "Muy fuerte (Excelente forma física). Cerca del máximo potencial."
    elif umbrales[5] <= ffmi < umbrales[6]:
        return "Muy cerca del máximo potencial."
    elif umbrales[6] <= ffmi < umbrales[7]:
        return "Potencial máximo natural alcanzado. Muy muy pocos llegan naturales"
    else:
        return "Imposible sin fármacos"


def interpretar_rcc(rcc: float, genero: Sexo) -> str:
    """
    Interpreta la relación cintura-cadera basándose en umbrales específicos
    de riesgo según el género.

    Args:
        rcc (float): Relación cintura-cadera calculada.
        genero (Sexo): Género del usuario (Sexo.HOMBRE o Sexo.MUJER).

    Returns:
        str: Interpretación del nivel de riesgo asociado con la RCC.

    Raises:
        ValueError: Si el valor de 'genero' no es Sexo.HOMBRE o Sexo.MUJER.
    """
    if genero not in [Sexo.HOMBRE, Sexo.MUJER]:
        raise ValueError("Género no válido. Debe ser 'Sexo.HOMBRE' o 'Sexo.MUJER'.")

    if genero == Sexo.HOMBRE:
        if rcc > RCC_ALTO_HOMBRES:
            return "Alto riesgo"
        elif RCC_MODERADO_HOMBRES < rcc <= RCC_ALTO_HOMBRES:
            return "Moderado riesgo"
        else:
            return "Bajo riesgo"
    else:  # Sexo.MUJER
        if rcc > RCC_ALTO_MUJERES:
            return "Alto riesgo"
        elif RCC_MODERADO_MUJERES < rcc <= RCC_ALTO_MUJERES:
            return "Moderado riesgo"
        else:
            return "Bajo riesgo"


def interpretar_ratio_cintura_altura(ratio: float) -> str:
    """
    Interpreta el ratio cintura-altura para evaluar el riesgo metabólico y posibles riesgos cardiovasculares.

    Args:
        ratio (float): Ratio cintura-altura calculado.

    Returns:
        str: Interpretación del nivel de riesgo metabólico basado en el ratio.

    Raises:
        ValueError: Si el valor de 'ratio' no es positivo.
    """
    if ratio <= 0:
        raise ValueError("El valor del 'ratio' debe ser un número positivo.")

    if ratio >= RATIO_ALTO_RIESGO:
        return "Alto riesgo"
    elif RATIO_MODERADO_RIESGO <= ratio < RATIO_ALTO_RIESGO:
        return "Moderado riesgo"
    else:
        return "Bajo riesgo"
