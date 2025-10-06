import json
import logging
import os
from typing import Dict, Optional

from openai import OpenAI

# Configurar logging
logger = logging.getLogger(__name__)


# Inicializar cliente OpenAI con validación
def _get_openai_client() -> Optional[OpenAI]:
	"""Inicializar cliente OpenAI con validación de API key."""
	api_key = os.getenv("OPENAI_API_KEY")
	if not api_key:
		logger.warning("OPENAI_API_KEY no está configurada en las variables de entorno")
		return None

	try:
		return OpenAI(api_key = api_key)
	except Exception as e:
		logger.error(f"Error al inicializar cliente OpenAI: {e}")
		return None


client = _get_openai_client()


class FitMasterService:
	"""
	Servicio para analizar resultados biométricos con GPT-4o (FitMaster AI)
	"""

	@staticmethod
	def analyze_bio_results(bio_payload: Dict) -> Optional[Dict]:
		"""
		Envía los resultados del análisis biométrico a GPT-4o y devuelve la
		interpretación, plan de nutrición y entrenamiento.

		Args:
			bio_payload: Diccionario con los datos biométricos del usuario

		Returns:
			Dict con interpretación, nutrition_plan y training_plan, o None si hay error
		"""
		if not client:
			logger.error("Cliente OpenAI no está disponible")
			return FitMasterService._get_fallback_response("Cliente OpenAI no configurado")

		if not bio_payload:
			logger.error("bio_payload está vacío")
			return FitMasterService._get_fallback_response("Datos biométricos no válidos")

		prompt = f"""
        Eres FitMaster AI, un experto en fitness, nutrición y composición corporal.
        Analiza los siguientes datos biométricos y genera:

        1. Interpretación del estado corporal (peso, grasa, IMC, masa magra, metabolismo, etc.)
        2. Plan nutricional diario (objetivo, calorías, macros y ejemplo de comidas)
        3. Plan de entrenamiento semanal (frecuencia, tipo de rutina, ejercicios principales)

        Devuelve el resultado en formato JSON con esta estructura exacta:
        {{
          "interpretation": "...",
          "nutrition_plan": {{
            "goal": "...",
            "daily_calories": 0,
            "macros": {{"protein": 0, "carbs": 0, "fat": 0}},
            "meals": [{{"name": "...", "description": "..."}}]
          }},
          "training_plan": {{
            "frequency": "...",
            "routine_type": "...",
            "exercises": ["..."]
          }}
        }}
		
		IMPORTANTE: Responde ÚNICAMENTE con JSON válido. No agregues texto antes o después del JSON.
		Ejemplo de formato esperado:
		{{"interpretation": "...", "nutrition_plan": {{"goal": "..."}}, "training_plan": {{"frequency": "..."}}}}
		
		
        Datos del usuario:
        {bio_payload}
        """

		try:
			logger.info("Enviando solicitud a OpenAI GPT-4o")
			response = client.chat.completions.create(
				model = "gpt-4o-mini",
				messages = [
					{"role": "system", "content": "Eres FitMaster, IA experta en fitness y nutrición."},
					{"role": "user", "content": prompt},
					],
				temperature = 0.7,
				max_tokens = 2600,
				)

			# Extraer y normalizar respuesta
			message = response.choices[0].message.content
			logger.info("Respuesta recibida de OpenAI")

			# AGREGAR ESTA LÍNEA PARA VER LA RESPUESTA CRUDA:
			logger.info(f"Respuesta cruda de OpenAI: {message[:200]}...")

			# Intentar parsear JSON
			try:
				data = json.loads(message)
				logger.info("Respuesta JSON parseada correctamente")
				return FitMasterService._validate_response(data)
			except json.JSONDecodeError as e:
				logger.warning(f"Error al parsear JSON de OpenAI: {e}")
				logger.warning(f"Respuesta que causó el error: {message[:500]}")

				# Si no es JSON válido, usar como interpretación simple
				return {
					"interpretation": message if message else "No se recibió respuesta de OpenAI",
					"nutrition_plan": None,
					"training_plan": None,
					}

		except Exception as exc:
			logger.error(f"Error en la conexión con OpenAI: {exc}")
			return FitMasterService._get_fallback_response(f"Error de conexión: {str(exc)}")

	@staticmethod
	def _validate_response(data: Dict) -> Dict:
		"""Validar y normalizar la respuesta de OpenAI."""
		if not isinstance(data, dict):
			return FitMasterService._get_fallback_response("Respuesta no válida")

		# Asegurar que tenga las claves requeridas
		validated_data = {
			"interpretation": data.get("interpretation", "Análisis no disponible"),
			"nutrition_plan": data.get("nutrition_plan"),
			"training_plan": data.get("training_plan"),
			}

		return validated_data

	@staticmethod
	def _get_fallback_response(error_msg: str) -> Dict:
		"""Respuesta de respaldo cuando hay errores."""
		return {
			"interpretation": f"No se pudo conectar con FitMaster AI. {error_msg}",
			"nutrition_plan": None,
			"training_plan": None,
			}
