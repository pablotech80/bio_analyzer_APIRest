from .metrics import metrics_bp
from .nutricion import nutricion_bp
from .informe import informe_bp
from .interpretaciones import interpretaciones_bp

# Lista central de todos los blueprints
all_blueprints = [
    metrics_bp,
    nutricion_bp,
    informe_bp,
    interpretaciones_bp,
]

