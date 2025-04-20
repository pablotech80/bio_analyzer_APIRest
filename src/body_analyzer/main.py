from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics


from src.body_analyzer.constantes import *
from src.body_analyzer.endpoints import configure_routes

app = Flask(__name__, template_folder="templates")
metrics = PrometheusMetrics(app)
configure_routes(app)

# Imprimir las rutas registradas
for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)

