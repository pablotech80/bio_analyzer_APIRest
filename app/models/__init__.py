# app/models/__init__.py
from app.models.user import User, Role, Permission
from app.models.biometric_analysis import BiometricAnalysis
from app.models.contact_message import ContactMessage

__all__ = ['User', 'Role', 'Permission', 'BiometricAnalysis', 'ContactMessage']
