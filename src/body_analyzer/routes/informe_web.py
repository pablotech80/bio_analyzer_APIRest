from flask import Blueprint, request, render_template, session


from src.body_analyzer.model import Sexo
from src.body_analyzer.utils import convertir_genero, convertir_objetivo
from src.body_analyzer.calculos import (
    calcular_porcentaje_grasa, calcular_tmb, calcular_imc,
    calcular_agua_total, calcular_ffmi, calcular_peso_saludable,
    calcular_sobrepeso, calcular_rcc, calcular_ratio_cintura_altura,
    calcular_calorias_diarias, calcular_macronutrientes, calcular_macronutrientes_porcentajes,
    calcular_edad_metabolica_avanzada
    )

from src.body_analyzer.interpretaciones import (
    interpretar_imc, interpretar_porcentaje_grasa, interpretar_ffmi,
    interpretar_rcc, interpretar_ratio_cintura_altura,
    interpretar_edad_metabolica_avanzada,
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

            # Captura de datos
            peso_str = data.get("peso", "").strip()
            altura_str = data.get("altura", "").strip()
            edad_str = data.get("edad", "").strip()
            cuello_str = data.get("cuello", "").strip()
            cintura_str = data.get("cintura", "").strip()
            cadera_str = data.get("cadera", "").strip()
            genero_str = data.get("genero", "").strip().lower()
            objetivo_str = data.get("objetivo", "").strip().lower()
            nivel = data.get("nivel", "").strip().lower()

            # Captura de factor de actividad
            factor_actividad_str = data.get("factor_actividad", "").strip()
            if not factor_actividad_str:
                raise ValueError("Por favor seleccione su nivel de actividad física.")
            factor_actividad = float(factor_actividad_str)

            # Validación de campos obligatorios
            if not all([peso_str, altura_str, edad_str, cuello_str, cintura_str, genero_str]):
                raise ValueError("Por favor complete todos los campos obligatorios.")

            # Conversión segura
            peso = parse_decimal(peso_str)
            altura = parse_decimal(altura_str)
            edad = int(edad_str)
            cuello = parse_decimal(cuello_str)
            cintura = parse_decimal(cintura_str)
            cadera = parse_decimal(cadera_str) if cadera_str else 0.0
            genero = convertir_genero(genero_str)

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

            # Cálculo edad metabólica avanzada
            edad_metabolica = calcular_edad_metabolica_avanzada(
                tmb, genero, edad, imc, porcentaje_grasa, ratio_cintura_altura
            )
            interpretacion_edad_metabolica = interpretar_edad_metabolica_avanzada(
                edad, edad_metabolica, imc, porcentaje_grasa, ratio_cintura_altura, genero
            )

            # Calorías de mantenimiento
            tdee = tmb * factor_actividad
            calorias_diarias = tdee

            # Inicialización de macros
            proteinas = carbohidratos = grasas = None

            # SOLO si el usuario eligió objetivo y nivel, calculamos macros
            if objetivo_str and nivel:
                objetivo = convertir_objetivo(objetivo_str)
                calorias_diarias = calcular_calorias_diarias(tmb, objetivo, factor_actividad)

                if nivel == "saludable":
                    distribucion = {
                        "mantener peso": {"proteinas": 25, "carbohidratos": 50, "grasas": 25},
                        "perder grasa": {"proteinas": 35, "carbohidratos": 30, "grasas": 35},
                        "ganar masa muscular": {"proteinas": 30, "carbohidratos": 55, "grasas": 15},
                    }
                elif nivel == "fitness":
                    distribucion = {
                        "mantener peso": {"proteinas": 30, "carbohidratos": 45, "grasas": 25},
                        "perder grasa": {"proteinas": 40, "carbohidratos": 20, "grasas": 40},
                        "ganar masa muscular": {"proteinas": 30, "carbohidratos": 50, "grasas": 20},
                    }
                elif nivel == "competicion":
                    distribucion = None
                else:
                    raise ValueError("Nivel de ajuste de macronutrientes no válido.")

                if distribucion:
                    macros = distribucion.get(objetivo_str)
                    if macros:
                        porcentaje_proteinas = macros["proteinas"]
                        porcentaje_carbohidratos = macros["carbohidratos"]
                        porcentaje_grasas = macros["grasas"]

                        proteinas, carbohidratos, grasas = calcular_macronutrientes_porcentajes(
                            calorias_diarias,
                            porcentaje_proteinas,
                            porcentaje_carbohidratos,
                            porcentaje_grasas
                        )
                else:
                    # Competición: gramos/kg
                    proteinas_kg = float(data.get("proteinas_kg", 0) or 0)
                    carbohidratos_kg = float(data.get("carbohidratos_kg", 0) or 0)
                    grasas_kg = float(data.get("grasas_kg", 0) or 0)

                    if proteinas_kg and carbohidratos_kg and grasas_kg:
                        proteinas = peso * proteinas_kg
                        carbohidratos = peso * carbohidratos_kg
                        grasas = peso * grasas_kg
                        calorias_diarias = (proteinas * 4) + (carbohidratos * 4) + (grasas * 9)

            # Resultados
            resultados = {
                "tmb": round(tmb, 2),
                "tdee": round(tdee, 2),
                "edad_metabolica": edad_metabolica,
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
                    "proteinas": round(proteinas, 2) if proteinas else None,
                    "carbohidratos": round(carbohidratos, 2) if carbohidratos else None,
                    "grasas": round(grasas, 2) if grasas else None,
                },
            }

            # Interpretaciones
            interpretaciones = {
                "imc": interpretar_imc(imc, ffmi, genero),
                "porcentaje_grasa": interpretar_porcentaje_grasa(porcentaje_grasa, genero),
                "ffmi": interpretar_ffmi(ffmi, genero),
                "rcc": interpretar_rcc(rcc, genero) if genero == Sexo.MUJER else "N/A",
                "ratio_cintura_altura": interpretar_ratio_cintura_altura(ratio_cintura_altura),
                "edad_metabolica": interpretacion_edad_metabolica,
            }

            form_data = data.to_dict()
            session["form_data"] = form_data
            return render_template("resultados.html", resultados=resultados, interpretaciones=interpretaciones, form_data=form_data)

        except Exception as e:
            return render_template("formulario.html", error=str(e), form_data=request.form), 400

    form_data = session.pop('form_data', {})
    return render_template("formulario.html", form_data=form_data)

