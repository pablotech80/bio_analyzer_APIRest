import os
from flask import json, jsonify, request, Response, render_template
from src.body_analyzer.interpretaciones import *
from src.body_analyzer.model import Sexo
from .analisis_completo import validar_parametro
from .calculos import *
from .constantes import *

# Calcula la ruta absoluta de /templates en la raíz de tu proyecto
basedir = os.path.abspath(os.path.dirname(__file__))
# Sube dos niveles: src/body_analyzer → src → proyecto
templates_dir = os.path.join(basedir, '..', '..', 'templates')

# Función para encapsular el cálculo de genero en los endpoints.
def convertir_genero(genero_str):
    if genero_str == "h":
        return Sexo.HOMBRE
    elif genero_str == "h":
        return Sexo.MUJER
    else:
        raise ValueError("Género no válido. Usa 'h' para hombre o 'm' para mujer.")

def convertir_objetivo(objetivo_str):
    try:
        return ObjetivoNutricional(objetivo_str.strip().lower())
    except ValueError:
        raise ValueError("El objetivo debe ser 'mantener peso', 'perder grasa' o 'ganar masa muscular'.")


def configure_app(app):
    app.config["JSON_SORT_KEYS"] = False
    app.config["DEBUG"] = True
    @app.route("/")
    def index():
        return "Welcome to the BIO*ANALYZE API!"

    @app.route("/calcular_porcentaje_grasa", methods=["POST"])
    def calcular_porcentaje_grasa_endpoint():
        try:
            data = request.get_json()
            cintura = data.get("cintura")
            cuello = data.get("cuello")
            altura = data.get("altura")
            genero = data.get("genero", "").strip().lower()
            cadera = data.get("cadera")

            # Verificar los parámetros requeridos para hombres y mujeres
            if None in (cintura, cuello, altura, genero):
                return jsonify({"error": "Faltan parámetros obligatorios"}), 400

            # Verificar que el género sea válido
            if genero not in ["h", "m"]:
                return (
                    jsonify({"error": "El valor de 'genero' debe ser 'h' o 'm'."}),
                    400,
                )

            # Verificar el valor de cadera si el género es mujer
            if genero == "m" and cadera is None:
                return (
                    jsonify(
                        {"error": "Para mujeres, la cadera debe ser especificada."}
                    ),
                    400,
                )

            # Convertir genero a Enum Sexo
            genero_enum = Sexo.HOMBRE if genero == "h" else Sexo.MUJER

            # Calcular el porcentaje de grasa
            porcentaje_grasa = calcular_porcentaje_grasa(
                cintura, cuello, altura, genero_enum, cadera
            )

            return jsonify({"porcentaje_grasa": round(porcentaje_grasa, 2)}), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

    @app.route("/calcular_peso_grasa_corporal", methods=["POST"])
    def calcular_peso_grasa_corporal_endpoint():
        """
        Calcula el peso de la grasa corporal basado en los parámetros recibidos.

        Parámetros de la solicitud JSON:
        - peso: Peso total de la persona en kilogramos (obligatorio).
        - porcentaje_grasa: Porcentaje de grasa corporal (entre 0 y 100) (obligatorio).

        :return: Un JSON con el peso de la grasa corporal en kilogramos o un mensaje de error.
        """
        try:
            # Obtener los datos del cuerpo de la solicitud
            data = request.get_json()

            # Comprobación de existencia de parámetros
            if "peso" not in data or "porcentaje_grasa" not in data:
                return (
                    jsonify(
                        {
                            "error": "Faltan parámetros obligatorios: 'peso' y 'porcentaje_grasa'."
                        }
                    ),
                    400,
                )

            peso = data.get("peso")
            porcentaje_grasa = data.get("porcentaje_grasa")

            # Validación de tipos de datos y valores
            if not isinstance(peso, float):
                return (
                    jsonify(
                        {"error": "El valor de 'peso' debe ser un número positivo."}
                    ),
                    400,
                )
            if not isinstance(porcentaje_grasa, float):
                return (
                    jsonify(
                        {
                            "error": "El valor de 'porcentaje_grasa' debe ser un número entre 0 y 100."
                        }
                    ),
                    400,
                )

            # Validación de rango de valores
            if peso <= 0:
                return jsonify({"error": "El peso debe ser un número positivo."}), 400
            if not (0 <= porcentaje_grasa <= 100):
                return (
                    jsonify(
                        {"error": "El porcentaje de grasa debe estar entre 0 y 100."}
                    ),
                    400,
                )

            # Calcular el peso de la grasa corporal
            resultado = calcular_peso_grasa_corporal(peso, porcentaje_grasa)

            # Devolver el resultado
            return jsonify({"peso_grasa_corporal": resultado}), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

    @app.route("/calcular_sobrepeso", methods=["POST"])
    def calcular_sobrepeso_endpoint():
        """
        Calcula el sobrepeso basado en los parámetros recibidos.

        Parámetros de la solicitud JSON:
        - peso: Peso de la persona (obligatorio)
        - altura: Altura de la persona (obligatorio)

        :return: Un JSON con el sobrepeso calculado o un mensaje de error.
        """
        try:
            data = request.get_json()

            # Validación de parámetros obligatorios
            peso = data.get("peso")
            altura = data.get("altura")

            if None in (peso, altura):
                return (
                    jsonify(
                        {
                            "error": "Faltan parámetros obligatorios: peso y altura son requeridos."
                        }
                    ),
                    400,
                )

            # Validación adicional de tipos de datos
            if not isinstance(peso, (int, float)) or not isinstance(
                altura, (int, float)
            ):
                return (
                    jsonify(
                        {
                            "error": "Los parámetros 'peso' y 'altura' deben ser numéricos."
                        }
                    ),
                    400,
                )

            if peso <= 0 or altura <= 0:
                return (
                    jsonify(
                        {
                            "error": "Los valores de 'peso' y 'altura' deben ser mayores que 0."
                        }
                    ),
                    400,
                )

            # Calcular sobrepeso
            resultado = calcular_sobrepeso(peso, altura)

            return jsonify({"sobrepeso": f"{resultado:.2f}"}), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

    @app.route("/calcular_rcc", methods=["POST"])
    def calcular_rcc_endpoint():
        """
        Calcula el ratio cintura-cadera (RCC) basado en los parámetros recibidos.

        Parámetros de la solicitud JSON:
        - cintura: Circunferencia de cintura (obligatorio)
        - cadera: Circunferencia de cadera (obligatorio)

        :return: Un JSON con el RCC calculado o un mensaje de error.
        """
        try:
            data = request.get_json()
            cintura = data.get("cintura")
            cadera = data.get("cadera")

            if None in (cintura, cadera):
                return jsonify({"error": "Faltan parámetros obligatorios"}), 400

            resultado = calcular_rcc(cintura, cadera)
            return jsonify({"rcc": resultado}), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/calcular_tmb", methods=["POST"])
    def calcular_tmb_endpoint():
        """
        Endpoint para calcular la Tasa Metabólica Basal (TMB) usando la fórmula de Harris-Benedict.
        """
        try:
            data = request.get_json()

            if not data:
                return jsonify({"error": "El cuerpo de la solicitud debe ser un JSON válido"}), 400

            peso = data.get("peso")
            altura = data.get("altura")
            edad = data.get("edad")
            genero = data.get("genero", "").strip().lower()

            if None in (peso, altura, edad, genero):
                return jsonify({"error": "Faltan parámetros obligatorios: peso, altura, edad o genero"}), 400

            try:
                peso = float(peso)
                altura = float(altura)
                edad = int(edad)
                genero = str(genero)
            except ValueError:
                return jsonify({"error": "Peso, altura y edad deben ser mayores que cero, genero debe ser str."}), 400

            try:
                genero_enum = convertir_genero(genero)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

            tmb = calcular_tmb(peso, altura, edad, genero_enum)

            return jsonify({"tmb": round(tmb,2)}), 200

        except Exception as e:
            return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500


    @app.route("/calcular_imc", methods=["POST"])
    def calcular_imc_endpoint():
        """
        Calcula el índice de masa corporal (IMC) basado en los parámetros recibidos.

        Parámetros de la solicitud JSON:
        - peso:Peso de la persona (requerido)
        - altura:Altura de la persona (requerido)

        :return: Un JSON con el IMC calculado o un mensaje de error.
        """
        try:
            data = request.get_json()
            peso = data.get("peso")
            altura = data.get("altura")

            if None in (peso, altura):
                return jsonify({"error": "Faltan parámetros obligatorios"}), 400

            resultado = calcular_imc(peso, altura)
            return jsonify({"imc": resultado}), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/calcular_agua_total", methods=["POST"])
    def calcular_agua_total_endpoint():
        """
        Calcula el total de agua corporal basado en los parámetros recibidos.

        Parámetros de la solicitud JSON:
        - peso: Peso de la persona (obligatorio)
        - altura: Altura de la persona (obligatorio)
        - edad: Edad de la persona (obligatorio)
        - genero: Género de la persona ('h' para hombre, 'm' para mujer) (obligatorio)

        :return: Un JSON con la cantidad de agua total o un mensaje de error.
        """
        try:
            data = request.get_json()
            peso = data.get("peso")
            altura = data.get("altura")
            edad = data.get("edad")
            genero = data.get("genero", "").strip().lower()

            # Verificar si todos los parámetros obligatorios están presentes
            if None in (peso, altura, edad, genero):
                return jsonify({"error": "Faltan parámetros obligatorios"}), 400

            # Validar genero ('h' o 'm')
            if genero not in ["h", "m"]:
                return (
                    jsonify({"error": "El valor de 'genero' debe ser 'h' o 'm'."}),
                    400,
                )

            # Convertir genero a Enum Sexo
            genero_enum = Sexo.HOMBRE if genero == "h" else Sexo.MUJER

            # Llamar a la función de cálculo
            resultado = calcular_agua_total(peso, altura, edad, genero_enum)
            return jsonify({"agua_total": resultado}), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/calcular_peso_saludable", methods=["POST"])
    def calcular_peso_saludable_endpoint():
        """
        Calcula el rango de peso saludable basado en la altura recibida.

        Parámetros de la solicitud JSON:
        - altura: Altura de la persona (obligatorio)

        :return: Un JSON con el rango de peso saludable o un mensaje de error.
        """
        try:
            data = request.get_json()
            altura = data.get("altura")

            if altura is None:
                return (
                    jsonify({"error": "Falta el parámetro obligatorio 'altura'"}),
                    400,
                )

            resultado_min, resultado_max = calcular_peso_saludable(altura)
            return (
                jsonify(
                    {
                        "peso_min": f"{resultado_min:.2f}",
                        "peso_max": f"{resultado_max:.2f}",
                    }
                ),
                200,
            )

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/interpretar_imc", methods = ["POST"])
    def interpretar_imc_endpoint():
        """
        Interpreta el valor del IMC teniendo en cuenta el FFMI y el género.
        """
        try:
            data = request.get_json()
            imc = data.get("imc")
            ffmi = data.get("ffmi")
            genero = data.get("genero", "").strip().lower()

            if imc is None or ffmi is None or genero is None:
                return jsonify({"error": "Faltan parámetros obligatorios: imc, ffmi o genero"}), 400

            try:
                imc = float(imc)
                ffmi = float(ffmi)
            except ValueError:
                return jsonify({"error": "Los valores de 'imc' y 'ffmi' deben ser numéricos."}), 400

            try:
                genero_enum = convertir_genero(genero)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

            # Lógica de interpretación
            if imc > 25 and ffmi > 16:
                resultado = "El IMC es alto, pero puede estar influenciado por una alta masa muscular."
            elif imc < 18.5:
                resultado = "El IMC es bajo, se recomienda consultar con un profesional de salud."
            else:
                resultado = "El IMC está dentro del rango normal."

            return jsonify({"interpretacion_imc": resultado}), 200

        except Exception as e:
            return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

    @app.route("/interpretar_porcentaje_grasa", methods = ["POST"])
    def interpretar_porcentaje_grasa_endpoint():
        """
        Interpreta el porcentaje de grasa corporal junto con el género del usuario.
        """
        try:
            data = request.get_json()
            porcentaje_grasa = data.get("porcentaje_grasa")
            genero = data.get("genero", "").strip().lower()

            if porcentaje_grasa is None or genero is None:
                return jsonify({"error": "Faltan parámetros obligatorios: porcentaje_grasa y genero"}), 400

            try:
                porcentaje_grasa = float(porcentaje_grasa)
            except ValueError:
                return jsonify({"error": "El valor de 'porcentaje_grasa' debe ser numérico."}), 400

            try:
                genero_enum = convertir_genero(genero)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

            if genero_enum == Sexo.HOMBRE:
                if porcentaje_grasa > GRASA_ALTA_HOMBRES:
                    resultado = "Alto"
                elif porcentaje_grasa < GRASA_BAJA_HOMBRES:
                    resultado = "Bajo"
                else:
                    resultado = "Normal"
            else:  # Sexo.MUJER
                if porcentaje_grasa > GRASA_ALTA_MUJERES:
                    resultado = "Alto"
                elif porcentaje_grasa < GRASA_BAJA_MUJERES:
                    resultado = "Bajo"
                else:
                    resultado = "Normal"

            return jsonify({"interpretacion_grasa": resultado}), 200

        except Exception as e:
            return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

    @app.route("/interpretar_ffmi", methods = ["POST"])
    def interpretar_ffmi_endpoint():
        """
        Interpreta el FFMI recibido junto con el género.
        """
        try:
            data = request.get_json()
            ffmi = data.get("ffmi")
            genero = data.get("genero", "").strip().lower()

            if ffmi is None or genero is None:
                return jsonify({"error": "Faltan parámetros obligatorios: 'ffmi' y 'genero'"}), 400

            #  Convertir ffmi a número
            try:
                ffmi = float(ffmi)
            except ValueError:
                return jsonify({"error": "El valor de 'ffmi' debe ser numérico."}), 400

            #  Usar función centralizada
            try:
                genero_enum = convertir_genero(genero)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

            # Obtener umbrales correctos
            umbrales = FFMI_UMBRAL_HOMBRES if genero_enum == Sexo.HOMBRE else FFMI_UMBRAL_MUJERES

            # Interpretación
            if ffmi < umbrales[0]:
                resultado = "Lejos del máximo potencial (pobre forma física)."
            elif umbrales[0] <= ffmi < umbrales[1]:
                resultado = "Cercano a la normalidad."
            elif umbrales[1] <= ffmi < umbrales[2]:
                resultado = "Normal."
            elif umbrales[2] <= ffmi < umbrales[3]:
                resultado = "Superior a la normalidad (buena forma física)."
            elif umbrales[3] <= ffmi < umbrales[4]:
                resultado = "Fuerte (muy buena forma física)."
            elif umbrales[4] <= ffmi < umbrales[5]:
                resultado = "Muy fuerte (excelente forma física). Cerca del máximo potencial."
            elif umbrales[5] <= ffmi < umbrales[6]:
                resultado = "Muy cerca del máximo potencial."
            else:
                resultado = "Potencial máximo natural alcanzado. Muy muy pocos llegan naturales."

            return jsonify({"interpretacion_ffmi": resultado}), 200

        except Exception as e:
            return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

    @app.route("/interpretar_rcc", methods = ["POST"])
    def interpretar_rcc_endpoint():
        """
        Interpreta el ratio cintura-cadera (RCC) según el género del usuario.
        """
        try:
            data = request.get_json()
            rcc = data.get("rcc")
            genero = data.get("genero", "").strip().lower()

            if rcc is None or genero is None:
                return jsonify({"error": "Faltan parámetros obligatorios: rcc y genero"}), 400

            try:
                rcc = float(rcc)
            except ValueError:
                return jsonify({"error": "El valor de 'rcc' debe ser numérico."}), 400

            try:
                genero_enum = convertir_genero(genero)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

            # Interpretación sobre el género
            if genero_enum == Sexo.HOMBRE:
                if rcc > RCC_ALTO_HOMBRES:
                    resultado = "Alto riesgo."
                elif RCC_MODERADO_HOMBRES < rcc <= RCC_ALTO_HOMBRES:
                    resultado = "Moderado riesgo."
                else:
                    resultado = "Bajo riesgo."
            else:  # Sexo.MUJER
                if rcc > RCC_ALTO_MUJERES:
                    resultado = "Alto riesgo."
                elif RCC_MODERADO_MUJERES < rcc <= RCC_ALTO_MUJERES:
                    resultado = "Moderado riesgo."
                else:
                    resultado = "Bajo riesgo."

            return jsonify({"interpretacion_rcc": resultado}), 200

        except Exception as e:
            return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

    @app.route("/interpretar_ratio_cintura_altura", methods=["POST"])
    def interpretar_ratio_cintura_altura_endpoint():
        """
        Interpreta el ratio cintura-altura recibidos.

        Parámetros de la solicitud JSON:
        - ratio: Ratio cintura-altura (obligatorio)

        :return: Un JSON con la interpretación del ratio cintura-altura o un mensaje de error.
        """
        try:
            data = request.get_json()
            ratio = data.get("ratio")

            # Validación de que el parámetro ratio no sea nulo y sea un valor numérico positivo
            if ratio is None:
                return jsonify({"error": "Falta el parámetro obligatorio 'ratio'"}), 400
            if not isinstance(ratio, (int, float)):
                return jsonify({"error": "El valor de 'ratio' debe ser un número"}), 400
            if ratio <= 0:
                return (
                    jsonify(
                        {"error": "El valor de 'ratio' debe ser un número positivo"}
                    ),
                    400,
                )

            # Interpretación del ratio cintura-altura
            if ratio >= RATIO_ALTO_RIESGO:
                resultado = "Alto riesgo."
            elif RATIO_MODERADO_RIESGO <= ratio < RATIO_ALTO_RIESGO:
                resultado = "Moderado riesgo."
            else:
                resultado = "Bajo riesgo."

            return jsonify({"interpretacion_ratio_cintura_altura": resultado}), 200

        except ValueError as e:
            return jsonify({"error": f"Error de valor: {str(e)}"}), 400
        except TypeError as e:
            return jsonify({"error": f"Error de tipo: {str(e)}"}), 400
        except Exception as e:
            return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

    @app.route("/calorias_diarias", methods=["POST"])
    def calorias_diarias_endpoint():
        """
        Endpoint para calcular las calorías diarias basadas en TMB y objetivo nutricional.
        """
        try:
            data = request.get_json()

            # Validación de parámetros necesarios
            peso = data.get("peso")
            altura = data.get("altura")
            edad = data.get("edad")
            genero = data.get("genero", "").strip().lower()
            objetivo = data.get("objetivo")

            # Validación de valores
            if None in (peso, altura, edad, genero, objetivo):
                return jsonify({"error": "Faltan parámetros obligatorios"}), 400

            try:
                peso = float(peso)
                altura = float(altura)
                edad = int(edad)
            except ValueError:
                return jsonify({"error": "Peso y altura deben ser numéricos. Edad debe ser un entero."}), 400

            if peso <= 0 or altura <= 0 or edad <= 0:
                return jsonify({"error": "Peso, altura y edad deben ser mayores que cero."}), 400

            # Uso las funciones centralizadas
            try:
                genero_enum = convertir_genero(genero)
                objetivo_enum = convertir_objetivo(objetivo)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

            #  Calculamos
            tmb = calcular_tmb(peso, altura, edad, genero_enum)
            calorias_diarias = round(calcular_calorias_diarias(tmb, objetivo_enum), 2)

            return jsonify({"calorias_diarias": calorias_diarias}), 200

        except Exception as e:
            return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

    @app.route("/macronutrientes", methods = ["POST"])
    def macronutrientes_endpoint():
        """
        Calcula los macronutrientes diarios basados en calorías y objetivo nutricional.
        """
        try:
            data = request.get_json()
            calorias_diarias = data.get("calorias_diarias")
            objetivo = data.get("objetivo")

            if calorias_diarias is None or objetivo is None:
                return jsonify({"error": "Faltan parámetros obligatorios"}), 400

            try:
                calorias_diarias = float(calorias_diarias)
                if calorias_diarias <= 0:
                    raise ValueError("Las calorías deben ser un número positivo.")
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

            try:
                objetivo_enum = convertir_objetivo(objetivo)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

            proteinas, carbohidratos, grasas = calcular_macronutrientes(
                calorias_diarias, objetivo_enum
                )

            return jsonify(
                {
                    "macronutrientes": {
                        "proteinas": round(proteinas, 2),
                        "carbohidratos": round(carbohidratos, 2),
                        "grasas": round(grasas, 2),
                        }
                    }
                ), 200

        except Exception as e:
            return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

    @app.route("/informe_completo", methods = ["POST"])
    def informe_completo_endpoint():
        try:
            data = request.get_json()

            # Extraer datos
            peso = data.get("peso")
            altura = data.get("altura")
            edad = data.get("edad")
            genero = data.get("genero", "").strip().lower()
            cuello = data.get("cuello")
            cintura = data.get("cintura")
            cadera = data.get("cadera")
            objetivo = data.get("objetivo")

            if None in (peso, altura, edad, genero, cuello, cintura, objetivo):
                return jsonify({"error": "Faltan parámetros obligatorios"}), 400

            # Validar tipos
            try:
                peso = float(peso)
                altura = float(altura)
                edad = int(edad)
                cuello = float(cuello)
                cintura = float(cintura)
                cadera = float(cadera) if cadera is not None else 0
            except ValueError:
                return jsonify({"error": "Parámetros numéricos inválidos"}), 400

            if peso <= 0 or altura <= 0 or edad <= 0:
                return jsonify({"error": "Peso, altura y edad deben ser mayores que cero"}), 400

            # Convertir genero y objetivo
            try:
                genero_enum = convertir_genero(genero)
                objetivo_enum = convertir_objetivo(objetivo)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

            # Cálculos principales
            porcentaje_grasa = calcular_porcentaje_grasa(cintura, cuello, altura, genero_enum, cadera)
            tmb = calcular_tmb(peso, altura, edad, genero_enum)
            imc = calcular_imc(peso, altura)
            masa_muscular = peso - (peso * (porcentaje_grasa / 100))
            agua_total = calcular_agua_total(peso, altura, edad, genero_enum)
            ffmi = calcular_ffmi(masa_muscular, altura)
            peso_saludable_min, peso_saludable_max = calcular_peso_saludable(altura)
            sobrepeso = calcular_sobrepeso(peso, altura)
            rcc = calcular_rcc(cintura, cadera) if genero_enum == Sexo.MUJER else "N/A"
            ratio_cintura_altura = calcular_ratio_cintura_altura(cintura, altura)

            calorias_diarias = calcular_calorias_diarias(tmb, objetivo_enum)
            proteinas, carbohidratos, grasas = calcular_macronutrientes(calorias_diarias, objetivo_enum)

            # Interpretaciones
            interpretaciones = {
                "imc": interpretar_imc(imc, ffmi, genero_enum),
                "porcentaje_grasa": interpretar_porcentaje_grasa(porcentaje_grasa, genero_enum),
                "ffmi": interpretar_ffmi(ffmi, genero_enum),
                "rcc": interpretar_rcc(rcc, genero_enum) if genero_enum == Sexo.MUJER else "N/A",
                "ratio_cintura_altura": interpretar_ratio_cintura_altura(ratio_cintura_altura),
                }

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

            return jsonify(
                {
                    "resultados": resultados,
                    "interpretaciones": interpretaciones
                    }
                ), 200

        except Exception as e:
            return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500



