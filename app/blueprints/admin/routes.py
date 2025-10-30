from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
import json
from datetime import datetime

from app import db
from app.models.biometric_analysis import BiometricAnalysis
from app.models.nutrition_plan import NutritionPlan
from app.models.training_plan import TrainingPlan
from app.models.user import User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/users")
@login_required
def users():
    if not current_user.is_admin:
        return render_template("errors/403.html"), 403
    gender = request.args.get("gender")
    last_name = request.args.get("last_name")
    query = User.query
    if gender:
        query = query.filter_by(gender=gender)
    if last_name:
        query = query.filter(User.last_name.ilike(f"%{last_name}%"))
    users_list = query.order_by(User.last_name.asc(), User.first_name.asc()).all()
    
    # Calcular estadísticas para cada usuario
    users_data = []
    for user in users_list:
        # Contar análisis totales
        total_analyses = BiometricAnalysis.query.filter_by(user_id=user.id).count()
        
        # Obtener IDs de análisis con planes
        nutrition_analysis_ids = set(
            plan.analysis_id for plan in 
            NutritionPlan.query.filter_by(user_id=user.id).filter(
                NutritionPlan.analysis_id.isnot(None)
            ).all()
        )
        training_analysis_ids = set(
            plan.analysis_id for plan in 
            TrainingPlan.query.filter_by(user_id=user.id).filter(
                TrainingPlan.analysis_id.isnot(None)
            ).all()
        )
        
        # Contar análisis sin ningún plan
        analyses_without_plans = 0
        if total_analyses > 0:
            all_analyses = BiometricAnalysis.query.filter_by(user_id=user.id).all()
            for analysis in all_analyses:
                if analysis.id not in nutrition_analysis_ids and analysis.id not in training_analysis_ids:
                    analyses_without_plans += 1
        
        # Contar planes totales
        total_nutrition_plans = NutritionPlan.query.filter_by(user_id=user.id).count()
        total_training_plans = TrainingPlan.query.filter_by(user_id=user.id).count()
        
        users_data.append({
            'user': user,
            'total_analyses': total_analyses,
            'analyses_without_plans': analyses_without_plans,
            'total_nutrition_plans': total_nutrition_plans,
            'total_training_plans': total_training_plans,
            'needs_attention': analyses_without_plans > 0
        })
    
    return render_template("admin_users.html", users_data=users_data)


@admin_bp.route("/users/<int:user_id>/analyses")
@login_required
def user_analyses(user_id):
    if not current_user.is_admin:
        return render_template("errors/403.html"), 403
    user = User.query.get_or_404(user_id)
    analyses = (
        BiometricAnalysis.query.filter_by(user_id=user.id)
        .order_by(BiometricAnalysis.created_at.desc())
        .all()
    )
    
    # Obtener planes del usuario
    nutrition_plans = NutritionPlan.query.filter_by(user_id=user.id).order_by(NutritionPlan.created_at.desc()).all()
    training_plans = TrainingPlan.query.filter_by(user_id=user.id).order_by(TrainingPlan.created_at.desc()).all()
    
    return render_template(
        "admin_user_analyses.html", 
        user=user, 
        analyses=analyses,
        nutrition_plans=nutrition_plans,
        training_plans=training_plans
    )


@admin_bp.route("/users/<int:user_id>/nutrition/create", methods=["GET", "POST"])
@login_required
def create_nutrition_plan(user_id):
    """Crear plan nutricional para un usuario"""
    if not current_user.is_admin:
        return render_template("errors/403.html"), 403
    
    user = User.query.get_or_404(user_id)
    
    if request.method == "POST":
        try:
            # Obtener meals como texto Markdown
            meals_text = request.form.get("meals_text", "").strip() or None
            
            # Crear plan
            plan = NutritionPlan(
                user_id=user.id,
                created_by=current_user.id,
                title=request.form.get("title"),
                description=request.form.get("description"),
                goal=request.form.get("goal"),
                daily_calories=int(request.form.get("daily_calories")) if request.form.get("daily_calories") else None,
                protein_grams=int(request.form.get("protein_grams")) if request.form.get("protein_grams") else None,
                carbs_grams=int(request.form.get("carbs_grams")) if request.form.get("carbs_grams") else None,
                fats_grams=int(request.form.get("fats_grams")) if request.form.get("fats_grams") else None,
                meals=meals_text,
                supplements=request.form.get("supplements"),
                notes=request.form.get("notes"),
                start_date=datetime.strptime(request.form.get("start_date"), "%Y-%m-%d").date() if request.form.get("start_date") else None,
                end_date=datetime.strptime(request.form.get("end_date"), "%Y-%m-%d").date() if request.form.get("end_date") else None,
                analysis_id=int(request.form.get("analysis_id")) if request.form.get("analysis_id") else None,
                is_active=True
            )
            
            db.session.add(plan)
            db.session.commit()
            
            # Redirigir directamente al plan creado para verificar
            return redirect(url_for("nutrition.view_plan", plan_id=plan.id))
            
        except Exception as e:
            flash(f"❌ Error al crear plan: {str(e)}", "danger")
            db.session.rollback()
    
    # GET: Mostrar formulario
    analyses = BiometricAnalysis.query.filter_by(user_id=user.id).order_by(BiometricAnalysis.created_at.desc()).all()
    return render_template("admin_create_nutrition.html", user=user, analyses=analyses)


@admin_bp.route("/users/<int:user_id>/training/create", methods=["GET", "POST"])
@login_required
def create_training_plan(user_id):
    """Crear plan de entrenamiento para un usuario"""
    if not current_user.is_admin:
        return render_template("errors/403.html"), 403
    
    user = User.query.get_or_404(user_id)
    
    if request.method == "POST":
        try:
            # Obtener workouts como texto Markdown
            workouts_text = request.form.get("workouts_text", "").strip() or None
            
            # Crear plan
            plan = TrainingPlan(
                user_id=user.id,
                created_by=current_user.id,
                title=request.form.get("title"),
                description=request.form.get("description"),
                goal=request.form.get("goal"),
                frequency=request.form.get("frequency"),
                routine_type=request.form.get("routine_type"),
                duration_weeks=int(request.form.get("duration_weeks")) if request.form.get("duration_weeks") else None,
                workouts=workouts_text,
                warm_up=request.form.get("warm_up"),
                cool_down=request.form.get("cool_down"),
                notes=request.form.get("notes"),
                start_date=datetime.strptime(request.form.get("start_date"), "%Y-%m-%d").date() if request.form.get("start_date") else None,
                end_date=datetime.strptime(request.form.get("end_date"), "%Y-%m-%d").date() if request.form.get("end_date") else None,
                analysis_id=int(request.form.get("analysis_id")) if request.form.get("analysis_id") else None,
                is_active=True
            )
            
            db.session.add(plan)
            db.session.commit()
            
            # Redirigir directamente al plan creado para verificar
            return redirect(url_for("training.view_plan", plan_id=plan.id))
            
        except Exception as e:
            flash(f"❌ Error al crear plan: {str(e)}", "danger")
            db.session.rollback()
    
    # GET: Mostrar formulario
    analyses = BiometricAnalysis.query.filter_by(user_id=user.id).order_by(BiometricAnalysis.created_at.desc()).all()
    return render_template("admin_create_training.html", user=user, analyses=analyses)


@admin_bp.route("/nutrition/<int:plan_id>/edit", methods=["GET", "POST"])
@login_required
def edit_nutrition_plan(plan_id):
    """Editar plan nutricional existente"""
    if not current_user.is_admin:
        return render_template("errors/403.html"), 403
    
    plan = NutritionPlan.query.get_or_404(plan_id)
    user = User.query.get_or_404(plan.user_id)
    
    if request.method == "POST":
        try:
            # Obtener meals como texto Markdown
            meals_text = request.form.get("meals_text", "").strip() or None
            plan.meals = meals_text
            
            # Actualizar campos
            plan.title = request.form.get("title")
            plan.description = request.form.get("description")
            plan.goal = request.form.get("goal")
            plan.daily_calories = int(request.form.get("daily_calories")) if request.form.get("daily_calories") else None
            plan.protein_grams = int(request.form.get("protein_grams")) if request.form.get("protein_grams") else None
            plan.carbs_grams = int(request.form.get("carbs_grams")) if request.form.get("carbs_grams") else None
            plan.fats_grams = int(request.form.get("fats_grams")) if request.form.get("fats_grams") else None
            plan.supplements = request.form.get("supplements")
            plan.notes = request.form.get("notes")
            plan.start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d").date() if request.form.get("start_date") else None
            plan.end_date = datetime.strptime(request.form.get("end_date"), "%Y-%m-%d").date() if request.form.get("end_date") else None
            plan.analysis_id = int(request.form.get("analysis_id")) if request.form.get("analysis_id") else None
            plan.is_active = request.form.get("is_active") == "on"
            
            db.session.commit()
            flash("✅ Plan nutricional actualizado correctamente", "success")
            return redirect(url_for("nutrition.view_plan", plan_id=plan.id))
            
        except Exception as e:
            flash(f"❌ Error al actualizar plan: {str(e)}", "danger")
            db.session.rollback()
    
    # GET: Mostrar formulario con datos actuales
    analyses = BiometricAnalysis.query.filter_by(user_id=user.id).order_by(BiometricAnalysis.created_at.desc()).all()
    
    return render_template("admin_edit_nutrition.html", user=user, plan=plan, analyses=analyses)


@admin_bp.route("/training/<int:plan_id>/edit", methods=["GET", "POST"])
@login_required
def edit_training_plan(plan_id):
    """Editar plan de entrenamiento existente"""
    if not current_user.is_admin:
        return render_template("errors/403.html"), 403
    
    plan = TrainingPlan.query.get_or_404(plan_id)
    user = User.query.get_or_404(plan.user_id)
    
    if request.method == "POST":
        try:
            # Obtener workouts como texto Markdown
            workouts_text = request.form.get("workouts_text", "").strip() or None
            plan.workouts = workouts_text
            
            # Actualizar campos
            plan.title = request.form.get("title")
            plan.description = request.form.get("description")
            plan.goal = request.form.get("goal")
            plan.frequency = request.form.get("frequency")
            plan.routine_type = request.form.get("routine_type")
            plan.duration_weeks = int(request.form.get("duration_weeks")) if request.form.get("duration_weeks") else None
            plan.warm_up = request.form.get("warm_up")
            plan.cool_down = request.form.get("cool_down")
            plan.notes = request.form.get("notes")
            plan.start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d").date() if request.form.get("start_date") else None
            plan.end_date = datetime.strptime(request.form.get("end_date"), "%Y-%m-%d").date() if request.form.get("end_date") else None
            plan.analysis_id = int(request.form.get("analysis_id")) if request.form.get("analysis_id") else None
            plan.is_active = request.form.get("is_active") == "on"
            
            db.session.commit()
            flash("✅ Plan de entrenamiento actualizado correctamente", "success")
            return redirect(url_for("training.view_plan", plan_id=plan.id))
            
        except Exception as e:
            flash(f"❌ Error al actualizar plan: {str(e)}", "danger")
            db.session.rollback()
    
    # GET: Mostrar formulario con datos actuales
    analyses = BiometricAnalysis.query.filter_by(user_id=user.id).order_by(BiometricAnalysis.created_at.desc()).all()
    
    return render_template("admin_edit_training.html", user=user, plan=plan, analyses=analyses)


@admin_bp.route("/nutrition/<int:plan_id>/delete", methods=["POST"])
@login_required
def delete_nutrition_plan(plan_id):
    """Eliminar plan nutricional"""
    if not current_user.is_admin:
        return render_template("errors/403.html"), 403
    
    plan = NutritionPlan.query.get_or_404(plan_id)
    user_id = plan.user_id
    
    try:
        db.session.delete(plan)
        db.session.commit()
        flash("✅ Plan nutricional eliminado correctamente", "success")
    except Exception as e:
        flash(f"❌ Error al eliminar plan: {str(e)}", "danger")
        db.session.rollback()
    
    return redirect(url_for("admin.user_analyses", user_id=user_id))


@admin_bp.route("/training/<int:plan_id>/delete", methods=["POST"])
@login_required
def delete_training_plan(plan_id):
    """Eliminar plan de entrenamiento"""
    if not current_user.is_admin:
        return render_template("errors/403.html"), 403
    
    plan = TrainingPlan.query.get_or_404(plan_id)
    user_id = plan.user_id
    
    try:
        db.session.delete(plan)
        db.session.commit()
        flash("✅ Plan de entrenamiento eliminado correctamente", "success")
    except Exception as e:
        flash(f"❌ Error al eliminar plan: {str(e)}", "danger")
        db.session.rollback()
    
    return redirect(url_for("admin.user_analyses", user_id=user_id))
