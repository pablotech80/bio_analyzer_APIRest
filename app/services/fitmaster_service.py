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

            # Registrar consumo si hay usage disponible
            if hasattr(response, 'usage') and response.usage:
                # Extraemos user_id del payload biométrico si existe para poder vincularlo
                user_id = bio_payload.get('user_id', 0)
                if user_id > 0:
                    FitMasterService._record_usage(user_id, modelo_usado, response.usage, channel="web")

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
    def chat_query(query: str, user_id: int, context: Optional[Dict] = None, stream_callback=None) -> str:
        """
        Maneja consultas via Assistants API con threads persistentes y RAG.
        
        Args:
            query: Consulta del usuario
            user_id: ID del usuario
            context: Contexto biométrico opcional
            stream_callback: Función callback para streaming (recibe chunks de texto)
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
                # NO ejecutar un run aquí — el asistente lo leerá con el run principal
                if context:
                    context_msg = (
                        "CONTEXTO DEL BACKEND CoachBodyFit360 — "
                        "Estos son los datos biométricos actuales del cliente. "
                        "Úsalos como referencia. Para planes de nutrición y "
                        "entrenamiento SIEMPRE usa las herramientas get_current_plans() "
                        "y get_user_history().\n\n"
                        f"{json.dumps(context, ensure_ascii=False, indent=2)}"
                    )
                    client.beta.threads.messages.create(
                        thread_id=thread_id,
                        role="user",
                        content=context_msg,
                    )
                    logger.info(f"Contexto biométrico inyectado en thread {thread_id}")

            # 2. Cancelar runs activos/fallidos para evitar BadRequestError
            try:
                runs = client.beta.threads.runs.list(thread_id=thread_id, limit=5)
                for r in runs.data:
                    if r.status in ('in_progress', 'requires_action', 'queued'):
                        logger.warning(f"Cancelando run {r.id} en estado {r.status}")
                        client.beta.threads.runs.cancel(thread_id=thread_id, run_id=r.id)
            except Exception as cancel_err:
                logger.warning(f"Error cancelando runs previos: {cancel_err}")

            # 3. Enviar mensaje del usuario al thread
            client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=query,
            )

            # 4. Ejecutar el Assistant con streaming si hay callback
            if stream_callback:
                return FitMasterService._handle_streaming_run(
                    thread_id, user_id, stream_callback
                )
            else:
                # Modo sin streaming (polling)
                run = client.beta.threads.runs.create_and_poll(
                    thread_id=thread_id,
                    assistant_id=FitMasterService.ASSISTANT_ID,
                    timeout=60,
                )

                # 3.5. Manejar tool calls (FASE 3: Agent Tools)
                while run.status == 'requires_action':
                    tool_calls = run.required_action.submit_tool_outputs.tool_calls
                    tool_outputs = []
                    
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        arguments = json.loads(tool_call.function.arguments)
                        
                        logger.info(f"Asistente llamando a función: {function_name} con argumentos: {arguments}")
                        
                        try:
                            # Despachador de funciones
                            if function_name == "get_user_history":
                                output = FitMasterService._tool_get_user_history(user_id, arguments)
                            elif function_name == "get_current_plans":
                                output = FitMasterService._tool_get_current_plans(user_id)
                            else:
                                output = json.dumps({"error": f"Unknown function: {function_name}"})
                                
                        except Exception as e:
                            logger.error(f"Error ejecutando tool {function_name}: {e}", exc_info=True)
                            output = json.dumps({"error": str(e)})
                            
                        # Validar que output es string (requerido por API de OpenAI)
                        if not isinstance(output, str):
                            output = json.dumps(output)
                            
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": output
                        })
                    
                    # Enviar los resultados de las tools al Assistant
                    run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=tool_outputs,
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
            logger.error(f"Error en FitMaster Assistants chat_query: {type(e).__name__}: {e}", exc_info=True)
            return f"Lo siento, tuve un problema al procesar tu consulta. Error: {type(e).__name__}"

    @staticmethod
    def _handle_streaming_run(thread_id: str, user_id: int, stream_callback) -> str:
        """
        Maneja la ejecución del assistant con streaming.
        Usa submit_tool_outputs_stream para continuar el stream tras tool calls.
        El texto acumulado se comparte entre el stream principal y los sub-streams.
        """
        full_response_container = {"text": ""}

        def _execute_tools(tool_calls) -> list:
            """Ejecuta las tool calls y devuelve los outputs."""
            tool_outputs = []
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                try:
                    arguments = json.loads(tool_call.function.arguments)
                except Exception:
                    arguments = {}

                logger.info(f"[Stream] Tool call: {function_name}")

                try:
                    if function_name == "get_user_history":
                        output = FitMasterService._tool_get_user_history(user_id, arguments)
                    elif function_name == "get_current_plans":
                        output = FitMasterService._tool_get_current_plans(user_id)
                    else:
                        output = json.dumps({"error": f"Unknown function: {function_name}"})
                except Exception as e:
                    logger.error(f"Error en tool {function_name}: {e}", exc_info=True)
                    output = json.dumps({"error": str(e)})

                if not isinstance(output, str):
                    output = json.dumps(output)

                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": output
                })
            return tool_outputs

        def _process_stream(stream_obj):
            """Procesa un stream de eventos, manejando tool calls recursivamente."""
            for event in stream_obj:
                if event.event == 'thread.message.delta':
                    for content in event.data.delta.content:
                        if hasattr(content, 'text') and hasattr(content.text, 'value'):
                            chunk = content.text.value
                            full_response_container["text"] += chunk
                            if stream_callback:
                                try:
                                    stream_callback(chunk)
                                except Exception as cb_err:
                                    logger.error(f"Error en stream_callback: {cb_err}")

                elif event.event == 'thread.run.requires_action':
                    run_id = event.data.id
                    tool_calls = event.data.required_action.submit_tool_outputs.tool_calls
                    tool_outputs = _execute_tools(tool_calls)

                    # Abrir un nuevo stream para continuar tras las tool calls
                    with client.beta.threads.runs.submit_tool_outputs_stream(
                        thread_id=thread_id,
                        run_id=run_id,
                        tool_outputs=tool_outputs,
                    ) as tool_stream:
                        _process_stream(tool_stream)

        try:
            with client.beta.threads.runs.stream(
                thread_id=thread_id,
                assistant_id=FitMasterService.ASSISTANT_ID,
            ) as stream:
                _process_stream(stream)

            final_text = re.sub(r'【\d+[:\u2020†].*?】', '', full_response_container["text"]).strip()
            return final_text if final_text else "No obtuve una respuesta válida."

        except Exception as e:
            logger.error(f"Error crítico en streaming: {type(e).__name__}: {e}", exc_info=True)
            raise

    @staticmethod
    def _record_usage(user_id: int, model: str, usage_obj, channel: str = "telegram") -> None:
        """Registra el consumo de tokens en el ledger."""
        from app.models.telegram import LLMUsageLedger
        try:
            prompt_tokens = getattr(usage_obj, 'prompt_tokens', 0) or 0
            completion_tokens = getattr(usage_obj, 'completion_tokens', 0) or 0
            total_tokens = getattr(usage_obj, 'total_tokens', 0) or 0

            # Costes estimados gpt-4o-mini
            prompt_cost = (prompt_tokens / 1_000_000) * 0.15
            completion_cost = (completion_tokens / 1_000_000) * 0.60

            entry = LLMUsageLedger(
                user_id=user_id,
                model_name=model,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                cost_usd=prompt_cost + completion_cost,
                channel=channel
            )
            db.session.add(entry)
            db.session.commit()
        except Exception as e:
            logger.error(f"Error registrando uso de tokens: {e}")


    @staticmethod
    def _build_prompt(bio_payload: Dict) -> str:
        """
        Lee el prompt base desde fitmaster_prompt.yaml y lo formatea con los datos biométricos.
        """
        prompt_path = os.path.join(os.path.dirname(__file__), "fitmaster_prompt.yaml")
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
            "interpretation": data.get("interpretation", "Análisis no disponible")
        }

        return validated_data

    @staticmethod
    def _get_fallback_response(error_msg: str) -> Dict:
        """Respuesta de respaldo cuando hay errores."""
        return {
            "interpretation": f"No se pudo conectar con FitMaster AI. {error_msg}"
        }

    # ── Agent Tools (Fase 3) ───────────────────────────────────
    @staticmethod
    def _tool_get_user_history(user_id: int, arguments: Dict) -> str:
        """Obtiene el historial biométrico del usuario para el agente."""
        try:
            from app.models.biometric_analysis import BiometricAnalysis
            limit = arguments.get("limit", 5)
            analyses = BiometricAnalysis.query.filter_by(user_id=user_id).order_by(BiometricAnalysis.created_at.desc()).limit(limit).all()
            
            if not analyses:
                return json.dumps({"status": "no_data", "message": "El usuario no tiene análisis biométricos registrados."})
            
            data = []
            for a in analyses:
                data.append({
                    "id": a.id,
                    "date": a.created_at.strftime("%Y-%m-%d"),
                    "weight": a.weight,
                    "height": a.height,
                    "body_fat_percentage": a.body_fat_percentage,
                    "bmi": a.bmi,
                    "bmr": a.bmr,
                    "tdee": a.tdee,
                    "lean_mass": a.lean_mass,
                    "fat_mass": a.fat_mass
                })
            return json.dumps({"status": "success", "data": data})
        except Exception as e:
            logger.error(f"Error en _tool_get_user_history: {e}")
            return json.dumps({"error": str(e)})

    @staticmethod
    def _tool_get_current_plans(user_id: int) -> str:
        """Obtiene el plan de nutrición y entrenamiento REALES asignados al usuario."""
        try:
            from app.models.nutrition_plan import NutritionPlan
            from app.models.training_plan import TrainingPlan
            
            # Buscar el último plan de nutrición activo
            nutrition = NutritionPlan.query.filter_by(
                user_id=user_id, 
                is_active=True
            ).order_by(NutritionPlan.created_at.desc()).first()
            
            # Buscar el último plan de entrenamiento activo
            training = TrainingPlan.query.filter_by(
                user_id=user_id, 
                is_active=True
            ).order_by(TrainingPlan.created_at.desc()).first()
            
            if not nutrition and not training:
                return json.dumps({"status": "no_data", "message": "El usuario no tiene planes de nutrición ni entrenamiento activos asignados."})
            
            data = {}
            if nutrition:
                data["nutrition_plan"] = nutrition.to_dict()
                
            if training:
                data["training_plan"] = training.to_dict()
                
            return json.dumps({"status": "success", "data": data})
        except Exception as e:
            logger.error(f"Error en _tool_get_current_plans: {e}")
            return json.dumps({"error": str(e)})
