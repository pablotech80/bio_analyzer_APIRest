# app/utils/decorators.py
from functools import wraps

from flask import abort, flash, redirect, url_for
from flask_login import current_user


def role_required(*roles):
    """
    Decorador para requerir roles específicos.

    Uso:
            @role_required('admin')
            @role_required('trainer', 'nutritionist')
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Debes iniciar sesión para acceder a esta página.", "warning")
                return redirect(url_for("auth.login"))

            if not current_user.role:
                flash("No tienes un rol asignado.", "danger")
                return redirect(url_for("index"))

            if current_user.role.name not in roles:
                flash("No tienes permisos para acceder a esta página.", "danger")
                abort(403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def permission_required(permission_name):
    """
    Decorador para requerir un permiso específico.

    Uso:
            @permission_required('write:training_plans')
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Debes iniciar sesión para acceder a esta página.", "warning")
                return redirect(url_for("auth.login"))

            if not current_user.has_permission(permission_name):
                flash("No tienes permisos para realizar esta acción.", "danger")
                abort(403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    """
    Decorador para requerir rol de administrador.

    Uso:
            @admin_required
    """
    return role_required("admin")(f)


def verified_email_required(f):
    """
    Decorador para requerir email verificado.

    Uso:
            @verified_email_required
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Debes iniciar sesión para acceder a esta página.", "warning")
            return redirect(url_for("auth.login"))

        if not current_user.is_verified:
            flash(
                "Debes verificar tu email para acceder a esta funcionalidad.", "warning"
            )
            return redirect(url_for("auth.profile"))

        return f(*args, **kwargs)

    return decorated_function
