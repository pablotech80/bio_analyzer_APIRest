"""Domain services for biometric analysis routes."""

from __future__ import annotations

from typing import Dict

from app import db
from app.body_analysis.interpretaciones import (
    interpretar_edad_metabolica_avanzada,
    interpretar_ffmi,
    interpretar_imc,
    interpretar_porcentaje_grasa,
    interpretar_ratio_cintura_altura,
    interpretar_rcc,
)
from app.body_analysis.utils import convertir_genero
from app.models import BiometricAnalysis

from apps.bioanalyze.core import AnalysisPayload, AnalysisValidationError, run_biometric_analysis


 # The pure calculation core moved to apps.bioanalyze.core.


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
