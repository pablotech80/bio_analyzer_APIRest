from src.body_analyzer.model import Sexo, ObjetivoNutricional

def convertir_genero(genero_str):
    if genero_str == "h":
        return Sexo.HOMBRE
    elif genero_str == "m":
        return Sexo.MUJER
    else:
        raise ValueError("Género no válido. Usa 'h' para hombre o 'm' para mujer.")

def convertir_objetivo(objetivo_str):
    try:
        return ObjetivoNutricional(objetivo_str.strip().lower())
    except ValueError:
        raise ValueError("El objetivo debe ser 'mantener peso', 'perder grasa' o 'ganar masa muscular'.")
