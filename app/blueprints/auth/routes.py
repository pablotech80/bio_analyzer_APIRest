# app/blueprints/auth/routes.py
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required

from app.blueprints.auth import auth_bp
from app.blueprints.auth.forms import (
	RegistrationForm, LoginForm, ChangePasswordForm,
	RequestPasswordResetForm, ResetPasswordForm,
	)
from app.blueprints.auth.services import AuthService


@auth_bp.route('/register', methods = ['GET', 'POST'])
def register():
	"""Página de registro de usuarios."""

	# Si ya está autenticado, redirigir al dashboard
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = RegistrationForm()

	if form.validate_on_submit():
		try:
			# Registrar usuario
			user = AuthService.register_user(
				username = form.username.data,
				email = form.email.data,
				password = form.password.data,
				first_name = form.first_name.data,
				last_name = form.last_name.data
				)

			# Generar link de verificación (el token ya se generó en register_user)
			from app.models.user import User
			user_updated = User.query.get(user.id)  # Recargar para obtener el token
			verify_url = url_for('auth.verify_email', token = user_updated.verification_token, _external = True)

			flash(
				f'¡Bienvenido {user.username}! Tu cuenta ha sido creada exitosamente. '
				f'Por favor verifica tu email. (Demo: {verify_url})',
				'success'
				)

			# Auto-login después del registro
			login_user(user)

			# Redirigir a donde intentaba ir o al index
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('index'))

		except ValueError as e:
			flash(str(e), 'danger')
		except Exception as e:
			flash('Ocurrió un error al crear la cuenta. Por favor intenta nuevamente.', 'danger')

	return render_template('auth/register.html', form = form)


@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
	"""Página de inicio de sesión."""

	# Si ya está autenticado, redirigir al dashboard
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = LoginForm()

	if form.validate_on_submit():
		# Autenticar usuario
		user = AuthService.authenticate_user(
			email = form.email.data,
			password = form.password.data
			)

		if user:
			# Login exitoso
			login_user(user, remember = form.remember_me.data)

			flash(f'¡Bienvenido de vuelta, {user.username}!', 'success')

			# Redirigir a donde intentaba ir o al index
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('index'))
		else:
			flash('Email o contraseña incorrectos. Por favor intenta nuevamente.', 'danger')

	return render_template('auth/login.html', form = form)


@auth_bp.route('/logout')
@login_required
def logout():
	"""Cerrar sesión del usuario."""
	logout_user()
	flash('Has cerrado sesión exitosamente.', 'info')
	return redirect(url_for('auth.login'))


@auth_bp.route('/profile')
@login_required
def profile():
	"""Página de perfil del usuario."""
	return render_template('auth/profile.html', user = current_user)


@auth_bp.route('/edit-profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
	"""Editar perfil del usuario autenticado."""
	from app.blueprints.auth.forms import EditProfileForm

	form = EditProfileForm(
		original_username = current_user.username,
		original_email = current_user.email
		)

	if form.validate_on_submit():
		try:
			AuthService.update_user_profile(
				user = current_user,
				username = form.username.data,
				email = form.email.data,
				first_name = form.first_name.data,
				last_name = form.last_name.data,
				phone = form.phone.data,
				date_of_birth = form.date_of_birth.data,
				gender = form.gender.data if form.gender.data else None
				)
			flash('Tu perfil ha sido actualizado exitosamente.', 'success')
			return redirect(url_for('auth.profile'))
		except ValueError as e:
			flash(str(e), 'danger')

	# Pre-llenar el formulario con los datos actuales
	if request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
		form.first_name.data = current_user.first_name
		form.last_name.data = current_user.last_name
		form.phone.data = current_user.phone
		form.date_of_birth.data = current_user.date_of_birth
		form.gender.data = current_user.gender

	return render_template('auth/edit_profile.html', form = form)


@auth_bp.route('/change-password', methods = ['GET', 'POST'])
@login_required
def change_password():
	"""Cambiar contraseña del usuario autenticado."""
	form = ChangePasswordForm()

	if form.validate_on_submit():
		try:
			AuthService.change_password(
				user = current_user,
				old_password = form.old_password.data,
				new_password = form.new_password.data
				)
			flash('Tu contraseña ha sido cambiada exitosamente.', 'success')
			return redirect(url_for('auth.profile'))
		except ValueError as e:
			flash(str(e), 'danger')

	return render_template('auth/change_password.html', form = form)


@auth_bp.route('/forgot-password', methods = ['GET', 'POST'])
def forgot_password():
	"""Solicitar reseteo de contraseña."""

	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = RequestPasswordResetForm()

	if form.validate_on_submit():
		user, token = AuthService.generate_password_reset_token(form.email.data)

		if user:
			# TODO: Enviar email con el token
			# Por ahora solo mostramos el link (en producción esto sería un email)
			reset_url = url_for('auth.reset_password', token = token, _external = True)

			flash(
				f'Se han enviado instrucciones a {form.email.data} para resetear tu contraseña. '
				f'(Demo: {reset_url})',
				'info'
				)
		else:
			# Por seguridad, mostramos el mismo mensaje aunque el email no exista
			flash(
				f'Si {form.email.data} está registrado, recibirás un email con instrucciones.',
				'info'
				)

		return redirect(url_for('auth.login'))

	return render_template('auth/forgot_password.html', form = form)


@auth_bp.route('/reset-password/<token>', methods = ['GET', 'POST'])
def reset_password(token):
	"""Resetear contraseña con token."""

	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = ResetPasswordForm()

	if form.validate_on_submit():
		user = AuthService.reset_password_with_token(
			token = token,
			new_password = form.password.data
			)

		if user:
			flash('Tu contraseña ha sido reseteada exitosamente. Ya puedes iniciar sesión.', 'success')
			return redirect(url_for('auth.login'))
		else:
			flash('El link de reseteo es inválido o ha expirado. Solicita uno nuevo.', 'danger')
			return redirect(url_for('auth.forgot_password'))

	return render_template('auth/reset_password.html', form = form, token = token)


# ============================================================
# API ENDPOINTS (JSON) - Para consumo desde frontend React/Vue
# ============================================================

@auth_bp.route('/api/register', methods = ['POST'])
def api_register():
	"""API: Registrar usuario (retorna JSON)."""
	data = request.get_json()

	try:
		user = AuthService.register_user(
			username = data.get('username'),
			email = data.get('email'),
			password = data.get('password'),
			first_name = data.get('first_name'),
			last_name = data.get('last_name')
			)

		return jsonify(
			{
				'success': True,
				'message': 'Usuario registrado exitosamente',
				'user': {
					'id': user.id,
					'username': user.username,
					'email': user.email,
					'full_name': user.full_name
					}
				}
			), 201

	except ValueError as e:
		return jsonify({'success': False, 'error': str(e)}), 400
	except Exception as e:
		return jsonify({'success': False, 'error': 'Error al registrar usuario'}), 500


@auth_bp.route('/api/login', methods = ['POST'])
def api_login():
	"""API: Iniciar sesión (retorna JSON + JWT)."""
	from flask_jwt_extended import create_access_token, create_refresh_token

	data = request.get_json()

	user = AuthService.authenticate_user(
		email = data.get('email'),
		password = data.get('password')
		)

	if not user:
		return jsonify(
			{
				'success': False,
				'error': 'Email o contraseña incorrectos'
				}
			), 401

	# Crear tokens JWT
	access_token = create_access_token(identity = user.id)
	refresh_token = create_refresh_token(identity = user.id)

	return jsonify(
		{
			'success': True,
			'message': 'Login exitoso',
			'access_token': access_token,
			'refresh_token': refresh_token,
			'user': {
				'id': user.id,
				'username': user.username,
				'email': user.email,
				'full_name': user.full_name,
				'role': user.role.name if user.role else None
				}
			}
		), 200


@auth_bp.route('/api/me', methods = ['GET'])
@login_required
def api_me():
	"""API: Obtener usuario actual."""
	return jsonify(
		{
			'id': current_user.id,
			'username': current_user.username,
			'email': current_user.email,
			'full_name': current_user.full_name,
			'role': current_user.role.name if current_user.role else None,
			'is_verified': current_user.is_verified,
			'created_at': current_user.created_at.isoformat() if current_user.created_at else None,
			'last_login': current_user.last_login.isoformat() if current_user.last_login else None
			}
		), 200


@auth_bp.route('/verify-email/<token>')
def verify_email(token):
	"""Verificar email con token."""
	user = AuthService.verify_email_with_token(token)

	if user:
		flash('¡Tu email ha sido verificado exitosamente!', 'success')

		# Si el usuario no está logueado, loguearlo automáticamente
		if not current_user.is_authenticated:
			login_user(user)
	else:
		flash('El link de verificación es inválido o ha expirado.', 'danger')

	return redirect(url_for('auth.profile') if current_user.is_authenticated else url_for('auth.login'))


@auth_bp.route('/resend-verification', methods = ['POST'])
@login_required
def resend_verification():
	"""Reenviar email de verificación."""
	try:
		token = AuthService.resend_verification_email(current_user)
		verify_url = url_for('auth.verify_email', token = token, _external = True)

		flash(
			f'Se ha generado un nuevo link de verificación. '
			f'(Demo: {verify_url})',
			'info'
			)
	except ValueError as e:
		flash(str(e), 'warning')

	return redirect(url_for('auth.profile'))
