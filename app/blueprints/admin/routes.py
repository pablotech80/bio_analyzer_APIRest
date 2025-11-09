from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
import json
from datetime import datetime

from app import db
from app.models.biometric_analysis import BiometricAnalysis
from app.models.nutrition_plan import NutritionPlan
from app.models.training_plan import TrainingPlan
from app.models.user import User
from app.models.notification import Notification

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
        
        # Contar planes totales
        total_nutrition_plans = NutritionPlan.query.filter_by(user_id=user.id).count()
        total_training_plans = TrainingPlan.query.filter_by(user_id=user.id).count()
        
        # Contar planes activos
        active_nutrition_plans = NutritionPlan.query.filter_by(user_id=user.id, is_active=True).count()
        active_training_plans = TrainingPlan.query.filter_by(user_id=user.id, is_active=True).count()
        
        # Obtener IDs de análisis con planes vinculados
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
        
        # Contar análisis sin ningún plan vinculado
        analyses_without_plans = 0
        if total_analyses > 0:
            all_analyses = BiometricAnalysis.query.filter_by(user_id=user.id).all()
            for analysis in all_analyses:
                if analysis.id not in nutrition_analysis_ids and analysis.id not in training_analysis_ids:
                    analyses_without_plans += 1
        
        # Determinar si requiere atención:
        # - Si tiene análisis pero NO tiene planes activos de nutrición Y entrenamiento
        # - O si tiene análisis sin planes vinculados
        needs_attention = False
        if total_analyses > 0:
            # Si no tiene ambos planes activos, requiere atención
            if active_nutrition_plans == 0 or active_training_plans == 0:
                needs_attention = True
        
        users_data.append({
            'user': user,
            'total_analyses': total_analyses,
            'analyses_without_plans': analyses_without_plans,
            'total_nutrition_plans': total_nutrition_plans,
            'total_training_plans': total_training_plans,
            'active_nutrition_plans': active_nutrition_plans,
            'active_training_plans': active_training_plans,
            'needs_attention': needs_attention
        })
    
    return render_template(
        "admin_users.html", 
        users_data=users_data,
        current_gender=gender,
        current_last_name=last_name
    )


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
            
            # Manejo seguro de fechas vacías
            start_date_str = request.form.get("start_date", "").strip()
            end_date_str = request.form.get("end_date", "").strip()
            
            try:
                plan.start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
            except (ValueError, TypeError):
                plan.start_date = None
                
            try:
                plan.end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None
            except (ValueError, TypeError):
                plan.end_date = None
                
            plan.analysis_id = int(request.form.get("analysis_id")) if request.form.get("analysis_id") else None
            plan.is_active = request.form.get("is_active") == "on"
            
            db.session.commit()
            flash("✅ Plan nutricional actualizado correctamente", "success")
            return redirect(url_for("nutrition.view_plan", plan_id=plan.id))
            
        except Exception as e:
            flash(f"❌ Error al actualizar plan: {str(e)}", "danger")
            db.session.rollback()
    
    # GET: Mostrar formulario con datos actuales
    try:
        analyses = BiometricAnalysis.query.filter_by(user_id=user.id).order_by(BiometricAnalysis.created_at.desc()).all()
        return render_template("admin_edit_nutrition.html", user=user, plan=plan, analyses=analyses)
    except Exception as e:
        flash(f"❌ Error al cargar el formulario de edición: {str(e)}", "danger")
        return redirect(url_for("admin.user_analyses", user_id=user.id))


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


@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    """Eliminar usuario y todos sus datos relacionados"""
    if not current_user.is_admin:
        return render_template("errors/403.html"), 403
    
    # No permitir eliminar al propio admin
    if user_id == current_user.id:
        flash("❌ No puedes eliminar tu propia cuenta de administrador", "danger")
        return redirect(url_for("admin.users"))
    
    user = User.query.get_or_404(user_id)
    user_name = f"{user.first_name} {user.last_name}"
    
    try:
        # Eliminar notificaciones (si la tabla existe)
        try:
            Notification.query.filter_by(user_id=user.id).delete()
        except Exception:
            pass  # Tabla notifications aún no existe
        
        # Eliminar mensajes de contacto (si existen)
        try:
            from app.models.contact_message import ContactMessage
            ContactMessage.query.filter_by(user_id=user.id).delete()
        except Exception:
            pass  # Tabla contact_messages no existe
        
        # Eliminar en cascada: análisis, planes
        BiometricAnalysis.query.filter_by(user_id=user.id).delete()
        NutritionPlan.query.filter_by(user_id=user.id).delete()
        TrainingPlan.query.filter_by(user_id=user.id).delete()
        
        # Eliminar usuario
        db.session.delete(user)
        db.session.commit()
        
        flash(f"✅ Usuario {user_name} y todos sus datos han sido eliminados correctamente", "success")
    except Exception as e:
        flash(f"❌ Error al eliminar usuario: {str(e)}", "danger")
        db.session.rollback()
    
    return redirect(url_for("admin.users"))


@admin_bp.route("/users/<int:user_id>/notify-plans", methods=["POST"])
@login_required
def notify_user_plans(user_id):
    """Enviar notificación al usuario de que sus planes están disponibles"""
    if not current_user.is_admin:
        return render_template("errors/403.html"), 403
    
    user = User.query.get_or_404(user_id)
    
    # Obtener planes activos
    nutrition_plans = NutritionPlan.query.filter_by(user_id=user.id, is_active=True).all()
    training_plans = TrainingPlan.query.filter_by(user_id=user.id, is_active=True).all()
    
    if len(nutrition_plans) == 0 and len(training_plans) == 0:
        flash("⚠️ Este usuario no tiene planes activos para notificar", "warning")
        return redirect(url_for("admin.user_analyses", user_id=user_id))
    
    try:
        # Crear notificación en la base de datos (si la tabla existe)
        message_parts = []
        if len(nutrition_plans) > 0:
            message_parts.append(f"✅ {len(nutrition_plans)} plan(es) de nutrición")
        if len(training_plans) > 0:
            message_parts.append(f"✅ {len(training_plans)} plan(es) de entrenamiento")
        
        try:
            notification = Notification(
                user_id=user.id,
                title="🎉 ¡Tus planes están listos!",
                message=f"Hola {user.first_name},\n\nTu entrenador ha preparado tus planes personalizados:\n\n" + "\n".join(message_parts) + "\n\nPuedes verlos en tu dashboard.",
                notification_type="success",
                nutrition_plan_id=nutrition_plans[0].id if nutrition_plans else None,
                training_plan_id=training_plans[0].id if training_plans else None
            )
            
            db.session.add(notification)
            db.session.commit()
            
            # Enviar email al usuario
            from app.services.email_service import send_plans_ready_email
            import logging
            logger = logging.getLogger(__name__)
            
            logger.info(f"🔔 Intentando enviar email a {user.email}")
            email_sent = send_plans_ready_email(user, len(nutrition_plans), len(training_plans))
            logger.info(f"📧 Resultado del envío: {email_sent}")
            
            if email_sent:
                flash(f"✅ Notificación creada y email enviado a {user.email} sobre sus {len(nutrition_plans)} plan(es) de nutrición y {len(training_plans)} plan(es) de entrenamiento", "success")
            else:
                flash(f"⚠️ Notificación creada para {user.email} pero el email NO se envió (revisa logs de Railway)", "warning")
        except Exception as db_error:
            # Si falla (tabla no existe), solo mostrar mensaje sin guardar en BD
            db.session.rollback()
            flash(f"⚠️ Planes listos para {user.email}: {', '.join(message_parts)}. (Notificación en BD pendiente de migración)", "warning")
        
    except Exception as e:
        flash(f"❌ Error al procesar notificación: {str(e)}", "danger")
        db.session.rollback()
    
    return redirect(url_for("admin.user_analyses", user_id=user_id))
