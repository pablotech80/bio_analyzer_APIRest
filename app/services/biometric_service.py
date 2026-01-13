# app/services/biometric_service.py
"""
Biometric Analysis Service - Business Logic Layer

Principios CoachBodyFit360:
- SRP: Solo maneja lógica de negocio de análisis biométricos
- SoC: Separado de routes (controller) y models (persistencia)
- DRY: Funciones reutilizables desde cualquier blueprint
"""
import logging
from datetime import datetime
from typing import Dict, Optional, Tuple

from app import db
from app.models.biometric_analysis import BiometricAnalysis
from app.services.fitmaster_service import FitMasterService

logger = logging.getLogger(__name__)


class BiometricServiceError(Exception):
    """Custom exception for biometric service errors."""

    pass


def create_analysis(
    user_id: int, biometric_data: Dict, request_fitmaster: bool = True
) -> Tuple[BiometricAnalysis, Optional[str]]:
    """
    Create a new biometric analysis with optional FitMaster interpretation.

    Args:
            user_id: ID of the user
            biometric_data: Dict with biometric measurements
                    Required: weight, height, age, gender, neck, waist
                    Optional: hip, biceps_left, biceps_right, thigh_left, thigh_right,
                                     calf_left, calf_right, activity_level, goal
            request_fitmaster: Whether to request FitMaster AI analysis

    Returns:
            Tuple[BiometricAnalysis, Optional[str]]: (analysis_object, error_message)
            - If successful: (analysis, None)
            - If error: (None, error_message)

    Raises:
            BiometricServiceError: For validation or persistence errors

    Example:
            >>> data = {
            ...     'weight': 75.5,
            ...     'height': 175,
            ...     'age': 30,
            ...     'gender': 'male',
            ...     'neck': 38,
            ...     'waist': 85,
            ...     'biceps_left': 35.2,
            ...     'biceps_right': 35.8
            ... }
            >>> analysis, error = create_analysis(user_id=1, biometric_data=data)
            >>> if error:
            ...     print(f"Error: {error}")
            ... else:
            ...     print(f"Created analysis ID: {analysis.id}")
    """
    try:
        # Validate required fields
        required_fields = ["weight", "height", "age", "gender", "neck", "waist"]
        missing_fields = [
            field for field in required_fields if field not in biometric_data
        ]

        if missing_fields:
            error_msg = f"Missing required fields: {', '.join(missing_fields)}"
            logger.error(error_msg)
            return None, error_msg

        # Validate gender value
        valid_genders = ["male", "female", "other"]
        if biometric_data["gender"] not in valid_genders:
            error_msg = f"Invalid gender. Must be one of: {', '.join(valid_genders)}"
            logger.error(error_msg)
            return None, error_msg

        # Create analysis object
        analysis = BiometricAnalysis(
            user_id=user_id,
            weight=biometric_data["weight"],
            height=biometric_data["height"],
            age=biometric_data["age"],
            gender=biometric_data["gender"],
            neck=biometric_data["neck"],
            waist=biometric_data["waist"],
            hip=biometric_data.get("hip"),
            # Bilateral measurements
            biceps_left=biometric_data.get("biceps_left"),
            biceps_right=biometric_data.get("biceps_right"),
            thigh_left=biometric_data.get("thigh_left"),
            thigh_right=biometric_data.get("thigh_right"),
            calf_left=biometric_data.get("calf_left"),
            calf_right=biometric_data.get("calf_right"),
            # Activity data
            activity_factor=biometric_data.get("activity_factor"),
            activity_level=biometric_data.get("activity_level"),
            goal=biometric_data.get("goal"),
            # Calculated metrics (if provided)
            bmi=biometric_data.get("bmi"),
            bmr=biometric_data.get("bmr"),
            tdee=biometric_data.get("tdee"),
            body_fat_percentage=biometric_data.get("body_fat_percentage"),
            lean_mass=biometric_data.get("lean_mass"),
            fat_mass=biometric_data.get("fat_mass"),
            ffmi=biometric_data.get("ffmi"),
            body_water=biometric_data.get("body_water"),
            waist_hip_ratio=biometric_data.get("waist_hip_ratio"),
            waist_height_ratio=biometric_data.get("waist_height_ratio"),
            metabolic_age=biometric_data.get("metabolic_age"),
            maintenance_calories=biometric_data.get("maintenance_calories"),
            protein_grams=biometric_data.get("protein_grams"),
            carbs_grams=biometric_data.get("carbs_grams"),
            fats_grams=biometric_data.get("fats_grams"),
        )

        # Save to database first (to get ID)
        db.session.add(analysis)
        db.session.commit()

        logger.info(
            f"Created biometric analysis ID={analysis.id} for user_id={user_id}"
        )

        # Request FitMaster analysis if enabled
        if request_fitmaster:
            fitmaster_error = add_fitmaster_analysis(analysis.id, biometric_data)
            if fitmaster_error:
                logger.warning(
                    f"FitMaster analysis failed for ID={analysis.id}: {fitmaster_error}"
                )
            # Don't fail the entire operation, just log the warning

        return analysis, None

    except Exception as e:
        db.session.rollback()
        error_msg = f"Error creating biometric analysis: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return None, error_msg


def add_fitmaster_analysis(analysis_id: int, biometric_data: Dict) -> Optional[str]:
    """
    Add FitMaster AI interpretation to an existing analysis.

    Args:
            analysis_id: ID of the biometric analysis
            biometric_data: Dict with biometric measurements for FitMaster

    Returns:
            Optional[str]: Error message if failed, None if successful

    Example:
            >>> error = add_fitmaster_analysis(analysis_id=1, biometric_data=data)
            >>> if error:
            ...     print(f"FitMaster failed: {error}")
    """
    try:
        # Get analysis from database
        analysis = BiometricAnalysis.query.get(analysis_id)
        if not analysis:
            return f"Analysis with ID={analysis_id} not found"

        # Call FitMaster service
        logger.info(f"Requesting FitMaster analysis for ID={analysis_id}")
        fitmaster_response = FitMasterService.analyze_bio_results(biometric_data)

        if not fitmaster_response:
            return "FitMaster service returned empty response"

        # Structure the response
        fitmaster_data = {
            "interpretation": fitmaster_response.get("interpretation", ""),
            "nutrition_plan": fitmaster_response.get("nutrition_plan", {}),
            "training_plan": fitmaster_response.get("training_plan", {}),
            "generated_at": datetime.utcnow().isoformat(),
            "model_version": fitmaster_response.get("model_version", "fitmaster-v1.0"),
        }

        # Save to database
        analysis.fitmaster_data = fitmaster_data
        db.session.commit()

        logger.info(f"FitMaster analysis saved for ID={analysis_id}")
        return None

    except Exception as e:
        db.session.rollback()
        error_msg = f"Error adding FitMaster analysis: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg


def get_user_analyses(user_id: int, limit: int = 10) -> list:
    """
    Get all biometric analyses for a user, ordered by most recent.

    Args:
            user_id: ID of the user
            limit: Maximum number of results (default: 10)

    Returns:
            list: List of BiometricAnalysis objects

    Example:
            >>> analyses = get_user_analyses(user_id=1, limit=5)
            >>> for analysis in analyses:
            ...     print(f"ID: {analysis.id}, Date: {analysis.created_at}")
    """
    return (
        BiometricAnalysis.query.filter_by(user_id=user_id)
        .order_by(BiometricAnalysis.created_at.desc())
        .limit(limit)
        .all()
    )


def get_analysis_by_id(analysis_id: int) -> Optional[BiometricAnalysis]:
    """
    Get a specific biometric analysis by ID.

    Args:
            analysis_id: ID of the analysis

    Returns:
            Optional[BiometricAnalysis]: Analysis object or None if not found

    Example:
            >>> analysis = get_analysis_by_id(1)
            >>> if analysis:
            ...     print(f"Weight: {analysis.weight} kg")
    """
    return BiometricAnalysis.query.get(analysis_id)


def delete_analysis(analysis_id: int, user_id: int) -> Tuple[bool, Optional[str]]:
    """
    Delete a biometric analysis (with user ownership verification).
    Eliminará en cascada todos los registros relacionados (nutrition_plans, training_plans, etc.)

    Args:
            analysis_id: ID of the analysis to delete
            user_id: ID of the user (for authorization check)

    Returns:
            Tuple[bool, Optional[str]]: (success, error_message)

    Example:
            >>> success, error = delete_analysis(analysis_id=1, user_id=1)
            >>> if not success:
            ...     print(f"Error: {error}")
    """
    try:
        analysis = BiometricAnalysis.query.get(analysis_id)

        if not analysis:
            return False, f"Analysis with ID={analysis_id} not found"

        # Verify ownership
        if analysis.user_id != user_id:
            return False, "Unauthorized: Analysis belongs to another user"

        # Eliminar registros relacionados primero para evitar violación de clave foránea
        try:
            # Eliminar nutrition_plans relacionados
            from app.models.nutrition_plan import NutritionPlan
            NutritionPlan.query.filter_by(analysis_id=analysis_id).delete()
            
            # Eliminar training_plans relacionados
            from app.models.training_plan import TrainingPlan
            TrainingPlan.query.filter_by(analysis_id=analysis_id).delete()
            
            logger.info(f"Deleted related records for analysis ID={analysis_id}")
        except Exception as related_error:
            logger.warning(f"Error deleting related records: {str(related_error)}")
            # Continuar con la eliminación del análisis de todas formas

        # Ahora eliminar el análisis principal
        db.session.delete(analysis)
        db.session.commit()

        logger.info(f"Deleted analysis ID={analysis_id} by user_id={user_id}")
        return True, None

    except Exception as e:
        db.session.rollback()
        error_msg = f"Error deleting analysis: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg


def update_fitmaster_data(
    analysis_id: int, fitmaster_data: Dict
) -> Tuple[bool, Optional[str]]:
    """
    Update FitMaster data for an existing analysis (e.g., after recalculation).

    Args:
            analysis_id: ID of the analysis
            fitmaster_data: New FitMaster data dict

    Returns:
            Tuple[bool, Optional[str]]: (success, error_message)
    """
    try:
        analysis = BiometricAnalysis.query.get(analysis_id)

        if not analysis:
            return False, f"Analysis with ID={analysis_id} not found"

        analysis.fitmaster_data = fitmaster_data
        db.session.commit()

        logger.info(f"Updated FitMaster data for analysis ID={analysis_id}")
        return True, None

    except Exception as e:
        db.session.rollback()
        error_msg = f"Error updating FitMaster data: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg
