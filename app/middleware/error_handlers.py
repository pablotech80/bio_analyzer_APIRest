# app/middleware/error_handlers.py
from flask import render_template, jsonify, request


def register_error_handlers(app):
	"""Registrar manejadores de errores globales."""

	@app.errorhandler(404)
	def not_found_error(error):
		if request.path.startswith('/api/'):
			return jsonify({'error': 'Recurso no encontrado'}), 404
		return render_template('errors/404.html'), 404

	@app.errorhandler(403)
	def forbidden_error(error):
		if request.path.startswith('/api/'):
			return jsonify({'error': 'Acceso prohibido'}), 403
		return render_template('errors/403.html'), 403

	@app.errorhandler(500)
	def internal_error(error):
		from app import db
		db.session.rollback()
		if request.path.startswith('/api/'):
			return jsonify({'error': 'Error interno del servidor'}), 500
		return render_template('errors/500.html'), 500

	@app.errorhandler(401)
	def unauthorized_error(error):
		if request.path.startswith('/api/'):
			return jsonify({'error': 'No autorizado'}), 401
		return render_template('errors/401.html'), 401