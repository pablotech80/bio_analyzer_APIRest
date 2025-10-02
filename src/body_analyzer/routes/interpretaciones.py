from flask import Blueprint, request, jsonify

from src.body_analyzer.utils import convertir_genero
from src.body_analyzer.constantes import *
from src.body_analyzer.interpretaciones import (
    interpretar_imc,
    interpretar_porcentaje_grasa,
    interpretar_ffmi,
    interpretar_rcc,
    interpretar_ratio_cintura_altura,
    interpretar_edad_metabolica_avanzada as interpretar_edad_metabolica_model,
)

interpretaciones_bp = Blueprint("interpretaciones", __name__)


@interpretaciones_bp.route("/interpretar_imc", methods=["POST"])
def interpretar_imc_endpoint():
    data = request.get_json() or {}
    imc = data.get("imc")
    ffmi = data.get("ffmi")
    genero = data.get("genero", "").strip().lower()

    if imc is None or ffmi is None or not genero:
        return jsonify({"error": "Faltan parámetros obligatorios: imc, ffmi o genero"}), 400

    try:
        imc = float(imc)
        ffmi = float(ffmi)
        genero_enum = convertir_genero(genero)
    except (TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400

    try:
        resultado = interpretar_imc(imc, ffmi, genero_enum)
        return jsonify({"interpretacion_imc": resultado}), 200
    except Exception as exc:
        return jsonify({"error": f"Error interno: {exc}"}), 500


@interpretaciones_bp.route("/interpretar_porcentaje_grasa", methods=["POST"])
def interpretar_porcentaje_grasa_endpoint():
    data = request.get_json() or {}
    porcentaje_grasa = data.get("porcentaje_grasa")
    genero = data.get("genero", "").strip().lower()

    if porcentaje_grasa is None or not genero:
        return jsonify({"error": "Faltan parámetros obligatorios: porcentaje_grasa y genero"}), 400

    try:
        porcentaje_grasa = float(porcentaje_grasa)
        genero_enum = convertir_genero(genero)
    except (TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400

    try:
        resultado = interpretar_porcentaje_grasa(porcentaje_grasa, genero_enum)
        return jsonify({"interpretacion_grasa": resultado}), 200
    except Exception as exc:
        return jsonify({"error": f"Error interno: {exc}"}), 500


@interpretaciones_bp.route("/interpretar_ffmi", methods=["POST"])
def interpretar_ffmi_endpoint():
    data = request.get_json() or {}
    ffmi = data.get("ffmi")
    genero = data.get("genero", "").strip().lower()

    if ffmi is None or not genero:
        return jsonify({"error": "Faltan parámetros obligatorios: 'ffmi' y 'genero'"}), 400

    try:
        ffmi = float(ffmi)
        genero_enum = convertir_genero(genero)
    except (TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400

    try:
        resultado = interpretar_ffmi(ffmi, genero_enum)
        return jsonify({"interpretacion_ffmi": resultado}), 200
    except Exception as exc:
        return jsonify({"error": f"Error interno: {exc}"}), 500


@interpretaciones_bp.route("/interpretar_rcc", methods=["POST"])
def interpretar_rcc_endpoint():
    data = request.get_json() or {}
    rcc = data.get("rcc")
    genero = data.get("genero", "").strip().lower()

    if rcc is None or not genero:
        return jsonify({"error": "Faltan parámetros obligatorios: rcc y genero"}), 400

    try:
        rcc = float(rcc)
        genero_enum = convertir_genero(genero)
    except (TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400

    try:
        resultado = interpretar_rcc(rcc, genero_enum)
        return jsonify({"interpretacion_rcc": resultado}), 200
    except Exception as exc:
        return jsonify({"error": f"Error interno: {exc}"}), 500


@interpretaciones_bp.route("/interpretar_ratio_cintura_altura", methods=["POST"])
def interpretar_ratio_cintura_altura_endpoint():
    data = request.get_json() or {}
    ratio = data.get("ratio")

    if ratio is None:
        return jsonify({"error": "Falta el parámetro obligatorio 'ratio'"}), 400

    try:
        ratio = float(ratio)
    except (TypeError, ValueError):
        return jsonify({"error": "El valor de 'ratio' debe ser numérico"}), 400

    try:
        resultado = interpretar_ratio_cintura_altura(ratio)
        return jsonify({"interpretacion_ratio_cintura_altura": resultado}), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": f"Error interno: {exc}"}), 500

@interpretaciones_bp.route("/interpretar_edad_metabolica", methods=["POST"])
def interpretar_edad_metabolica_endpoint():
    data = request.get_json() or {}

    edad_cronologica = data.get("edad_cronologica")
    edad_metabolica = data.get("edad_metabolica")
    imc = data.get("imc")
    porcentaje_grasa = data.get("porcentaje_grasa")
    ratio_cintura_altura = data.get("ratio_cintura_altura")
    genero = data.get("genero", "").strip().lower()

    if None in (
        edad_cronologica,
        edad_metabolica,
        imc,
        porcentaje_grasa,
        ratio_cintura_altura,
    ) or not genero:
        return jsonify({"error": "Faltan parámetros obligatorios"}), 400

    try:
        edad_cronologica = int(edad_cronologica)
        edad_metabolica = int(edad_metabolica)
        imc = float(imc)
        porcentaje_grasa = float(porcentaje_grasa)
        ratio_cintura_altura = float(ratio_cintura_altura)
    except (TypeError, ValueError):
        return jsonify({"error": "Los parámetros deben ser numéricos"}), 400

    try:
        genero_enum = convertir_genero(genero)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    try:
        interpretacion = interpretar_edad_metabolica_model(
            edad_cronologica,
            edad_metabolica,
            imc,
            porcentaje_grasa,
            ratio_cintura_altura,
            genero_enum,
        )
        return jsonify({"interpretacion_edad_metabolica": interpretacion}), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": f"Error interno: {exc}"}), 500

__all__ = ["interpretaciones_bp"]
