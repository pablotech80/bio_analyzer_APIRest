from flask import Blueprint, request, jsonify
from src.body_analyzer.calculos import (
    calcular_porcentaje_grasa,
    calcular_tmb,
    calcular_imc,
    calcular_agua_total,
    calcular_ffmi,
    calcular_peso_saludable,
    calcular_sobrepeso,
    calcular_rcc,
    calcular_ratio_cintura_altura,
    calcular_calorias_diarias,
    calcular_macronutrientes
)
from src.body_analyzer.interpretaciones import (
    interpretar_imc,
    interpretar_porcentaje_grasa,
    interpretar_ffmi,
    interpretar_rcc,
    interpretar_ratio_cintura_altura
)
from src.body_analyzer.utils import convertir_genero, convertir_objetivo
from src.body_analyzer.model import Sexo

informe_bp = Blueprint("informe", __name__)

@informe_bp.route("/informe_completo", methods=["POST"])
def informe_completo_endpoint():
    try:
        data = request.get_json()

        peso = data.get("peso")
        altura = data.get("altura")
        edad = data.get("edad")
        genero = data.get("genero", "").strip().lower()
        cuello = data.get("cuello")
        cintura = data.get("cintura")
        cadera = data.get("cadera")
        objetivo = data.get("objetivo")

        if None in (peso, altura, edad, genero, cuello, cintura, objetivo):
            return jsonify({"error": "Faltan parámetros obligatorios"}), 400

        try:
            peso = float(peso)
            altura = float(altura)
            edad = int(edad)
            cuello = float(cuello)
            cintura = float(cintura)
            cadera = float(cadera) if cadera is not None else 0
        except ValueError:
            return jsonify({"error": "Parámetros numéricos inválidos"}), 400

        if peso <= 0 or altura <= 0 or edad <= 0:
            return jsonify({"error": "Peso, altura y edad deben ser mayores que cero"}), 400

        genero_enum = convertir_genero(genero)
        objetivo_enum = convertir_objetivo(objetivo)

        porcentaje_grasa = calcular_porcentaje_grasa(cintura, cuello, altura, genero_enum, cadera)
        tmb = calcular_tmb(peso, altura, edad, genero_enum)
        imc = calcular_imc(peso, altura)
        masa_muscular = peso - (peso * (porcentaje_grasa / 100))
        agua_total = calcular_agua_total(peso, altura, edad, genero_enum)
        ffmi = calcular_ffmi(masa_muscular, altura)
        peso_saludable_min, peso_saludable_max = calcular_peso_saludable(altura)
        sobrepeso = calcular_sobrepeso(peso, altura)
        rcc = calcular_rcc(cintura, cadera) if genero_enum == Sexo.MUJER else "N/A"
        ratio_cintura_altura = calcular_ratio_cintura_altura(cintura, altura)
        calorias_diarias = calcular_calorias_diarias(tmb, objetivo_enum)
        proteinas, carbohidratos, grasas = calcular_macronutrientes(calorias_diarias, objetivo_enum)

        interpretaciones = {
            "imc": interpretar_imc(imc, ffmi, genero_enum),
            "porcentaje_grasa": interpretar_porcentaje_grasa(porcentaje_grasa, genero_enum),
            "ffmi": interpretar_ffmi(ffmi, genero_enum),
            "rcc": interpretar_rcc(rcc, genero_enum) if genero_enum == Sexo.MUJER else "N/A",
            "ratio_cintura_altura": interpretar_ratio_cintura_altura(ratio_cintura_altura),
        }

        resultados = {
            "tmb": round(tmb, 2),
            "imc": round(imc, 2),
            "porcentaje_grasa": round(porcentaje_grasa, 2),
            "masa_muscular": round(masa_muscular, 2),
            "agua_total": round(agua_total, 2),
            "ffmi": round(ffmi, 2),
            "peso_saludable": {
                "min": round(peso_saludable_min, 2),
                "max": round(peso_saludable_max, 2),
            },
            "sobrepeso": round(sobrepeso, 2),
            "rcc": rcc,
            "ratio_cintura_altura": round(ratio_cintura_altura, 2),
            "calorias_diarias": round(calorias_diarias, 2),
            "macronutrientes": {
                "proteinas": round(proteinas, 2),
                "carbohidratos": round(carbohidratos, 2),
                "grasas": round(grasas, 2),
            },
        }

        return jsonify({"resultados": resultados, "interpretaciones": interpretaciones}), 200

    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500


__all__ = ["informe_bp"]
