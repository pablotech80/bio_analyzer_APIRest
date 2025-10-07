# constantes_enum.py
# Provee una clase base Enum compatible con los usos en constantes.py

try:
    from enum import Enum
except ImportError:
    # Fallback mínimo si enum no está disponible (Python <3.4)
    class Enum(object):
        pass
