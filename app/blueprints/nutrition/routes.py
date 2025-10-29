"""
Routes para planes nutricionales personalizados.

Funcionalidades:
- Ver mis planes de nutrición
- Crear nuevo plan personalizado
- Editar plan existente
- Ver detalles de un plan
"""
import logging
from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from . import nutrition_bp

logger = logging.getLogger(__name__)


@nutrition_bp.route('/mis-planes')
@login_required
def my_plans():
    """
    Muestra todos los planes nutricionales del usuario.
    
    Incluye planes manuales creados por el admin/entrenador.
    """
    from app.models.nutrition_plan import NutritionPlan
    
    # Obtener planes manuales activos del usuario
    manual_plans = NutritionPlan.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).order_by(
        NutritionPlan.created_at.desc()
    ).all()
    
    return render_template(
        'nutrition/my_plans.html',
        plans=manual_plans
    )


@nutrition_bp.route('/plan/<int:plan_id>')
@login_required
def view_plan(plan_id: int):
    """
    Muestra el detalle de un plan nutricional específico.
    
    Args:
        plan_id: ID del plan nutricional
    """
    from app.models.nutrition_plan import NutritionPlan
    
    plan = NutritionPlan.query.get_or_404(plan_id)
    
    # Verificar ownership
    if plan.user_id != current_user.id and not current_user.is_admin:
        flash("No tienes permiso para ver este plan.", "danger")
        return redirect(url_for('nutrition.my_plans'))
    
    return render_template(
        'nutrition/plan_detail_manual.html',
        plan=plan
    )


@nutrition_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def create_plan():
    """
    Crea un nuevo plan nutricional personalizado.
    
    Requiere datos biométricos actualizados.
    """
    if request.method == 'POST':
        # TODO: Implementar creación de plan personalizado
        flash("Funcionalidad en desarrollo. Por ahora, crea un análisis biométrico para obtener un plan.", "info")
        return redirect(url_for('bioanalyze.new_analysis'))
    
    return render_template('nutrition/create_plan.html')
