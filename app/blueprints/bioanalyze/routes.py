"""Routes for biometric analysis capture, history and detail views."""
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

        analysis = persist_analysis(current_user, payload)
        flash("Análisis guardado en tu historial.", "success")
        return redirect(url_for("bioanalyze.analysis_detail", analysis_id=analysis.id))

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

    return render_template(
        "bioanalyze/detail.html",
        analysis=analysis,
        interpretaciones=interpretaciones,
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

    from app import db

    db.session.delete(analysis)
    db.session.commit()

    flash(flash_message, "info")
    return redirect(url_for("bioanalyze.history"))
