import json
import logging
import os
import re
from typing import Dict, Optional
from openai import OpenAI
from app import db

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
    logger.info(
        f"OPENAI_API_KEY detectada, comienza por: {api_key[:8]}... (longitud: {len(api_key)})"
    )

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
            return FitMasterService._get_fallback_response(
                "Cliente OpenAI no configurado"
            )

        if not bio_payload:
            logger.error("bio_payload está vacío")
            return FitMasterService._get_fallback_response(
                "Datos biométricos no válidos"
            )
        prompt = FitMasterService._build_prompt(bio_payload)

        try:
            modelo_usado = "gpt-4o-mini"
            logger.info(f"Enviando solicitud a OpenAI. Modelo: {modelo_usado}")
            response = client.chat.completions.create(
                model=modelo_usado,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres FitMaster, IA experta en fitness y nutrición.",
                    },
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
                    "interpretation": (
                        message if message else "No se recibió respuesta de OpenAI"
                    ),
                    "nutrition_plan": None,
                    "training_plan": None,
                }
        except Exception as exc:
            logger.error(f"Error en la conexión con OpenAI: {exc}")
            logger.error(f"Tipo de excepción: {type(exc)}")
            return FitMasterService._get_fallback_response(
                f"Error de conexión: {str(exc)}"
            )

    # ── Assistants API config ──────────────────────────────────
    ASSISTANT_ID = os.getenv(
        "OPENAI_ASSISTANT_ID", "asst_h2VGSmUO36ONu9Wf8am36oBT"
    )

    @staticmethod
    def chat_query(query: str, user_id: int, context: Optional[Dict] = None) -> str:
        """
        Maneja consultas via Assistants API con threads persistentes y RAG.
        """
        if not client:
            return "Lo siento, el motor de inteligencia artificial no está configurado."

        from app.models.telegram import UserTelegramLink
        link = UserTelegramLink.query.filter_by(user_id=user_id).first()
        if not link:
            return "No se encontró tu vinculación de Telegram."

        try:
            # 1. Obtener o crear Thread
            thread_id = link.openai_thread_id
            if not thread_id:
                thread = client.beta.threads.create()
                thread_id = thread.id
                link.openai_thread_id = thread_id
                db.session.commit()
                logger.info(f"Nuevo thread creado para user {user_id}: {thread_id}")

                # Inyectar contexto biométrico como primer mensaje del thread
                if context:
                    context_msg = (
                        "CONTEXTO DEL BACKEND CoachBodyFit360 — "
                        "Estos son los datos biométricos actuales del cliente. "
                        "Úsalos como fuente de verdad, NO pidas al usuario "
                        "que los repita:\n\n"
                        f"{json.dumps(context, ensure_ascii=False, indent=2)}"
                    )
                    client.beta.threads.messages.create(
                        thread_id=thread_id,
                        role="user",
                        content=context_msg,
                    )
                    # Run rápido para que el asistente "ingiera" el contexto
                    init_run = client.beta.threads.runs.create_and_poll(
                        thread_id=thread_id,
                        assistant_id=FitMasterService.ASSISTANT_ID,
                        timeout=30,
                    )
                    logger.info(f"Context ingestion run status: {init_run.status}")

            # 2. Enviar mensaje del usuario al thread
            client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=query,
            )

            # 3. Ejecutar el Assistant y esperar respuesta
            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=FitMasterService.ASSISTANT_ID,
                timeout=60,
            )

            if run.status != "completed":
                logger.error(f"Assistant run failed: {run.status} — {run.last_error}")
                return "Lo siento, tuve un problema al procesar tu consulta."

            # 4. Extraer el último mensaje del asistente
            messages = client.beta.threads.messages.list(
                thread_id=thread_id, order="desc", limit=1
            )
            reply = ""
            for msg in messages.data:
                if msg.role == "assistant":
                    for block in msg.content:
                        if block.type == "text":
                            reply = block.text.value
                    break

            if not reply:
                reply = "No obtuve una respuesta válida. Intenta de nuevo."

            # 5. Limpiar anotaciones de file_search (citas [0†source])
            import re
            reply = re.sub(r'【\d+[:\u2020†].*?】', '', reply).strip()

            # 6. Registrar consumo
            if run.usage:
                FitMasterService._record_usage(user_id, "assistants-api", run.usage)

            return reply

        except Exception as e:
            logger.error(f"Error en FitMaster Assistants chat_query: {e}")
            return "Lo siento, tuve un problema al procesar tu consulta."

    @staticmethod
    def _record_usage(user_id: int, model: str, usage_obj) -> None:
        """Registra el consumo de tokens en el ledger."""
        from app.models.telegram import LLMUsageLedger
        try:
            prompt_tokens = getattr(usage_obj, 'prompt_tokens', 0) or 0
            completion_tokens = getattr(usage_obj, 'completion_tokens', 0) or 0
            total_tokens = getattr(usage_obj, 'total_tokens', 0) or 0

            # Costes estimados gpt-4o-mini via Assistants
            prompt_cost = (prompt_tokens / 1_000_000) * 0.15
            completion_cost = (completion_tokens / 1_000_000) * 0.60

            entry = LLMUsageLedger(
                user_id=user_id,
                model_name=model,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                cost_usd=prompt_cost + completion_cost,
                channel="telegram"
            )
            db.session.add(entry)
            db.session.commit()
        except Exception as e:
            logger.error(f"Error registrando uso de tokens: {e}")


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
        return prompt_template.replace(
            "{bio_payload}", json.dumps(bio_payload, ensure_ascii=False, indent=2)
        )

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
            r"```json\s*(.*?)\s*```",  # ```json { ... } ```
            r"```\s*(.*?)\s*```",  # ``` { ... } ```
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
