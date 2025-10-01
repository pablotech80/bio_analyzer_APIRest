# app/blueprints/auth/services.py
from datetime import datetime, timedelta
from secrets import token_urlsafe

from flask import current_app

from app import db
from app.models.user import User, Role


class AuthService:
	"""Servicios de lógica de negocio para autenticación."""

	@staticmethod
	def register_user(username, email, password, first_name = None, last_name = None):
		"""
		Registrar un nuevo usuario en el sistema.

		Args:
			username: Nombre de usuario único
			email: Email único
			password: Contraseña en texto plano (se hasheará)
			first_name: Nombre opcional
			last_name: Apellidos opcionales

		Returns:
			User: Usuario creado

		Raises:
			ValueError: Si el usuario o email ya existen
		"""
		# Verificar si el usuario ya existe
		if User.query.filter_by(username = username).first():
			raise ValueError('El nombre de usuario ya está en uso')

		if User.query.filter_by(email = email.lower()).first():
			raise ValueError('El email ya está registrado')

		# Obtener el rol "client" por defecto
		default_role = Role.query.filter_by(name = 'client').first()
		if not default_role:
			# Si no existe el rol, crearlo (esto debería estar en init_db)
			default_role = Role(name = 'client', description = 'Usuario cliente estándar')
			db.session.add(default_role)
			db.session.flush()

		# Crear nuevo usuario
		user = User(
			username = username,
			email = email.lower(),
			first_name = first_name,
			last_name = last_name,
			role = default_role
			)
		user.password = password  # Se hasheará automáticamente

		db.session.add(user)
		db.session.commit()

		# Generar token de verificación
		verification_token = AuthService.generate_email_verification_token(user)

		current_app.logger.info(f'Nuevo usuario registrado: {username} ({email})')
		current_app.logger.info(f'Token de verificación generado: {verification_token[:10]}...')

		return user

	@staticmethod
	def authenticate_user(email, password):
		"""
		Autenticar usuario con email y contraseña.

		Args:
			email: Email del usuario
			password: Contraseña en texto plano

		Returns:
			User: Usuario autenticado o None si falla
		"""
		user = User.query.filter_by(email = email.lower()).first()

		if not user:
			current_app.logger.warning(f'Intento de login con email no registrado: {email}')
			return None

		if not user.is_active:
			current_app.logger.warning(f'Intento de login de usuario inactivo: {email}')
			return None

		if not user.check_password(password):
			current_app.logger.warning(f'Contraseña incorrecta para usuario: {email}')
			return None

		# Actualizar último login
		user.update_last_login()

		current_app.logger.info(f'Usuario autenticado exitosamente: {email}')
		return user

	@staticmethod
	def change_password(user, old_password, new_password):
		"""
		Cambiar contraseña de un usuario.

		Args:
			user: Instancia de User
			old_password: Contraseña actual
			new_password: Nueva contraseña

		Returns:
			bool: True si se cambió exitosamente

		Raises:
			ValueError: Si la contraseña actual es incorrecta
		"""
		if not user.check_password(old_password):
			raise ValueError('La contraseña actual es incorrecta')

		user.password = new_password
		db.session.commit()

		current_app.logger.info(f'Contraseña cambiada para usuario: {user.email}')
		return True

	@staticmethod
	def generate_password_reset_token(email):
		"""
		Generar token para reseteo de contraseña.

		Args:
			email: Email del usuario

		Returns:
			tuple: (user, token) o (None, None) si no existe
		"""
		user = User.query.filter_by(email = email.lower()).first()
		if not user:
			return None, None

		# Generar token seguro
		token = token_urlsafe(32)
		user.reset_password_token = token
		user.reset_password_expires = datetime.utcnow() + timedelta(hours = 1)

		db.session.commit()

		current_app.logger.info(f'Token de reset generado para: {email}')
		return user, token

	@staticmethod
	def reset_password_with_token(token, new_password):
		"""
		Resetear contraseña usando un token.

		Args:
			token: Token de reseteo
			new_password: Nueva contraseña

		Returns:
			User: Usuario si exitoso, None si token inválido/expirado
		"""
		user = User.query.filter_by(reset_password_token = token).first()

		if not user:
			current_app.logger.warning(f'Token de reset inválido: {token[:10]}...')
			return None

		# Verificar expiración
		if user.reset_password_expires < datetime.utcnow():
			current_app.logger.warning(f'Token de reset expirado para: {user.email}')
			return None

		# Cambiar contraseña
		user.password = new_password
		user.reset_password_token = None
		user.reset_password_expires = None

		db.session.commit()

		current_app.logger.info(f'Contraseña reseteada exitosamente para: {user.email}')
		return user

	@staticmethod
	def get_user_by_id(user_id):
		"""Obtener usuario por ID."""
		return User.query.get(user_id)

	@staticmethod
	def get_user_by_email(email):
		"""Obtener usuario por email."""
		return User.query.filter_by(email = email.lower()).first()

	@staticmethod
	def deactivate_user(user):
		"""Desactivar cuenta de usuario."""
		user.is_active = False
		db.session.commit()
		current_app.logger.info(f'Usuario desactivado: {user.email}')

	@staticmethod
	def update_user_profile(
			user, username, email, first_name = None, last_name = None,
			phone = None, date_of_birth = None, gender = None
			):
		"""
		Actualizar información del perfil de usuario.

		Args:
			user: Instancia de User
			username: Nuevo username
			email: Nuevo email
			first_name: Nombre
			last_name: Apellidos
			phone: Teléfono
			date_of_birth: Fecha de nacimiento
			gender: Género

		Returns:
			User: Usuario actualizado

		Raises:
			ValueError: Si el username o email ya están en uso
		"""
		# Verificar si el nuevo username está disponible (si cambió)
		if username != user.username:
			existing_user = User.query.filter_by(username = username).first()
			if existing_user:
				raise ValueError('El nombre de usuario ya está en uso')

		# Verificar si el nuevo email está disponible (si cambió)
		if email.lower() != user.email.lower():
			existing_user = User.query.filter_by(email = email.lower()).first()
			if existing_user:
				raise ValueError('El email ya está registrado')

		# Actualizar datos
		user.username = username
		user.email = email.lower()
		user.first_name = first_name
		user.last_name = last_name
		user.phone = phone
		user.date_of_birth = date_of_birth
		user.gender = gender

		db.session.commit()

		current_app.logger.info(f'Perfil actualizado para usuario: {user.email}')
		return user

	@staticmethod
	def activate_user(user):
		"""Activar cuenta de usuario."""
		user.is_active = True
		db.session.commit()
		current_app.logger.info(f'Usuario activado: {user.email}')

	@staticmethod
	def generate_email_verification_token(user):
		"""
		Generar token para verificación de email.

		Args:
			user: Instancia de User

		Returns:
			str: Token de verificación
		"""
		from secrets import token_urlsafe

		token = token_urlsafe(32)
		user.verification_token = token
		db.session.commit()

		current_app.logger.info(f'Token de verificación generado para: {user.email}')
		return token

	@staticmethod
	def verify_email_with_token(token):
		"""
		Verificar email usando token.

		Args:
			token: Token de verificación

		Returns:
			User: Usuario si exitoso, None si token inválido
		"""
		from datetime import datetime

		user = User.query.filter_by(verification_token = token).first()

		if not user:
			current_app.logger.warning(f'Token de verificación inválido')
			return None

		# Marcar como verificado
		user.is_verified = True
		user.email_verified_at = datetime.utcnow()
		user.verification_token = None  # Limpiar el token

		db.session.commit()

		current_app.logger.info(f'Email verificado exitosamente para: {user.email}')
		return user

	@staticmethod
	def resend_verification_email(user):
		"""
		Reenviar email de verificación.

		Args:
			user: Instancia de User

		Returns:
			str: Nuevo token de verificación
		"""
		if user.is_verified:
			raise ValueError('Este email ya está verificado')

		return AuthService.generate_email_verification_token(user)
