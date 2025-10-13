from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from app.models.biometric_analysis import BiometricAnalysis
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
    users = query.order_by(User.last_name.asc(), User.first_name.asc()).all()
    return render_template("admin_users.html", users=users)


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
    return render_template("admin_user_analyses.html", user=user, analyses=analyses)
