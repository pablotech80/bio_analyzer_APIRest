"""Domain services for biometric analysis routes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from werkzeug.datastructures import MultiDict

from app import db
from app.body_analysis.calculos import (calcular_agua_total,
                                        calcular_calorias_diarias,
                                        calcular_edad_metabolica_avanzada,
                                        calcular_ffmi, calcular_imc,
                                        calcular_macronutrientes,
                                        calcular_macronutrientes_porcentajes,
                                        calcular_peso_saludable,
                                        calcular_porcentaje_grasa,
                                        calcular_ratio_cintura_altura,
                                        calcular_rcc, calcular_sobrepeso,
                                        calcular_tmb)
from app.body_analysis.interpretaciones import (
    interpretar_edad_metabolica_avanzada, interpretar_ffmi, interpretar_imc,
    interpretar_porcentaje_grasa, interpretar_ratio_cintura_altura,
    interpretar_rcc)
from app.body_analysis.model import ObjetivoNutricional, Sexo
from app.body_analysis.utils import convertir_genero, convertir_objetivo
from app.models import BiometricAnalysis


class AnalysisValidationError(ValueError):
    """Raised when user input for the biometric analysis is invalid."""


@dataclass
class AnalysisPayload:
    """Convenience container for parsed inputs and computed results."""

    inputs: Dict[str, Any]
    results: Dict[str, Any]
    interpretations: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the payload to a dictionary format."""
        return {
            "inputs": self.inputs,
            "results": self.results,
            "interpretations": self.interpretations,
        }


_DISTRIBUCION_SALUDABLE = {
    "mantener peso": {"proteinas": 25, "carbohidratos": 50, "grasas": 25},
    "perder grasa": {"proteinas": 35, "carbohidratos": 30, "grasas": 35},
    "ganar masa muscular": {"proteinas": 30, "carbohidratos": 55, "grasas": 15},
}

_DISTRIBUCION_FITNESS = {
    "mantener peso": {"proteinas": 30, "carbohidratos": 45, "grasas": 25},
    "perder grasa": {"proteinas": 40, "carbohidratos": 20, "grasas": 40},
    "ganar masa muscular": {"proteinas": 30, "carbohidratos": 50, "grasas": 20},
}


def _clean_str(value: Optional[str]) -> str:
    return (value or "").strip()


def _require(
    form: MultiDict[str, str], field: str, message: Optional[str] = None
) -> str:
    value = _clean_str(form.get(field))
    if not value:
        raise AnalysisValidationError(message or f"El campo '{field}' es obligatorio.")
    return value


def _parse_float(value: str, field: str) -> float:
    try:
        return float(value.replace(",", "."))
    except ValueError as exc:  # pragma: no cover - defensive
        raise AnalysisValidationError(f"'{field}' debe ser un número válido.") from exc


def _parse_positive_float(value: str, field: str) -> float:
    number = _parse_float(value, field)
    if number <= 0:
        raise AnalysisValidationError(f"'{field}' debe ser mayor a cero.")
    return number


def _parse_positive_int(value: str, field: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:  # pragma: no cover - defensive
        raise AnalysisValidationError(f"'{field}' debe ser un entero válido.") from exc
    if number <= 0:
        raise AnalysisValidationError(f"'{field}' debe ser mayor a cero.")
    return number


def run_biometric_analysis(form: MultiDict[str, str]) -> AnalysisPayload:
    """Parse form values, run calculations and return a structured payload."""

    peso = _parse_positive_float(_require(form, "peso"), "peso")
    altura = _parse_positive_float(_require(form, "altura"), "altura")
    edad = _parse_positive_int(_require(form, "edad"), "edad")
    cuello = _parse_positive_float(_require(form, "cuello"), "cuello")
    cintura = _parse_positive_float(_require(form, "cintura"), "cintura")

    genero_str = _require(form, "genero", "Seleccione un género.").lower()
    try:
        genero = convertir_genero(genero_str)
    except ValueError as exc:
        raise AnalysisValidationError(str(exc)) from exc

    cadera_raw = _clean_str(form.get("cadera"))
    if genero == Sexo.MUJER and not cadera_raw:
        raise AnalysisValidationError("Para mujeres, la cadera es un dato obligatorio.")
    cadera = (
        _parse_positive_float(cadera_raw, "cadera")
        if genero == Sexo.MUJER and cadera_raw
        else 0.0
    )

    factor_raw = _require(
        form, "factor_actividad", "Seleccione su nivel de actividad física."
    )
    factor_actividad = _parse_positive_float(factor_raw, "factor_actividad")

    objetivo_str = _clean_str(form.get("objetivo")).lower() or "mantener peso"
    nivel = _clean_str(form.get("nivel")).lower() or None

    proteinas_kg_str = _clean_str(form.get("proteinas_kg"))
    carbohidratos_kg_str = _clean_str(form.get("carbohidratos_kg"))
    grasas_kg_str = _clean_str(form.get("grasas_kg"))

    proteinas_kg = (
        _parse_positive_float(proteinas_kg_str, "proteinas_kg")
        if proteinas_kg_str
        else None
    )
    carbohidratos_kg = (
        _parse_positive_float(carbohidratos_kg_str, "carbohidratos_kg")
        if carbohidratos_kg_str
        else None
    )
    grasas_kg = (
        _parse_positive_float(grasas_kg_str, "grasas_kg") if grasas_kg_str else None
    )

    # Cálculos principales
    porcentaje_grasa = calcular_porcentaje_grasa(
        cintura, cuello, altura, genero, cadera
    )
    tmb = calcular_tmb(peso, altura, edad, genero)
    imc = calcular_imc(peso, altura)

    masa_grasa = peso * (porcentaje_grasa / 100)
    masa_magra = peso - masa_grasa
    agua_total = calcular_agua_total(peso, altura, edad, genero)
    ffmi = calcular_ffmi(masa_magra, altura)
    peso_saludable_min, peso_saludable_max = calcular_peso_saludable(altura)
    sobrepeso = calcular_sobrepeso(peso, altura)
    rcc = calcular_rcc(cintura, cadera) if genero == Sexo.MUJER else None
    ratio_cintura_altura = calcular_ratio_cintura_altura(cintura, altura)

    edad_metabolica = calcular_edad_metabolica_avanzada(
        tmb,
        genero,
        edad,
        imc,
        porcentaje_grasa,
        ratio_cintura_altura,
    )
    interpretacion_edad_metabolica = interpretar_edad_metabolica_avanzada(
        edad,
        edad_metabolica,
        imc,
        porcentaje_grasa,
        ratio_cintura_altura,
        genero,
    )

    tdee = tmb * factor_actividad

    try:
        objetivo_enum: ObjetivoNutricional = convertir_objetivo(objetivo_str)
    except ValueError as exc:
        raise AnalysisValidationError(str(exc)) from exc

    calorias_objetivo = calcular_calorias_diarias(tmb, objetivo_enum, factor_actividad)

    proteinas = carbohidratos = grasas = None

    if nivel in ("saludable", "fitness"):
        distribucion = (
            _DISTRIBUCION_SALUDABLE if nivel == "saludable" else _DISTRIBUCION_FITNESS
        )
        macros = distribucion.get(objetivo_str)
        if macros:
            proteinas, carbohidratos, grasas = calcular_macronutrientes_porcentajes(
                calorias_objetivo,
                macros["proteinas"],
                macros["carbohidratos"],
                macros["grasas"],
            )
    elif nivel == "competicion":
        if all(
            value and value > 0 for value in (proteinas_kg, carbohidratos_kg, grasas_kg)
        ):
            proteinas = peso * proteinas_kg
            carbohidratos = peso * carbohidratos_kg
            grasas = peso * grasas_kg
            calorias_objetivo = (proteinas * 4) + (carbohidratos * 4) + (grasas * 9)
    else:
        proteinas, carbohidratos, grasas = calcular_macronutrientes(
            calorias_objetivo, objetivo_enum
        )

    resultados = {
        "tmb": round(tmb, 2),
        "tdee": round(tdee, 2),
        "edad_metabolica": (
            round(edad_metabolica, 2) if edad_metabolica is not None else None
        ),
        "interpretacion_edad_metabolica": interpretacion_edad_metabolica,
        "imc": round(imc, 2),
        "porcentaje_grasa": round(porcentaje_grasa, 2),
        "masa_magra": round(masa_magra, 2),
        "masa_grasa": round(masa_grasa, 2),
        "agua_total": round(agua_total, 2),
        "ffmi": round(ffmi, 2),
        "peso_saludable": {
            "min": round(peso_saludable_min, 2),
            "max": round(peso_saludable_max, 2),
        },
        "sobrepeso": round(sobrepeso, 2),
        "rcc": round(rcc, 2) if rcc is not None else None,
        "ratio_cintura_altura": round(ratio_cintura_altura, 2),
        "calorias_diarias": round(calorias_objetivo, 2),
        "macronutrientes": {
            "proteinas": round(proteinas, 2) if proteinas is not None else None,
            "carbohidratos": (
                round(carbohidratos, 2) if carbohidratos is not None else None
            ),
            "grasas": round(grasas, 2) if grasas is not None else None,
        },
    }

    interpretaciones = {
        "imc": interpretar_imc(imc, ffmi, genero),
        "porcentaje_grasa": interpretar_porcentaje_grasa(porcentaje_grasa, genero),
        "ffmi": interpretar_ffmi(ffmi, genero),
        "rcc": (
            interpretar_rcc(rcc, genero)
            if genero == Sexo.MUJER and rcc is not None
            else None
        ),
        "ratio_cintura_altura": interpretar_ratio_cintura_altura(ratio_cintura_altura),
        "edad_metabolica": interpretacion_edad_metabolica,
    }

    inputs = {
        "peso": peso,
        "altura": altura,
        "edad": edad,
        "genero": genero.value,
        "cuello": cuello,
        "cintura": cintura,
        "cadera": cadera if genero == Sexo.MUJER else None,
        "factor_actividad": factor_actividad,
        "objetivo": objetivo_str,
        "nivel": nivel,
        "proteinas_kg": proteinas_kg,
        "carbohidratos_kg": carbohidratos_kg,
        "grasas_kg": grasas_kg,
    }

    return AnalysisPayload(
        inputs=inputs, results=resultados, interpretations=interpretaciones
    )


def persist_analysis(user, payload: AnalysisPayload) -> BiometricAnalysis:
    """Persist the analysis snapshot for the current user."""

    inputs = payload.inputs
    resultados = payload.results

    analysis = BiometricAnalysis(
        user=user,
        weight=inputs["peso"],
        height=inputs["altura"],
        age=inputs["edad"],
        gender=inputs["genero"],
        neck=inputs["cuello"],
        waist=inputs["cintura"],
        hip=inputs["cadera"],
        # Medidas musculares opcionales
        biceps=inputs.get("biceps"),
        cuadriceps=inputs.get("cuadriceps"),
        gemelos=inputs.get("gemelos"),
        activity_factor=inputs["factor_actividad"],
        activity_level=inputs.get("nivel"),
        goal=inputs.get("objetivo"),
        bmi=resultados["imc"],
        bmr=resultados["tmb"],
        tdee=resultados["tdee"],
        body_fat_percentage=resultados["porcentaje_grasa"],
        lean_mass=resultados["masa_magra"],
        fat_mass=resultados["masa_grasa"],
        ffmi=resultados["ffmi"],
        body_water=resultados["agua_total"],
        waist_hip_ratio=resultados["rcc"],
        waist_height_ratio=resultados["ratio_cintura_altura"],
        metabolic_age=resultados["edad_metabolica"],
        maintenance_calories=resultados["calorias_diarias"],
        protein_grams=resultados["macronutrientes"].get("proteinas"),
        carbs_grams=resultados["macronutrientes"].get("carbohidratos"),
        fats_grams=resultados["macronutrientes"].get("grasas"),
    )

    db.session.add(analysis)
    db.session.commit()

    return analysis


def build_interpretations_for_record(record: BiometricAnalysis) -> Dict[str, str]:
    """
    Build text interpretations from a stored BiometricAnalysis record.

    Args:
            record: BiometricAnalysis instance from database

    Returns:
            Dict with interpretation labels and descriptions
    """
    #  Convertir género de inglés a español para compatibilidad
    gender_map = {"male": "h", "female": "m", "other": "h"}
    genero_str = gender_map.get(record.gender, "h")

    try:
        genero = convertir_genero(genero_str)
    except ValueError:
        # Fallback si falla la conversión
        from app.body_analysis.model import Sexo

        genero = Sexo.HOMBRE

    interpretaciones = {}

    if record.bmi:
        interpretaciones["imc"] = interpretar_imc(
            record.bmi, record.ffmi or 0.0, genero
        )

    if record.body_fat_percentage:
        interpretaciones["porcentaje_grasa"] = interpretar_porcentaje_grasa(
            record.body_fat_percentage, genero
        )

    if record.ffmi:
        interpretaciones["ffmi"] = interpretar_ffmi(record.ffmi, genero)

    if record.waist_hip_ratio and genero.value == "m":
        interpretaciones["rcc"] = interpretar_rcc(record.waist_hip_ratio, genero)

    if record.waist_height_ratio:
        interpretaciones["ratio_cintura_altura"] = interpretar_ratio_cintura_altura(
            record.waist_height_ratio
        )

    if record.metabolic_age:
        interpretaciones["edad_metabolica"] = interpretar_edad_metabolica_avanzada(
            record.age,
            record.metabolic_age,
            record.bmi or 0.0,
            record.body_fat_percentage or 0.0,
            record.waist_height_ratio or 0.0,
            genero,
        )

    return interpretaciones
