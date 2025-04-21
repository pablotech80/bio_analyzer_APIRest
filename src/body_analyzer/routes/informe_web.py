from flask import Blueprint, request, render_template
from src.body_analyzer.model import Sexo
from src.body_analyzer.utils import convertir_genero, convertir_objetivo
from src.body_analyzer.calculos import (
    calcular_porcentaje_grasa, calcular_tmb, calcular_imc,
    calcular_agua_total, calcular_ffmi, calcular_peso_saludable,
    calcular_sobrepeso, calcular_rcc, calcular_ratio_cintura_altura,
    calcular_calorias_diarias, calcular_macronutrientes
)
from src.body_analyzer.interpretaciones import (
    interpretar_imc, interpretar_porcentaje_grasa, interpretar_ffmi,
    interpretar_rcc, interpretar_ratio_cintura_altura
)

informe_web_bp = Blueprint("informe_web", __name__, template_folder="../../templates")

# Función auxiliar para aceptar coma o punto como separador decimal
def parse_decimal(value):
    return float(value.replace(",", "."))

@informe_web_bp.route("/informe_web", methods=["GET", "POST"])
def informe_web():
    if request.method == "POST":
        try:
            data = request.form

            # Captura de datos desde el formulario
            peso_str = data.get("peso", "").strip()
            altura_str = data.get("altura", "").strip()
            edad_str = data.get("edad", "").strip()
            cuello_str = data.get("cuello", "").strip()
            cintura_str = data.get("cintura", "").strip()
            cadera_str = data.get("cadera", "").strip()
            genero_str = data.get("genero", "").strip().lower()
            objetivo_str = data.get("objetivo", "").strip().lower()

            # Validación de campos obligatorios
            if not all([peso_str, altura_str, edad_str, cuello_str, cintura_str, genero_str, objetivo_str]):
                raise ValueError("Por favor complete todos los campos obligatorios.")

            # Conversión segura
            peso = parse_decimal(peso_str)
            altura = parse_decimal(altura_str)
            edad = int(edad_str)
            cuello = parse_decimal(cuello_str)
            cintura = parse_decimal(cintura_str)
            cadera = parse_decimal(cadera_str) if cadera_str else 0.0
            genero = convertir_genero(genero_str)
            objetivo = convertir_objetivo(objetivo_str)

            # Cálculos biométricos
            porcentaje_grasa = calcular_porcentaje_grasa(cintura, cuello, altura, genero, cadera)
            tmb = calcular_tmb(peso, altura, edad, genero)
            imc = calcular_imc(peso, altura)
            masa_muscular = peso - (peso * (porcentaje_grasa / 100))
            agua_total = calcular_agua_total(peso, altura, edad, genero)
            ffmi = calcular_ffmi(masa_muscular, altura)
            peso_saludable_min, peso_saludable_max = calcular_peso_saludable(altura)
            sobrepeso = calcular_sobrepeso(peso, altura)
            rcc = calcular_rcc(cintura, cadera) if genero == Sexo.MUJER else "N/A"
            ratio_cintura_altura = calcular_ratio_cintura_altura(cintura, altura)
            calorias_diarias = calcular_calorias_diarias(tmb, objetivo)
            proteinas, carbohidratos, grasas = calcular_macronutrientes(calorias_diarias, objetivo)

            # Interpretaciones
            interpretaciones = {
                "imc": interpretar_imc(imc, ffmi, genero),
                "porcentaje_grasa": interpretar_porcentaje_grasa(porcentaje_grasa, genero),
                "ffmi": interpretar_ffmi(ffmi, genero),
                "rcc": interpretar_rcc(rcc, genero) if genero == Sexo.MUJER else "N/A",
                "ratio_cintura_altura": interpretar_ratio_cintura_altura(ratio_cintura_altura),
            }

            # Resultados para renderizar
            resultados = {
                "tmb": round(tmb, 2),
                "imc": round(imc, 2),
                "porcentaje_grasa": round(porcentaje_grasa, 2),
                "masa_muscular": round(masa_muscular, 2),
                "agua_total": round(agua_total, 2),
                "ffmi": round(ffmi, 2),
                "peso_saludable": {
                    "min": round(peso_saludable_min, 2),
                    "max": round(peso_saludable_max, 2),
                },
                "sobrepeso": round(sobrepeso, 2),
                "rcc": rcc,
                "ratio_cintura_altura": round(ratio_cintura_altura, 2),
                "calorias_diarias": round(calorias_diarias, 2),
                "macronutrientes": {
                    "proteinas": round(proteinas, 2),
                    "carbohidratos": round(carbohidratos, 2),
                    "grasas": round(grasas, 2),
                },
            }

            return render_template("formulario.html", resultados=resultados, interpretaciones=interpretaciones)

        except Exception as e:
            return render_template("formulario.html", error=f"Error al procesar los datos: {e}"), 400

    return render_template("formulario.html")
