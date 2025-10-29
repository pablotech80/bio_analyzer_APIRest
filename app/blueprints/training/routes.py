"""
Routes para planes de entrenamiento personalizados.

Funcionalidades:
- Ver mis planes de entrenamiento
- Crear nuevo plan personalizado
- Editar plan existente
- Ver detalles de un plan
- Registrar progreso
"""
import logging
from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from . import training_bp

logger = logging.getLogger(__name__)


@training_bp.route('/mis-planes')
@login_required
def my_plans():
    """
    Muestra todos los planes de entrenamiento del usuario.
    
    Incluye planes manuales creados por el admin/entrenador.
    """
    from app.models.training_plan import TrainingPlan
    
    # Obtener planes manuales activos del usuario
    manual_plans = TrainingPlan.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).order_by(
        TrainingPlan.created_at.desc()
    ).all()
    
    return render_template(
        'training/my_plans.html',
        plans=manual_plans
    )


@training_bp.route('/plan/<int:plan_id>')
@login_required
def view_plan(plan_id: int):
    """
    Muestra el detalle de un plan de entrenamiento específico.
    
    Args:
        plan_id: ID del plan de entrenamiento
    """
    from app.models.training_plan import TrainingPlan
    
    plan = TrainingPlan.query.get_or_404(plan_id)
    
    # Verificar ownership
    if plan.user_id != current_user.id and not current_user.is_admin:
        flash("No tienes permiso para ver este plan.", "danger")
        return redirect(url_for('training.my_plans'))
    
    return render_template(
        'training/plan_detail.html',
        plan=plan
    )


@training_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def create_plan():
    """
    Crea un nuevo plan de entrenamiento personalizado.
    
    Requiere datos biométricos actualizados.
    """
    if request.method == 'POST':
        # TODO: Implementar creación de plan personalizado
        flash("Funcionalidad en desarrollo. Por ahora, crea un análisis biométrico para obtener un plan.", "info")
        return redirect(url_for('bioanalyze.new_analysis'))
    
    return render_template('training/create_plan.html')
