import json
import logging
import os
import re
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

    # Log parcial de la API key (por seguridad)
    logger.info(f"OPENAI_API_KEY detectada, comienza por: {api_key[:8]}... (longitud: {len(api_key)})")

    try:
        logger.info("Inicializando cliente OpenAI...")
        return OpenAI(api_key=api_key)
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
        Envía los resultados del análisis biométrico a GPT-4o y devuelve la interpretación, plan de nutrición y entrenamiento.
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
        prompt = FitMasterService._build_prompt(bio_payload)

        try:
            modelo_usado = "gpt-4o-mini"
            logger.info(f"Enviando solicitud a OpenAI. Modelo: {modelo_usado}")
            response = client.chat.completions.create(
                model=modelo_usado,
                messages=[
                    {"role": "system", "content": "Eres FitMaster, IA experta en fitness y nutrición."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=2600,
            )

            # Extraer y normalizar respuesta
            message = response.choices[0].message.content
            logger.info("Respuesta recibida de OpenAI")
            logger.info(f"Respuesta cruda de OpenAI: {message[:200]}...")

            # Limpiar respuesta de OpenAI
            cleaned_message = FitMasterService._clean_json_response(message)

            # Intentar parsear JSON
            try:
                data = json.loads(cleaned_message)
                logger.info("Respuesta JSON parseada correctamente")
                return FitMasterService._validate_response(data)
            except json.JSONDecodeError as e:
                logger.warning(f"Error al parsear JSON de OpenAI: {e}")
                logger.warning(f"Respuesta que causó el error: {message[:500]}")
                return {
                    "interpretation": message if message else "No se recibió respuesta de OpenAI",
                    "nutrition_plan": None,
                    "training_plan": None,
                }
        except Exception as exc:
            logger.error(f"Error en la conexión con OpenAI: {exc}")
            logger.error(f"Tipo de excepción: {type(exc)}")
            return FitMasterService._get_fallback_response(f"Error de conexión: {str(exc)}")

    @staticmethod
    def _build_prompt(bio_payload: Dict) -> str:
        """
        Lee el prompt base desde fitmaster_prompt.txt y lo formatea con los datos biométricos.
        """
        prompt_path = os.path.join(os.path.dirname(__file__), "fitmaster_prompt.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt_template = f.read()
        except Exception as e:
            logger.error(f"No se pudo leer el prompt externo: {e}")
            prompt_template = "Eres FitMaster AI. Analiza los datos: {bio_payload}"
        return prompt_template.replace("{bio_payload}", json.dumps(bio_payload, ensure_ascii=False, indent=2))

    @staticmethod
    def _clean_json_response(message: str) -> str:
        """
        Limpia la respuesta de OpenAI eliminando bloques de código markdown.

        Args:
            message: Respuesta cruda de OpenAI

        Returns:
            str: JSON limpio sin bloques de código markdown
        """
        if not message:
            return message

        # Patrón para capturar JSON dentro de bloques de código
        patterns = [
            r'```json\s*(.*?)\s*```',  # ```json { ... } ```
            r'```\s*(.*?)\s*```',       # ``` { ... } ```
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.DOTALL)
            if match:
                cleaned = match.group(1).strip()
                logger.info("JSON extraído de bloque markdown")
                return cleaned

        # Si no hay bloques markdown, devolver el mensaje tal cual
        return message.strip()

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
