from .calculos import *
from .interpretaciones import *
from .model import Sexo, ObjetivoNutricional


def validar_parametro(nombre, valor, tipos, positivo=True):
    """
    Valida que el parámetro `valor` sea de uno de los `tipos` indicados y, si se requiere,
    que sea positivo.
    """
    if not isinstance(valor, tipos) or (positivo and valor <= 0):
        tipo_str = ", ".join([t.__name__ for t in tipos])
        raise ValueError(f"'{nombre}' debe ser un {tipo_str} positivo.")


def calcular_resultados(
    peso, altura, edad, genero_enum, cintura, cuello, cadera, objetivo
):
    """
    Realiza cálculos principales como TMB, IMC, porcentaje de grasa, etc., y devuelve un diccionario
    con los resultados.
    """
    tmb = calcular_tmb(peso, altura, edad, genero_enum)
    porcentaje_grasa = calcular_porcentaje_grasa(
        cintura, cuello, altura, genero_enum, cadera
    )

    # Calorías diarias según el objetivo
    calorias_diarias = calcular_calorias_diarias(tmb, objetivo)

    # Cálculo de macronutrientes
    proteinas, carbohidratos, grasas = calcular_macronutrientes(
        calorias_diarias, objetivo
    )

    return {
        "tmb": tmb,
        "imc": calcular_imc(peso, altura),
        "porcentaje_grasa": porcentaje_grasa,
        "peso_grasa_corporal": calcular_peso_grasa_corporal(peso, porcentaje_grasa),
        "masa_muscular": peso - calcular_peso_grasa_corporal(peso, porcentaje_grasa),
        "ffmi": calcular_masa_muscular(peso, porcentaje_grasa),
        "calorias_diarias": calorias_diarias,
        "macronutrientes": {
            "proteinas": proteinas,
            "carbohidratos": carbohidratos,
            "grasas": grasas,
        },
        "rcc": calcular_rcc(cintura, cadera) if genero_enum == Sexo.MUJER else "N/A",
        "ratio_cintura_altura": cintura / altura,
    }


def calcular_interpretaciones(resultados, genero_enum):
    """
    Realiza las interpretaciones de los resultados y devuelve un diccionario con las interpretaciones.
    """
    return {
        "ffmi": interpretar_ffmi(resultados["ffmi"], genero_enum),
        "imc": interpretar_imc(resultados["imc"], resultados["ffmi"], genero_enum),
        "porcentaje_grasa": interpretar_porcentaje_grasa(
            resultados["porcentaje_grasa"], genero_enum
        ),
        "rcc": (
            interpretar_rcc(resultados["rcc"], genero_enum)
            if genero_enum == Sexo.MUJER
            else "N/A"
        ),
        "ratio_cintura_altura": interpretar_ratio_cintura_altura(
            resultados["ratio_cintura_altura"]
        ),
    }


def informe_completo(data):
    try:
        # Extracción y validación de datos simplificando con un bucle
        campos_obligatorios = [
            "peso",
            "altura",
            "edad",
            "genero",
            "cuello",
            "cintura",
            "objetivo",
        ]
        for campo in campos_obligatorios:
            if data.get(campo) is None:
                raise ValueError(f"Falta el parámetro obligatorio: {campo}")

        peso, altura, edad, genero, cuello, cintura, objetivo = [
            data.get(c) for c in campos_obligatorios
        ]
        cadera = data.get("cadera") if genero == "m" else None

        # Validación de valores y tipos
        validar_parametro("peso", peso, (int, float))
        validar_parametro("altura", altura, (int, float))
        validar_parametro("edad", edad, (int,))
        validar_parametro("cuello", cuello, (int, float))
        validar_parametro("cintura", cintura, (int, float))
        if genero == "m":
            validar_parametro("cadera", cadera, (int, float))
        genero_enum = Sexo.HOMBRE if genero == "h" else Sexo.MUJER

        # Convertir objetivo a enum ObjetivoNutricional
        try:
            objetivo_enum = ObjetivoNutricional(objetivo)
        except ValueError:
            raise ValueError(
                "El objetivo debe ser 'mantener peso', 'perder grasa' o 'ganar masa muscular'."
            )

        # Realización de cálculos e interpretaciones
        resultados = calcular_resultados(
            peso, altura, edad, genero_enum, cintura, cuello, cadera, objetivo_enum
        )
        interpretaciones = calcular_interpretaciones(resultados, genero_enum)

        return {"resultados": resultados, "interpretaciones": interpretaciones}

    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Error interno del servidor: {str(e)}"}
