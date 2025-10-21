# app/blueprints/api/routes.py
"""
API REST Routes
Endpoints JSON para frontend futuro
---
components:
  schemas:
    GenericError:
      type: object
      properties:
        status:
          type: string
          example: error
        message:
          type: string
    BiometricAnalysis:
      type: object
      properties:
        id: { type: integer }
        user_id: { type: integer }
        weight: { type: number, format: float }
        height: { type: number, format: float }
        age: { type: integer }
        gender: { type: string }
        neck: { type: number, format: float }
        waist: { type: number, format: float }
        hip: { type: number, format: float, nullable: true }
        bmi: { type: number, format: float }
        body_fat_percentage: { type: number, format: float }
        # ... (añade el resto de campos si necesitas más detalle en la doc) ...
        created_at: { type: string, format: date-time }
    UserProfile:
       type: object
       properties:
         id: { type: integer }
         username: { type: string }
         email: { type: string, format: email }
         first_name: { type: string, nullable: true }
         last_name: { type: string, nullable: true }
         is_admin: { type: boolean }
         created_at: { type: string, format: date-time, nullable: true }
    ContactMessage:
        type: object
        properties:
          id: { type: integer }
          user_id: { type: integer }
          username: { type: string }
          user_email: { type: string, format: email }
          subject: { type: string }
          message: { type: string }
          analysis_id: { type: integer, nullable: true }
          is_read: { type: boolean }
          read_at: { type: string, format: date-time, nullable: true }
          created_at: { type: string, format: date-time }

  securitySchemes:
    # Si usaras autenticación Bearer para la API, la definirías aquí
    # bearerAuth:
    #   type: http
    #   scheme: bearer
    #   bearerFormat: JWT
    cookieAuth: # Para Flask-Login basado en cookies (puede no ser usable por OpenAI)
        type: apiKey
        in: cookie
        name: session # O el nombre de tu cookie de sesión
---
"""
from flask import jsonify, request
from flask_login import current_user, login_required

# Asumiendo que db está importado correctamente desde app
from app import db
from app.models.biometric_analysis import BiometricAnalysis
from app.models.contact_message import ContactMessage
from . import api_bp


@api_bp.route("/health", methods=["GET"])
def health_check():
    """Endpoint de verificación de estado
    ---
    get:
      tags: [Estado]
      summary: Verifica el estado de la API.
      description: Endpoint simple para confirmar que la API está funcionando.
      operationId: health_check_api_v1
      x-openai-is-consequential: false # GET es seguro
      responses:
        200:
          description: API está saludable.
          content:
            application/json:
              schema:
                type: object
                properties:
                  status: { type: string, example: healthy }
                  service: { type: string, example: "CoachBodyFit360 API" }
                  version: { type: string, example: "v1.0.0" }
    """
    return (
        jsonify(
            {"status": "healthy", "service": "CoachBodyFit360 API", "version": "v1.0.0"}
        ),
        200,
    )


@api_bp.route("/analysis/<int:analysis_id>", methods=["GET"])
@login_required # Nota: OpenAI podría no manejar login basado en cookies fácilmente
def get_analysis(analysis_id):
    """Obtener un análisis biométrico por ID
    ---
    get:
      tags: [Análisis]
      summary: Obtiene los detalles de un análisis biométrico específico.
      description: Retorna el análisis completo en JSON. Requiere que el usuario esté autenticado (sesión web).
      operationId: get_analysis_by_id_api_v1
      x-openai-is-consequential: false # GET es seguro
      parameters:
        - name: analysis_id
          in: path
          required: true
          description: ID del análisis a obtener.
          schema:
            type: integer
      security:
           # Indica que usa la cookie de sesión de Flask-Login
           # - cookieAuth: []
           # Si usaras JWT/Bearer, sería:
           # - bearerAuth: []
           # **Importante**: OpenAI puede tener problemas con cookieAuth.
           # Considera usar autenticación por Token/API Key para el agente.
           # Por ahora, lo dejamos comentado para ver si OpenAI lo maneja.
           - {} # Permite probar sin seguridad definida explícitamente para OpenAI
      responses:
        200:
          description: Análisis encontrado y devuelto.
          content:
            application/json:
              schema:
                type: object
                properties:
                  status: { type: string, example: success }
                  data: {$ref: '#/components/schemas/BiometricAnalysis'}
        403:
          description: Sin permiso para ver este análisis.
          content:
            application/json:
              schema: {$ref: '#/components/schemas/GenericError'}
        404:
          description: Análisis no encontrado.
          content:
            application/json:
              schema: {$ref: '#/components/schemas/GenericError'}
        401:
          description: No autenticado.
          content:
             application/json:
               schema: {$ref: '#/components/schemas/GenericError'}
    """
    analysis = BiometricAnalysis.query.get(analysis_id)

    if not analysis:
        return jsonify({"status": "error", "message": "Análisis no encontrado"}), 404

    # La protección @login_required ya maneja el 401 si no hay sesión
    if analysis.user_id != current_user.id and not current_user.is_admin:
        return (
            jsonify(
                {"status": "error", "message": "Sin permiso para ver este análisis"}
            ),
            403,
        )

    return jsonify({"status": "success", "data": analysis.to_dict()}), 200


@api_bp.route("/history", methods=["GET"])
@login_required # Requiere autenticación
def get_history():
    """Obtener historial de análisis del usuario
    ---
    get:
      tags: [Análisis]
      summary: Retorna el historial de análisis biométricos del usuario autenticado.
      description: Devuelve una lista de todos los análisis del usuario. Requiere autenticación (sesión web).
      operationId: get_user_history_api_v1
      x-openai-is-consequential: false # GET es seguro
      security:
        - {} # Permite probar sin seguridad definida explícitamente para OpenAI
      responses:
        200:
          description: Historial de análisis devuelto exitosamente.
          content:
            application/json:
              schema:
                type: object
                properties:
                  status: { type: string, example: success }
                  count: { type: integer, example: 5 }
                  data:
                    type: array
                    items: { $ref: '#/components/schemas/BiometricAnalysis' }
        401:
          description: No autenticado.
          content:
             application/json:
               schema: { $ref: '#/components/schemas/GenericError' }
    """
    analyses = BiometricAnalysis.query.filter_by(user_id=current_user.id).order_by(
        BiometricAnalysis.created_at.desc()
    ).all()

    return (
        jsonify(
            {
                "status": "success",
                "count": len(analyses),
                # Devuelve el diccionario completo generado por to_dict()
                "data": [analysis.to_dict() for analysis in analyses],
            }
        ),
        200,
    )


@api_bp.route("/analysis", methods=["POST"])
@login_required # Requiere autenticación
def create_analysis():
    """Crear un nuevo análisis biométrico
    ---
    post:
      tags: [Análisis]
      summary: Crea un nuevo registro de análisis biométrico.
      description: Recibe datos biométricos en formato JSON. Actualmente no implementado. Requiere autenticación.
      operationId: create_analysis_api_v1
      x-openai-is-consequential: true # POST tiene consecuencias
      security:
        - {} # Permite probar sin seguridad definida explícitamente para OpenAI
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                weight: { type: number, format: float, description: "Peso en kg" }
                height: { type: number, format: float, description: "Altura en cm" }
                age: { type: integer, description: "Edad en años" }
                gender: { type: string, enum: ['male', 'female', 'other'], description: "Género" }
                neck: { type: number, format: float, description: "Circunferencia cuello en cm" }
                waist: { type: number, format: float, description: "Circunferencia cintura en cm" }
                hip: { type: number, format: float, description: "Circunferencia cadera en cm (opcional)", nullable: true }
                # ... añade otras propiedades opcionales que tu API pueda aceptar ...
              required: [weight, height, age, gender, neck, waist]
      responses:
        501:
          description: Endpoint en desarrollo.
          content:
            application/json:
              schema: { $ref: '#/components/schemas/GenericError' }
        400:
           description: Datos inválidos.
           content:
             application/json:
               schema: { $ref: '#/components/schemas/GenericError' }
        401:
           description: No autenticado.
           content:
             application/json:
               schema: { $ref: '#/components/schemas/GenericError' }
    """
    # Tu código actual que devuelve 501
    try:
        data = request.get_json()
        required_fields = ["weight", "height", "age", "gender", "neck", "waist"]
        for field in required_fields:
            if field not in data:
                return (
                    jsonify(
                        {"status": "error", "message": f"Campo requerido: {field}"}
                    ),
                    400,
                )
        # --- Aquí iría la lógica real cuando la implementes ---
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Endpoint en desarrollo. Usa el formulario web.",
                }
            ),
            501,
        )
    except Exception as e:
        # Loggear el error real sería bueno aquí
        return jsonify({"status": "error", "message": str(e)}), 500


@api_bp.route("/profile", methods=["GET"])
@login_required # Requiere autenticación
def get_profile():
    """Obtener perfil del usuario actual
    ---
    get:
      tags: [Usuario]
      summary: Devuelve los datos del perfil del usuario autenticado.
      description: Retorna información básica del usuario. Requiere autenticación (sesión web).
      operationId: get_current_user_profile_api_v1
      x-openai-is-consequential: false # GET es seguro
      security:
        - {} # Permite probar sin seguridad definida explícitamente para OpenAI
      responses:
        200:
          description: Perfil del usuario devuelto exitosamente.
          content:
            application/json:
              schema:
                type: object
                properties:
                  status: { type: string, example: success }
                  data: { $ref: '#/components/schemas/UserProfile' }
        401:
          description: No autenticado.
          content:
             application/json:
               schema: { $ref: '#/components/schemas/GenericError' }
    """
    return (
        jsonify(
            {
                "status": "success",
                "data": {
                    "id": current_user.id,
                    "username": current_user.username,
                    "email": current_user.email,
                    "first_name": current_user.first_name,
                    "last_name": current_user.last_name,
                    "is_admin": current_user.is_admin,
                    "created_at": (
                        current_user.created_at.isoformat()
                        if current_user.created_at
                        else None
                    ),
                },
            }
        ),
        200,
    )


@api_bp.route("/contact", methods=["POST"])
@login_required # Requiere autenticación
def send_message():
    """Enviar mensaje de contacto
    ---
    post:
      tags: [Contacto]
      summary: Envía un mensaje de contacto al entrenador.
      description: Guarda un mensaje enviado por el usuario autenticado.
      operationId: send_contact_message_api_v1
      x-openai-is-consequential: true # POST tiene consecuencias
      security:
        - {} # Permite probar sin seguridad definida explícitamente para OpenAI
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                subject: { type: string, description: "Asunto del mensaje", maxLength: 200 }
                message: { type: string, description: "Contenido del mensaje" }
                analysis_id: { type: integer, description: "ID del análisis relacionado (opcional)", nullable: true }
              required: [subject, message]
      responses:
        201:
          description: Mensaje enviado correctamente.
          content:
            application/json:
              schema:
                type: object
                properties:
                  status: { type: string, example: success }
                  message: { type: string }
                  data: { $ref: '#/components/schemas/ContactMessage' }
        400:
          description: Datos de entrada inválidos (falta subject o message).
          content:
            application/json:
              schema: { $ref: '#/components/schemas/GenericError' }
        401:
           description: No autenticado.
           content:
             application/json:
               schema: { $ref: '#/components/schemas/GenericError' }
        500:
           description: Error interno al guardar el mensaje.
           content:
             application/json:
               schema: { $ref: '#/components/schemas/GenericError' }
    """
    try:
        data = request.get_json()
        if not data.get("subject") or not data.get("message"):
            return (
                jsonify(
                    {"status": "error", "message": "Subject y message son requeridos"}
                ),
                400,
            )

        message = ContactMessage(
            user_id=current_user.id,
            subject=data["subject"],
            message=data["message"],
            analysis_id=data.get("analysis_id"),
        )
        db.session.add(message)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Mensaje enviado correctamente",
                    "data": message.to_dict(),
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        # Loggear el error real sería bueno aquí
        return jsonify({"status": "error", "message": "Error al guardar el mensaje"}), 500


@api_bp.route("/admin/messages", methods=["GET"])
@login_required # Requiere autenticación y ser admin
def get_messages():
    """Obtener todos los mensajes (Admin)
    ---
    get:
      tags: [Admin, Contacto]
      summary: Devuelve todos los mensajes de contacto (solo para administradores).
      description: Requiere autenticación como administrador. Permite filtrar por no leídos.
      operationId: get_admin_messages_api_v1
      x-openai-is-consequential: false # GET es seguro
      security:
        - {} # Permite probar sin seguridad definida explícitamente para OpenAI
      parameters:
        - name: unread
          in: query
          required: false
          description: Si es 'true', devuelve solo los mensajes no leídos.
          schema:
            type: boolean
            default: false
      responses:
        200:
          description: Lista de mensajes devuelta.
          content:
            application/json:
              schema:
                type: object
                properties:
                  status: { type: string, example: success }
                  count: { type: integer }
                  unread_count: { type: integer }
                  data:
                    type: array
                    items: { $ref: '#/components/schemas/ContactMessage' }
        401:
           description: No autenticado.
           content:
             application/json:
               schema: { $ref: '#/components/schemas/GenericError' }
        403:
           description: Acceso denegado (no es admin).
           content:
             application/json:
               schema: { $ref: '#/components/schemas/GenericError' }
    """
    if not current_user.is_admin:
        return (
            jsonify(
                {"status": "error", "message": "Acceso denegado. Solo administradores."}
            ),
            403,
        )

    unread_only = request.args.get("unread", "false").lower() == "true"
    query = ContactMessage.query
    if unread_only:
        query = query.filter_by(is_read=False)

    messages = query.order_by(ContactMessage.created_at.desc()).all()
    unread_count_val = ContactMessage.query.filter_by(is_read=False).count() # Renombrada para evitar conflicto

    return (
        jsonify(
            {
                "status": "success",
                "count": len(messages),
                "unread_count": unread_count_val,
                "data": [msg.to_dict() for msg in messages],
            }
        ),
        200,
    )


@api_bp.route("/admin/messages/<int:message_id>", methods=["PATCH"])
@login_required # Requiere autenticación y ser admin
def mark_message_read(message_id):
    """Marcar mensaje como leído (Admin)
    ---
    patch:
      tags: [Admin, Contacto]
      summary: Marca un mensaje específico como leído (solo para administradores).
      description: Actualiza el estado de un mensaje leído. Requiere autenticación como admin.
      operationId: mark_message_as_read_api_v1
      x-openai-is-consequential: true # PATCH tiene consecuencias
      security:
        - {} # Permite probar sin seguridad definida explícitamente para OpenAI
      parameters:
        - name: message_id
          in: path
          required: true
          description: ID del mensaje a marcar como leído.
          schema:
            type: integer
      response:
        200:
          description: Mensaje marcado como leído exitosamente.
          content:
            application/json:
              schema:
                type: object
                properties:
                  status: { type: string, example: success }
                  message: { type: string }
                  data: {$ref: '#/components/schemas/ContactMessage'}
        401:
           description: No autenticado.
           content:
             application/json:
               schema: {$ref: '#/components/schemas/GenericError'}
        403:
           description: Acceso denegado (no es admin).
           content:
             application/json:
               schema: {$ref: '#/components/schemas/GenericError'}
        404:
           description: Mensaje no encontrado.
           content:
             application/json:
               schema: {$ref: '#/components/schemas/GenericError'}
    """
    if not current_user.is_admin:
        return (
            jsonify(
                {"status": "error", "message": "Acceso denegado. Solo administradores."}
            ),
            403,
        )

    message = ContactMessage.query.get(message_id)
    if not message:
        return jsonify({"status": "error", "message": "Mensaje no encontrado"}), 404

    message.mark_as_read() # Asume que este método hace db.session.commit()

    return (
        jsonify(
            {
                "status": "success",
                "message": "Mensaje marcado como leído",
                "data": message.to_dict(), # Devuelve el mensaje actualizado
            }
        ),
        200,
    )