"""Routes for biometric analysis capture, history and detail views."""
import json
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.models import BiometricAnalysis
from app.blueprints.bioanalyze import bioanalyze_bp
from app.blueprints.bioanalyze.services import (
    AnalysisPayload,
    AnalysisValidationError,
    build_interpretations_for_record,
    persist_analysis,
    run_biometric_analysis,
)

# Importamos el servicio FitMaster y la base de datos
from app.services.fitmaster_service import FitMasterService
from app import db


@bioanalyze_bp.route("/informe_web", methods=["GET", "POST"])
@login_required
def informe_web():
    """Render the biometric analysis form and handle submissions."""
    
    if request.method == "POST":
        try:
            payload: AnalysisPayload = run_biometric_analysis(request.form)
        except AnalysisValidationError as exc:
            flash(str(exc), "danger")
            return render_template(
                "bioanalyze/form.html",
                form_data=request.form.to_dict(flat=True),
            )

        # Guardar el análisis biométrico base
        analysis = persist_analysis(current_user, payload)

        # Integración con FitMaster AI: enviar resultados y guardar respuesta
        print(f"[DEBUG] Iniciando integración con FitMaster AI para análisis {analysis.id}")
        
        try:
            print(f"[DEBUG] Llamando a FitMasterService.analyze_bio_results()")
            print(f"[DEBUG] Payload: {payload.to_dict()}")
            
            fitmaster_result = FitMasterService.analyze_bio_results(payload.to_dict())
            
            print(f"[DEBUG] Resultado de FitMaster: {fitmaster_result}")
            
            if fitmaster_result:
                print(f"[DEBUG] Guardando resultados AI en la base de datos...")
                analysis.ai_interpretation = fitmaster_result.get("interpretation")
                analysis.nutrition_plan = fitmaster_result.get("nutrition_plan")
                analysis.training_plan = fitmaster_result.get("training_plan")
                
                db.session.commit()
                print(f"[DEBUG] Resultados AI guardados exitosamente")
            else:
                print(f"[DEBUG] FitMaster devolvió resultado vacío o None")
                
        except Exception as exc:
            # Log del error para debugging
            print(f"[FitMasterService] ERROR COMPLETO: {exc}")
            import traceback
            print(f"[FitMasterService] STACK TRACE: {traceback.format_exc()}")
            flash("El análisis se guardó, pero no se pudo conectar con FitMaster AI.", "warning")

        flash("Análisis guardado en tu historial.", "success")
        return redirect(url_for("bioanalyze.analysis_detail", analysis_id=analysis.id))

    # Si es GET, mostrar formulario vacío
    return render_template("bioanalyze/form.html", form_data={})


@bioanalyze_bp.route("/historial")
@login_required
def history():
    """List the authenticated user's previous biometric analyses."""
    
    analyses = (
        BiometricAnalysis.query
        .filter_by(user_id=current_user.id)
        .order_by(BiometricAnalysis.created_at.desc())
        .all()
    )

    return render_template("bioanalyze/history.html", analyses=analyses)


@bioanalyze_bp.route("/informe_web/<int:analysis_id>")
@login_required
def analysis_detail(analysis_id: int):
    """Display a stored analysis with its interpretations."""
    
    analysis = (
        BiometricAnalysis.query
        .filter_by(id=analysis_id, user_id=current_user.id)
        .first_or_404()
    )

    interpretaciones = build_interpretations_for_record(analysis)

    # Preparar datos de FitMaster AI para el template
    ai_data = {
        'interpretation': analysis.ai_interpretation,
        'nutrition_plan': analysis.nutrition_plan,
        'training_plan': analysis.training_plan
    }

    return render_template(
        "bioanalyze/detail.html",
        analysis=analysis,
        interpretaciones=interpretaciones,
        ai_data=ai_data,
    )


@bioanalyze_bp.route("/historial/<int:analysis_id>/eliminar", methods=["POST"])
@login_required
def delete_analysis(analysis_id: int):
    """Allow users to delete one of their previously stored analyses."""
    
    analysis = (
        BiometricAnalysis.query
        .filter_by(id=analysis_id, user_id=current_user.id)
        .first_or_404()
    )

    persist_id = analysis.id
    flash_message = f"Análisis #{persist_id} eliminado."

    db.session.delete(analysis)
    db.session.commit()

    flash(flash_message, "info")
    return redirect(url_for("bioanalyze.history"))


@bioanalyze_bp.route("/debug/<int:analysis_id>")
@login_required
def debug_analysis(analysis_id: int):
    """Debug: Ver respuesta completa de FitMaster AI."""
    
    try:
        analysis = BiometricAnalysis.query.filter_by(id=analysis_id, user_id=current_user.id).first()
        
        if not analysis:
            return f"<h1>Análisis #{analysis_id} no encontrado</h1><p>User ID: {current_user.id}</p>"
        
        # Crear contenido muy simple sin caracteres especiales
        ai_exists = "SI" if analysis.ai_interpretation else "NO"
        nutrition_exists = "SI" if analysis.nutrition_plan else "NO" 
        training_exists = "SI" if analysis.training_plan else "NO"
        
        ai_content = str(analysis.ai_interpretation)[:500] if analysis.ai_interpretation else "VACIO"
        nutrition_content = str(analysis.nutrition_plan)[:500] if analysis.nutrition_plan else "VACIO"
        training_content = str(analysis.training_plan)[:500] if analysis.training_plan else "VACIO"
        
        return f"""
        <html>
        <head><title>Debug Simple - Analisis {analysis.id}</title></head>
        <body>
            <h1>Debug FitMaster AI - Analisis #{analysis.id}</h1>
            
            <h2>Estado de Datos AI:</h2>
            <p>AI Interpretation: {ai_exists}</p>
            <p>Nutrition Plan: {nutrition_exists}</p>
            <p>Training Plan: {training_exists}</p>
            
            <h2>Interpretacion AI (primeros 500 chars):</h2>
            <textarea rows="10" cols="80">{ai_content}</textarea>
            
            <h2>Plan Nutricional (primeros 500 chars):</h2>
            <textarea rows="10" cols="80">{nutrition_content}</textarea>
            
            <h2>Plan Entrenamiento (primeros 500 chars):</h2>
            <textarea rows="10" cols="80">{training_content}</textarea>
            
            <p><a href="/informe_web/{analysis.id}">Volver al analisis</a></p>
            <p><a href="/informe_web">Crear nuevo analisis</a></p>
        </body>
        </html>
        """
        
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1><p>Analysis ID: {analysis_id}</p>"
