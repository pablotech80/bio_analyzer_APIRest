from flask import Blueprint, request, jsonify
from src.body_analyzer.calculos import (calcular_tmb, calcular_calorias_diarias,
                                        calcular_macronutrientes, calcular_macronutrientes_porcentajes)
from src.body_analyzer.utils import convertir_genero, convertir_objetivo

nutricion_bp = Blueprint("nutricion", __name__)


@nutricion_bp.route("/calorias_diarias", methods=["POST"])
def calorias_diarias_endpoint():
    """
    Calcula las calorías diarias recomendadas a partir de peso, altura, edad, género y objetivo.
    """
    try:
        data = request.get_json()

        peso = data.get("peso")
        altura = data.get("altura")
        edad = data.get("edad")
        genero = data.get("genero", "").strip().lower()
        objetivo = data.get("objetivo")

        if None in (peso, altura, edad, genero, objetivo):
            return jsonify({"error": "Faltan parámetros obligatorios"}), 400

        peso = float(peso)
        altura = float(altura)
        edad = int(edad)

        if peso <= 0 or altura <= 0 or edad <= 0:
            return jsonify({"error": "Peso, altura y edad deben ser mayores que cero."}), 400

        genero_enum = convertir_genero(genero)
        objetivo_enum = convertir_objetivo(objetivo)

        tmb = calcular_tmb(peso, altura, edad, genero_enum)
        calorias_diarias = round(calcular_calorias_diarias(tmb, objetivo_enum), 2)

        return jsonify({"calorias_diarias": calorias_diarias}), 200

    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500


@nutricion_bp.route("/macronutrientes", methods=["POST"])
def macronutrientes_endpoint():
    """
    Calcula los macronutrientes diarios recomendados según las calorías diarias y el objetivo.
    """
    try:
        data = request.get_json()
        calorias_diarias = data.get("calorias_diarias")
        objetivo = data.get("objetivo")

        if calorias_diarias is None or objetivo is None:
            return jsonify({"error": "Faltan parámetros obligatorios"}), 400

        calorias_diarias = float(calorias_diarias)
        if calorias_diarias <= 0:
            return jsonify({"error": "Las calorías deben ser un número positivo."}), 400

        objetivo_enum = convertir_objetivo(objetivo)

        proteinas, carbohidratos, grasas = calcular_macronutrientes(
            calorias_diarias, objetivo_enum
        )

        return jsonify({
            "macronutrientes": {
                "proteinas": round(proteinas, 2),
                "carbohidratos": round(carbohidratos, 2),
                "grasas": round(grasas, 2),
            }
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500


@nutricion_bp.route("/macros_porcentajes", methods=["POST"])
def calcular_macronutrientes_porcentajes_endpoint():
    """
    Endpoint para calcular los gramos de proteínas, carbohidratos y grasas a partir del reparto porcentual de calorías.
    """
    try:
        data = request.get_json()

        calorias = float(data.get("calorias"))
        porcentaje_proteinas = float(data.get("porcentaje_proteinas"))
        porcentaje_carbohidratos = float(data.get("porcentaje_carbohidratos"))
        porcentaje_grasas = float(data.get("porcentaje_grasas"))

        # Llamada a la función de cálculo
        proteinas, carbohidratos, grasas = calcular_macronutrientes_porcentajes(
            calorias,
            porcentaje_proteinas,
            porcentaje_carbohidratos,
            porcentaje_grasas
        )

        return jsonify({
            "macronutrientes": {
                "proteinas": round(proteinas, 2),
                "carbohidratos": round(carbohidratos, 2),
                "grasas": round(grasas, 2)
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


__all__ = ["nutricion_bp"]
