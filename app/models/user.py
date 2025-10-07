# app/models/user.py
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from app import db, bcrypt


class User(db.Model, UserMixin):
	"""
	Modelo principal de usuario con autenticación y roles.
	"""
	__tablename__ = 'users'

	# Identificación
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(120), unique = True, nullable = False, index = True)
	username = db.Column(db.String(80), unique = True, nullable = False, index = True)
	_password_hash = db.Column('password_hash', db.String(255), nullable = False)

	# Información personal
	first_name = db.Column(db.String(50))
	last_name = db.Column(db.String(50))
	phone = db.Column(db.String(20))
	date_of_birth = db.Column(db.Date)
	gender = db.Column(db.Enum('male', 'female', 'other', name = 'gender_types'))

	# Estado de la cuenta
	is_active = db.Column(db.Boolean, default = True, nullable = False)
	is_verified = db.Column(db.Boolean, default = False, nullable = False)
	email_verified_at = db.Column(db.DateTime)
	
	# Admin flag (quick access, complementa el sistema de roles)
	is_admin = db.Column(db.Boolean, default = False, nullable = False)

	# Rol
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	role = db.relationship('Role', back_populates = 'users')
	biometric_analyses = db.relationship(
		'BiometricAnalysis',
		back_populates = 'user',
		lazy = 'dynamic',
		cascade = 'all, delete-orphan'
		)

	# Timestamps
	created_at = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)
	updated_at = db.Column(db.DateTime, default = datetime.utcnow, onupdate = datetime.utcnow)
	last_login = db.Column(db.DateTime)

	# Tokens de recuperación
	reset_password_token = db.Column(db.String(255))
	reset_password_expires = db.Column(db.DateTime)

	# Token de verificación de email
	verification_token = db.Column(db.String(255))

	@hybrid_property
	def password(self):
		"""No permitir leer el password."""
		raise AttributeError('password no es un atributo legible')

	@password.setter
	def password(self, plaintext_password):
		"""Hashear password al asignarlo."""
		self._password_hash = bcrypt.generate_password_hash(
			plaintext_password
			).decode('utf-8')

	def check_password(self, plaintext_password):
		"""
		Verificar si el password es correcto.

		Args:
			plaintext_password: Contraseña en texto plano

		Returns:
			bool: True si coincide, False si no
		"""
		return bcrypt.check_password_hash(self._password_hash, plaintext_password)

	@property
	def full_name(self):
		"""Nombre completo del usuario."""
		if self.first_name and self.last_name:
			return f"{self.first_name} {self.last_name}"
		return self.username

	def has_role(self, role_name):
		"""Verificar si el usuario tiene un rol específico."""
		return self.role and self.role.name == role_name

	def has_permission(self, permission_name):
		"""Verificar si el usuario tiene un permiso específico."""
		return self.role and self.role.has_permission(permission_name)

	def update_last_login(self):
		"""Actualizar timestamp de último login."""
		self.last_login = datetime.utcnow()
		db.session.commit()

	def __repr__(self):
		return f'<User {self.username}>'


class Role(db.Model):
	"""Sistema de roles para control de acceso."""
	__tablename__ = 'roles'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50), unique = True, nullable = False)
	description = db.Column(db.String(255))

	# Relaciones
	users = db.relationship('User', back_populates = 'role', lazy = 'dynamic')
	permissions = db.relationship(
		'Permission',
		secondary = 'role_permissions',
		back_populates = 'roles',
		lazy = 'dynamic'
		)

	def has_permission(self, permission_name):
		"""Verificar si el rol tiene un permiso específico."""
		return self.permissions.filter_by(name = permission_name).first() is not None

	def __repr__(self):
		return f'<Role {self.name}>'


class Permission(db.Model):
	"""Permisos granulares del sistema."""
	__tablename__ = 'permissions'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50), unique = True, nullable = False)
	description = db.Column(db.String(255))

	# Relaciones
	roles = db.relationship(
		'Role',
		secondary = 'role_permissions',
		back_populates = 'permissions',
		lazy = 'dynamic'
		)

	def __repr__(self):
		return f'<Permission {self.name}>'


# Tabla de asociación para roles y permisos (muchos a muchos)
role_permissions = db.Table(
	'role_permissions',
	db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key = True),
	db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key = True)
	)
