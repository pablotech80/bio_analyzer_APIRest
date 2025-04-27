from flask import Blueprint, request, jsonify
from src.body_analyzer.model import Sexo
from src.body_analyzer.utils import convertir_genero
from src.body_analyzer.constantes import *
from src.body_analyzer.interpretaciones import (
    interpretar_imc,
    interpretar_porcentaje_grasa,
    interpretar_ffmi,
    interpretar_rcc,
    interpretar_ratio_cintura_altura,
)

interpretaciones_bp = Blueprint("interpretaciones", __name__)


@interpretaciones_bp.route("/interpretar_imc", methods=["POST"])
def interpretar_imc_endpoint():
    try:
        data = request.get_json()
        imc = data.get("imc")
        ffmi = data.get("ffmi")
        genero = data.get("genero", "").strip().lower()

        if imc is None or ffmi is None or genero is None:
            return jsonify({"error": "Faltan parámetros obligatorios: imc, ffmi o genero"}), 400

        imc = float(imc)
        ffmi = float(ffmi)
        genero_enum = convertir_genero(genero)

        resultado = interpretar_imc(imc, ffmi, genero_enum)
        return jsonify({"interpretacion_imc": resultado}), 200

    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500


@interpretaciones_bp.route("/interpretar_porcentaje_grasa", methods=["POST"])
def interpretar_porcentaje_grasa_endpoint():
    try:
        data = request.get_json()
        porcentaje_grasa = data.get("porcentaje_grasa")
        genero = data.get("genero", "").strip().lower()

        if porcentaje_grasa is None or genero is None:
            return jsonify({"error": "Faltan parámetros obligatorios: porcentaje_grasa y genero"}), 400

        porcentaje_grasa = float(porcentaje_grasa)
        genero_enum = convertir_genero(genero)

        resultado = interpretar_porcentaje_grasa(porcentaje_grasa, genero_enum)
        return jsonify({"interpretacion_grasa": resultado}), 200

    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500


@interpretaciones_bp.route("/interpretar_ffmi", methods=["POST"])
def interpretar_ffmi_endpoint():
    try:
        data = request.get_json()
        ffmi = data.get("ffmi")
        genero = data.get("genero", "").strip().lower()

        if ffmi is None or genero is None:
            return jsonify({"error": "Faltan parámetros obligatorios: 'ffmi' y 'genero'"}), 400

        ffmi = float(ffmi)
        genero_enum = convertir_genero(genero)

        resultado = interpretar_ffmi(ffmi, genero_enum)
        return jsonify({"interpretacion_ffmi": resultado}), 200

    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500


@interpretaciones_bp.route("/interpretar_rcc", methods=["POST"])
def interpretar_rcc_endpoint():
    try:
        data = request.get_json()
        rcc = data.get("rcc")
        genero = data.get("genero", "").strip().lower()

        if rcc is None or genero is None:
            return jsonify({"error": "Faltan parámetros obligatorios: rcc y genero"}), 400

        rcc = float(rcc)
        genero_enum = convertir_genero(genero)

        resultado = interpretar_rcc(rcc, genero_enum)
        return jsonify({"interpretacion_rcc": resultado}), 200

    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500


@interpretaciones_bp.route("/interpretar_ratio_cintura_altura", methods=["POST"])
def interpretar_ratio_cintura_altura_endpoint():
    try:
        data = request.get_json()
        ratio = data.get("ratio")

        if ratio is None:
            return jsonify({"error": "Falta el parámetro obligatorio 'ratio'"}), 400

        ratio = float(ratio)
        if ratio <= 0:
            return jsonify({"error": "El valor de 'ratio' debe ser positivo"}), 400

        resultado = interpretar_ratio_cintura_altura(ratio)
        return jsonify({"interpretacion_ratio_cintura_altura": resultado}), 200

    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

@interpretaciones_bp.route("/interpretar_edad_metabolica", methods=["POST"])
def interpretar_edad_metabolica_avanzada(edad_cronologica, edad_metabolica, imc, porcentaje_grasa, ratio_cintura_altura, genero):
    """
        Interpretación clínica de la edad metabólica, considerando también obesidad, grasa corporal y obesidad abdominal.
        """

    # Detectar si existe obesidad o problemas serios de composición corporal
    obesidad_detectada = (
            imc >= 30 or
            (genero == "hombre" and porcentaje_grasa >= 25) or
            (genero == "mujer" and porcentaje_grasa >= 32) or
            ratio_cintura_altura > 0.5
    )

    diferencia = edad_metabolica - edad_cronologica

    if obesidad_detectada:
        if diferencia <= 5:
            return "Tu metabolismo en reposo es aceptable, pero tu composición corporal indica un riesgo metabólico significativo. Se recomienda mejora urgente."
        else:
            return "Estado metabólico alterado debido a obesidad o composición corporal desfavorable. Riesgo metabólico elevado."
    else:
        if diferencia <= -5:
            return "Excelente estado metabólico: tu metabolismo y composición corporal son muy buenos para tu edad."
        elif -5 < diferencia <= 5:
            return "Buen estado metabólico: tu metabolismo y composición corporal son adecuados para tu edad."
        elif 5 < diferencia <= 10:
            return "Estado metabólico moderadamente envejecido: sería ideal mejorar tu condición física general."
        else:
            return "Estado metabólico envejecido: se recomienda intervención en estilo de vida y salud metabólica."

__all__ = ["interpretaciones_bp"]
