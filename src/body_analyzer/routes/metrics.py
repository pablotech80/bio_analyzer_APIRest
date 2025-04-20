from flask import Blueprint, request, jsonify
from src.body_analyzer.calculos import (
    calcular_porcentaje_grasa,
    calcular_peso_grasa_corporal,
    calcular_sobrepeso,
    calcular_rcc,
    calcular_tmb,
    calcular_imc,
    calcular_agua_total,
    calcular_peso_saludable,
)
from src.body_analyzer.utils import convertir_genero

metrics_bp = Blueprint("metrics", __name__)


@metrics_bp.route("/calcular_porcentaje_grasa", methods=["POST"])
def calcular_porcentaje_grasa_endpoint():
    try:
        data = request.get_json()
        cintura = data.get("cintura")
        cuello = data.get("cuello")
        altura = data.get("altura")
        genero = data.get("genero", "").strip().lower()
        cadera = data.get("cadera")

        if None in (cintura, cuello, altura, genero):
            return jsonify({"error": "Faltan parámetros obligatorios"}), 400

        if genero == "m" and cadera is None:
            return jsonify({"error": "Para mujeres, la cadera debe ser especificada."}), 400

        genero_enum = convertir_genero(genero)
        porcentaje_grasa = calcular_porcentaje_grasa(cintura, cuello, altura, genero_enum, cadera)
        return jsonify({"porcentaje_grasa": round(porcentaje_grasa, 2)}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500


@metrics_bp.route("/calcular_peso_grasa_corporal", methods=["POST"])
def calcular_peso_grasa_corporal_endpoint():
    try:
        data = request.get_json()
        peso = data.get("peso")
        porcentaje_grasa = data.get("porcentaje_grasa")

        if peso is None or porcentaje_grasa is None:
            return jsonify({"error": "Faltan parámetros obligatorios: 'peso' y 'porcentaje_grasa'."}), 400

        if not isinstance(peso, (float, int)) or not isinstance(porcentaje_grasa, (float, int)):
            return jsonify({"error": "Ambos valores deben ser numéricos."}), 400

        if peso <= 0 or not (0 <= porcentaje_grasa <= 100):
            return jsonify({"error": "Peso debe ser positivo y grasa entre 0 y 100."}), 400

        resultado = calcular_peso_grasa_corporal(peso, porcentaje_grasa)
        return jsonify({"peso_grasa_corporal": resultado}), 200

    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500


@metrics_bp.route("/calcular_sobrepeso", methods=["POST"])
def calcular_sobrepeso_endpoint():
    try:
        data = request.get_json()
        peso = data.get("peso")
        altura = data.get("altura")

        if None in (peso, altura):
            return jsonify({"error": "Faltan parámetros obligatorios: peso y altura"}), 400

        if not isinstance(peso, (float, int)) or not isinstance(altura, (float, int)):
            return jsonify({"error": "Los parámetros deben ser numéricos."}), 400

        if peso <= 0 or altura <= 0:
            return jsonify({"error": "Los valores deben ser mayores que cero."}), 400

        resultado = calcular_sobrepeso(peso, altura)
        return jsonify({"sobrepeso": round(resultado, 2)}), 200

    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500


@metrics_bp.route("/calcular_rcc", methods=["POST"])
def calcular_rcc_endpoint():
    try:
        data = request.get_json()
        cintura = data.get("cintura")
        cadera = data.get("cadera")

        if None in (cintura, cadera):
            return jsonify({"error": "Faltan parámetros obligatorios"}), 400

        resultado = calcular_rcc(cintura, cadera)
        return jsonify({"rcc": resultado}), 200

    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500


@metrics_bp.route("/calcular_tmb", methods=["POST"])
def calcular_tmb_endpoint():
    try:
        data = request.get_json()
        peso = data.get("peso")
        altura = data.get("altura")
        edad = data.get("edad")
        genero = data.get("genero", "").strip().lower()

        if None in (peso, altura, edad, genero):
            return jsonify({"error": "Faltan parámetros obligatorios"}), 400

        peso = float(peso)
        altura = float(altura)
        edad = int(edad)

        genero_enum = convertir_genero(genero)
        tmb = calcular_tmb(peso, altura, edad, genero_enum)

        return jsonify({"tmb": round(tmb, 2)}), 200

    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500


@metrics_bp.route("/calcular_imc", methods=["POST"])
def calcular_imc_endpoint():
    try:
        data = request.get_json()
        peso = data.get("peso")
        altura = data.get("altura")

        if None in (peso, altura):
            return jsonify({"error": "Faltan parámetros obligatorios"}), 400

        resultado = calcular_imc(peso, altura)
        return jsonify({"imc": resultado}), 200

    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500


@metrics_bp.route("/calcular_agua_total", methods=["POST"])
def calcular_agua_total_endpoint():
    try:
        data = request.get_json()
        peso = data.get("peso")
        altura = data.get("altura")
        edad = data.get("edad")
        genero = data.get("genero", "").strip().lower()

        if None in (peso, altura, edad, genero):
            return jsonify({"error": "Faltan parámetros obligatorios"}), 400

        genero_enum = convertir_genero(genero)
        resultado = calcular_agua_total(peso, altura, edad, genero_enum)

        return jsonify({"agua_total": resultado}), 200

    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500


@metrics_bp.route("/calcular_peso_saludable", methods=["POST"])
def calcular_peso_saludable_endpoint():
    try:
        data = request.get_json()
        altura = data.get("altura")

        if altura is None:
            return jsonify({"error": "Falta el parámetro obligatorio 'altura'"}), 400

        resultado_min, resultado_max = calcular_peso_saludable(altura)
        return jsonify({
            "peso_min": f"{resultado_min:.2f}",
            "peso_max": f"{resultado_max:.2f}"
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500


__all__ = ["metrics_bp"]
