# app/models/__init__.py
from app.models.user import User, Role, Permission

__all__ = ['User', 'Role', 'Permission']