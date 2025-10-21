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
        # ... puedes añadir el resto de campos de tu modelo aquí ...
        created_at: { type: string, format: date-time }
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
---
"""
from flask import jsonify, request
from flask_login import current_user, login_required

from app.models.biometric_analysis import BiometricAnalysis
from app.models.contact_message import ContactMessage
from . import api_bp


@api_bp.route("/health", methods = ["GET"])
def health_check():
	"""Endpoint de verificación de estado
	---
	get:
	  tags: [Estado]
	  summary: Verifica el estado de la API.
	  description: Endpoint simple para confirmar que la API está funcionando.
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


@api_bp.route("/analysis/<int:analysis_id>", methods = ["GET"])
@login_required
def get_analysis(analysis_id):
	"""Obtener un análisis biométrico por ID
	---
	get:
	  tags: [Análisis]
	  summary: Obtiene los detalles de un análisis biométrico específico.
	  description: Retorna el análisis completo en JSON. Requiere que el usuario esté autenticado.
	  parameters:
		- name: analysis_id
		  in: path
		  required: true
		  description: ID del análisis a obtener.
		  schema:
			type: integer
	  responses:
		200:
		  description: Análisis encontrado y devuelto.
		  content:
			application/json:
			  schema:
				type: object
				properties:
				  status: { type: string, example: success }
				  data: { $ref: '#/components/schemas/BiometricAnalysis' }
		403:
		  description: Sin permiso para ver este análisis.
		  content:
			application/json:
			  schema: { $ref: '#/components/schemas/GenericError' }
		404:
		  description: Análisis no encontrado.
		  content:
			application/json:
			  schema: { $ref: '#/components/schemas/GenericError' }
	"""
	analysis = BiometricAnalysis.query.get(analysis_id)

	if not analysis:
		return jsonify({"status": "error", "message": "Análisis no encontrado"}), 404

	if analysis.user_id != current_user.id and not current_user.is_admin:
		return (
			jsonify(
				{"status": "error", "message": "Sin permiso para ver este análisis"}
				),
			403,
			)

	return jsonify({"status": "success", "data": analysis.to_dict()}), 200


@api_bp.route("/history", methods = ["GET"])
@login_required
def get_history():
	"""Obtener historial de análisis del usuario
	---
	get:
	  tags: [Análisis]
	  summary: Retorna el historial de análisis biométricos del usuario autenticado.
	  description: Devuelve una lista de todos los análisis del usuario. Requiere autenticación.
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
	"""
	analyses = BiometricAnalysis.query.filter_by(user_id = current_user.id).order_by(
		BiometricAnalysis.created_at.desc()
		).all()

	return (
		jsonify(
			{
				"status": "success",
				"count": len(analyses),
				"data": [analysis.to_dict() for analysis in analyses],
				}
			),
		200,
		)


@api_bp.route("/analysis", methods = ["POST"])
@login_required
def create_analysis():
	"""Crear un nuevo análisis biométrico
	---
	post:
	  tags: [Análisis]
	  summary: Crea un nuevo registro de análisis biométrico.
	  description: Recibe datos biométricos en formato JSON. Actualmente no implementado.
	  requestBody:
		required: true
		content:
		  application/json:
			schema:
			  type: object
			  properties:
				weight: { type: number, format: float }
				height: { type: number, format: float }
				age: { type: integer }
				gender: { type: string, enum: ['male', 'female', 'other'] }
				neck: { type: number, format: float }
				waist: { type: number, format: float }
				hip: { type: number, format: float, nullable: true }
			  required: [weight, height, age, gender, neck, waist]
	  responses:
		501:
		  description: Endpoint en desarrollo.
		  content:
			application/json:
			  schema: { $ref: '#/components/schemas/GenericError' }
	"""
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
		return jsonify({"status": "error", "message": str(e)}), 500


@api_bp.route("/profile", methods = ["GET"])
@login_required
def get_profile():
	"""Obtener perfil del usuario actual
	---
	get:
	  tags: [Usuario]
	  summary: Devuelve los datos del perfil del usuario autenticado.
	  description: Requiere autenticación.
	  responses:
		200:
		  description: Perfil del usuario devuelto exitosamente.
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


# ... (Las rutas de /contact y /admin/messages no son relevantes para el agente principal,
# así que se pueden dejar sin docstrings por ahora para centrarnos en el problema)
# Si en el futuro quieres que el agente pueda usar estas funciones, deberás añadirles
# sus correspondientes docstrings YAML.

@api_bp.route("/contact", methods = ["POST"])
@login_required
def send_message():
	"""
	POST /api/v1/contact
	Enviar mensaje de contacto al entrenador
	"""
	# ... código sin cambios ...


@api_bp.route("/admin/messages", methods = ["GET"])
@login_required
def get_messages():
	"""
	GET /api/v1/admin/messages
	Ver todos los mensajes (solo admin)
	"""
	# ... código sin cambios ...


@api_bp.route("/admin/messages/<int:message_id>", methods = ["PATCH"])
@login_required
def mark_message_read(message_id):
	"""
	PATCH /api/v1/admin/messages/<id>
	Marcar mensaje como leído (solo admin)
	"""
	# ... código sin cambios ...

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

	message.mark_as_read()

	return (
		jsonify(
			{
				"status": "success",
				"message": "Mensaje marcado como leído",
				"data": message.to_dict(),
				}
			),
		200,
		)
