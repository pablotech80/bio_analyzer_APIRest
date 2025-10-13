# app/blueprints/bioanalyze/routes.py
"""
Routes for biometric analysis capture, history and detail views.

Principios CoachBodyFit360:
- SRP: Solo maneja routing y presentación (Controller layer)
- SoC: Lógica de negocio delegada a services/
- API-First: Rutas preparadas para devolver JSON si se solicita
"""
import logging

from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.blueprints.bioanalyze import bioanalyze_bp
from app.blueprints.bioanalyze.services import (
    AnalysisPayload,
    AnalysisValidationError,
    build_interpretations_for_record,
    run_biometric_analysis,
)

# Nuevo servicio centralizado
from app.services.biometric_service import add_fitmaster_analysis, create_analysis
from app.services.biometric_service import delete_analysis as delete_analysis_service
from app.services.biometric_service import get_analysis_by_id, get_user_analyses

logger = logging.getLogger(__name__)


@bioanalyze_bp.route("/nuevo", methods=["GET", "POST"])
@bioanalyze_bp.route("/informe_web", methods=["GET", "POST"])  # Alias legacy
@login_required
def new_analysis():
    """
    Render the biometric analysis form and handle submissions.

    GET: Display empty form
    POST: Process form, create analysis, optionally request FitMaster
    """
    if request.method == "POST":
        try:
            # Validar y procesar datos del formulario
            payload: AnalysisPayload = run_biometric_analysis(request.form)
        except AnalysisValidationError as exc:
            flash(str(exc), "danger")
            return render_template(
                "bioanalyze/form.html",
                form_data=request.form.to_dict(flat=True),
            )

        # 🔥 Mapear datos del formulario español → inglés para el servicio
        biometric_data = {
            # Datos del usuario
            "name": current_user.first_name or current_user.username,
            # Datos básicos (obligatorios)
            "weight": payload.inputs["peso"],
            "height": payload.inputs["altura"],
            "age": payload.inputs["edad"],
            "gender": "male" if payload.inputs["genero"] == "h" else "female",
            "neck": payload.inputs["cuello"],
            "waist": payload.inputs["cintura"],
            "hip": payload.inputs.get("cadera"),
            # Medidas bilaterales (opcionales) desde el formulario
            "biceps_left": float(request.form.get("biceps_izq") or 0) or None,
            "biceps_right": float(request.form.get("biceps_der") or 0) or None,
            "thigh_left": float(request.form.get("muslo_izq") or 0) or None,
            "thigh_right": float(request.form.get("muslo_der") or 0) or None,
            "calf_left": float(request.form.get("gemelo_izq") or 0) or None,
            "calf_right": float(request.form.get("gemelo_der") or 0) or None,
            # Activity data
            "activity_factor": payload.inputs["factor_actividad"],
            "activity_level": "moderate",  # Default, puedes mapear del factor
            "goal": payload.inputs["objetivo"],
            # Métricas calculadas
            "bmi": payload.results["imc"],
            "bmr": payload.results["tmb"],
            "tdee": payload.results["tdee"],
            "body_fat_percentage": payload.results["porcentaje_grasa"],
            "lean_mass": payload.results["masa_magra"],
            "fat_mass": payload.results["masa_grasa"],
            "ffmi": payload.results["ffmi"],
            "body_water": payload.results["agua_total"],
            "waist_hip_ratio": payload.results.get("rcc"),
            "waist_height_ratio": payload.results["ratio_cintura_altura"],
            "metabolic_age": payload.results.get("edad_metabolica"),
            "maintenance_calories": payload.results["calorias_diarias"],
            "protein_grams": payload.results["macronutrientes"].get("proteinas"),
            "carbs_grams": payload.results["macronutrientes"].get("carbohidratos"),
            "fats_grams": payload.results["macronutrientes"].get("grasas"),
        }

        # Crear análisis usando el servicio
        analysis, error = create_analysis(
            user_id=current_user.id,
            biometric_data=biometric_data,
            request_fitmaster=True,  # Siempre pedir FitMaster
        )

        if error:
            flash(f"Error al crear análisis: {error}", "danger")
            return render_template(
                "bioanalyze/form.html",
                form_data=request.form.to_dict(flat=True),
            )

        # Success
        logger.info(f"Analysis created: ID={analysis.id} for user={current_user.id}")

        if analysis.has_fitmaster_analysis:
            flash("Análisis guardado con interpretación de FitMaster AI.", "success")
        else:
            flash("Análisis guardado. (FitMaster AI no disponible)", "warning")

        return redirect(url_for("bioanalyze.result", analysis_id=analysis.id))

    # GET: Mostrar formulario vacío
    return render_template("bioanalyze/form.html", form_data={})


@bioanalyze_bp.route("/historial")
@login_required
def history():
    """
    List the authenticated user's previous biometric analyses.

    Returns HTML or JSON based on Accept header.
    """
    # Obtener análisis del usuario
    analyses = get_user_analyses(current_user.id, limit=50)

    # Si se solicita JSON (API)
    if request.accept_mimetypes.best == "application/json":
        return (
            jsonify(
                {
                    "success": True,
                    "count": len(analyses),
                    "analyses": [a.to_dict(include_fitmaster=False) for a in analyses],
                }
            ),
            200,
        )

    # HTML (web)
    return render_template("bioanalyze/history.html", analyses=analyses)


@bioanalyze_bp.route("/resultado/<int:analysis_id>")
@bioanalyze_bp.route("/informe_web/<int:analysis_id>")  # Alias legacy
@login_required
def result(analysis_id: int):
    """
    Display a stored analysis with its interpretations and FitMaster plan.

    Args:
            analysis_id: ID of the analysis to display

    Returns:
            HTML page with analysis details and AI interpretation
    """
    # Obtener análisis
    analysis = get_analysis_by_id(analysis_id)

    if not analysis:
        flash("Análisis no encontrado.", "danger")
        return redirect(url_for("bioanalyze.history"))

    # Verificar ownership (admins pueden ver todos los análisis)
    if analysis.user_id != current_user.id and not current_user.is_admin:
        flash("No tienes permiso para ver este análisis.", "danger")
        return redirect(url_for("bioanalyze.history"))

    # Construir interpretaciones (del servicio legacy)
    interpretaciones = build_interpretations_for_record(analysis)

    # Preparar datos de FitMaster
    fitmaster_data = None
    if analysis.has_fitmaster_analysis:
        fitmaster_data = analysis.fitmaster_data

    # Si se solicita JSON (API)
    if request.accept_mimetypes.best == "application/json":
        return (
            jsonify(
                {
                    "success": True,
                    "analysis": analysis.to_dict(include_fitmaster=True),
                    "interpretations": interpretaciones,
                }
            ),
            200,
        )

    # HTML (web)
    return render_template(
        "bioanalyze/result.html",
        analysis=analysis,
        interpretaciones=interpretaciones,
        fitmaster_data=fitmaster_data,
    )


@bioanalyze_bp.route("/historial/<int:analysis_id>/eliminar", methods=["POST"])
@login_required
def delete(analysis_id: int):
    """
    Delete a biometric analysis (with ownership verification).

    Args:
            analysis_id: ID of the analysis to delete

    Returns:
            Redirect to history page
    """
    success, error = delete_analysis_service(analysis_id, current_user.id)

    if not success:
        flash(f"Error: {error}", "danger")
    else:
        flash(f"Análisis #{analysis_id} eliminado.", "info")

    return redirect(url_for("bioanalyze.history"))


@bioanalyze_bp.route("/resultado/<int:analysis_id>/solicitar-ia", methods=["POST"])
@login_required
def request_ai_analysis(analysis_id: int):
    """
    Manually request FitMaster analysis for an existing record.

    Useful if:
    - Original analysis failed to get FitMaster
    - User wants to regenerate with updated AI model

    Args:
            analysis_id: ID of the analysis

    Returns:
            Redirect to result page
    """
    # Obtener análisis
    analysis = get_analysis_by_id(analysis_id)

    if not analysis:
        flash("Análisis no encontrado.", "danger")
        return redirect(url_for("bioanalyze.history"))

    # Verificar ownership (admins pueden ver todos los análisis)
    if analysis.user_id != current_user.id and not current_user.is_admin:
        flash("No tienes permiso para modificar este análisis.", "danger")
        return redirect(url_for("bioanalyze.history"))

    # Preparar datos biométricos del análisis existente
    biometric_data = analysis.to_dict(include_fitmaster=False)

    # Agregar nombre del usuario para personalización
    biometric_data["name"] = analysis.user.first_name or analysis.user.username

    # Solicitar análisis FitMaster
    error = add_fitmaster_analysis(analysis_id, biometric_data)

    if error:
        flash(f"Error al solicitar FitMaster: {error}", "warning")
    else:
        flash("Análisis de FitMaster AI generado exitosamente.", "success")

    return redirect(url_for("bioanalyze.result", analysis_id=analysis_id))


# ========== LEGACY ROUTES (mantener por compatibilidad) ==========


@bioanalyze_bp.route("/debug/<int:analysis_id>")
@login_required
def debug_analysis(analysis_id: int):
    """
    Debug route: Display raw FitMaster data for troubleshooting.

    Restricted to admin users only.
    """
    # Verificar que el usuario es admin
    if not current_user.is_admin:
        flash("Acceso denegado. Solo administradores pueden ver esta página.", "danger")
        return redirect(url_for("bioanalyze.history"))

    analysis = get_analysis_by_id(analysis_id)

    if not analysis:
        return "<h1>Análisis no encontrado</h1>", 404

    if analysis.user_id != current_user.id:
        return "<h1>Sin permiso</h1>", 403

    # Datos de debug
    has_fitmaster = "SÍ" if analysis.has_fitmaster_analysis else "NO"
    fitmaster_version = analysis.fitmaster_model_version or "N/A"
    fitmaster_date = analysis.fitmaster_generated_at or "N/A"

    fitmaster_content = ""
    if analysis.fitmaster_data:
        import json

        fitmaster_content = json.dumps(
            analysis.fitmaster_data, indent=2, ensure_ascii=False
        )

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Debug - Análisis #{analysis.id}</title>
        <style>
            body {{ font-family: monospace; padding: 20px; }}
            h1 {{ color: #333; }}
            .info {{ background: #f0f0f0; padding: 10px; margin: 10px 0; }}
            textarea {{ width: 100%; height: 400px; font-family: monospace; }}
        </style>
    </head>
    <body>
        <h1>🔍 Debug FitMaster - Análisis #{analysis.id}</h1>

        <div class="info">
            <strong>Usuario:</strong> {analysis.user_id}<br>
            <strong>Fecha creación:</strong> {analysis.created_at}<br>
            <strong>¿Tiene FitMaster?:</strong> {has_fitmaster}<br>
            <strong>Versión modelo:</strong> {fitmaster_version}<br>
            <strong>Generado el:</strong> {fitmaster_date}
        </div>

        <h2>Datos Biométricos:</h2>
        <div class="info">
            Peso: {analysis.weight} kg<br>
            Altura: {analysis.height} cm<br>
            Edad: {analysis.age} años<br>
            Género: {analysis.gender}<br>
            Bíceps L/R: {analysis.biceps_left} / {analysis.biceps_right} cm<br>
            Muslo L/R: {analysis.thigh_left} / {analysis.thigh_right} cm<br>
            Gemelo L/R: {analysis.calf_left} / {analysis.calf_right} cm
        </div>

        <h2>FitMaster Data (JSON):</h2>
        <textarea readonly>{fitmaster_content or "No hay datos de FitMaster"}</textarea>

        <p>
            <a href="{url_for('bioanalyze.result', analysis_id=analysis.id)}">← Volver al análisis</a> |
            <a href="{url_for('bioanalyze.history')}">Ver historial</a> |
            <a href="{url_for('bioanalyze.new_analysis')}">Nuevo análisis</a>
        </p>
    </body>
    </html>
    """


# Alias para compatibilidad con código existente
analysis_detail = result
