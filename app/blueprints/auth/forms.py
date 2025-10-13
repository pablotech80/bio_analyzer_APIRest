# app/blueprints/auth/forms.py
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
    ValidationError,
)

from app.models.user import User


class RegistrationForm(FlaskForm):
    """Formulario de registro de usuario."""

    username = StringField(
        "Nombre de usuario",
        validators=[
            DataRequired(message="El nombre de usuario es obligatorio"),
            Length(min=3, max=80, message="Debe tener entre 3 y 80 caracteres"),
        ],
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El email es obligatorio"),
            Email(message="Email inválido"),
        ],
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria"),
            Length(min=8, message="La contraseña debe tener al menos 8 caracteres"),
        ],
    )

    password_confirm = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(message="Debes confirmar la contraseña"),
            EqualTo("password", message="Las contraseñas deben coincidir"),
        ],
    )

    first_name = StringField("Nombre", validators=[Optional(), Length(max=50)])

    last_name = StringField("Apellidos", validators=[Optional(), Length(max=50)])

    submit = SubmitField("Registrarse")

    def validate_username(self, username):
        """Validar que el username no esté en uso."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Este nombre de usuario ya está en uso. Por favor elige otro."
            )

    def validate_email(self, email):
        """Validar que el email no esté registrado."""
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError(
                "Este email ya está registrado. ¿Deseas iniciar sesión?"
            )


class LoginForm(FlaskForm):
    """Formulario de inicio de sesión."""

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El email es obligatorio"),
            Email(message="Email inválido"),
        ],
    )

    password = PasswordField(
        "Contraseña", validators=[DataRequired(message="La contraseña es obligatoria")]
    )

    remember_me = BooleanField("Recordarme")

    submit = SubmitField("Iniciar Sesión")


class ChangePasswordForm(FlaskForm):
    """Formulario para cambiar contraseña."""

    old_password = PasswordField(
        "Contraseña actual",
        validators=[DataRequired(message="Ingresa tu contraseña actual")],
    )

    new_password = PasswordField(
        "Nueva contraseña",
        validators=[
            DataRequired(message="La nueva contraseña es obligatoria"),
            Length(min=8, message="La contraseña debe tener al menos 8 caracteres"),
        ],
    )

    new_password_confirm = PasswordField(
        "Confirmar nueva contraseña",
        validators=[
            DataRequired(message="Debes confirmar la nueva contraseña"),
            EqualTo("new_password", message="Las contraseñas deben coincidir"),
        ],
    )

    submit = SubmitField("Cambiar Contraseña")


class RequestPasswordResetForm(FlaskForm):
    """Formulario para solicitar reset de contraseña."""

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El email es obligatorio"),
            Email(message="Email inválido"),
        ],
    )

    submit = SubmitField("Enviar instrucciones")

    def validate_email(self, email):
        """Validar que el email exista en el sistema."""
        user = User.query.filter_by(email=email.data.lower()).first()
        if not user:
            raise ValidationError("No existe una cuenta con este email.")


class ResetPasswordForm(FlaskForm):
    """Formulario para resetear contraseña con token."""

    password = PasswordField(
        "Nueva contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria"),
            Length(min=8, message="La contraseña debe tener al menos 8 caracteres"),
        ],
    )

    password_confirm = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(message="Debes confirmar la contraseña"),
            EqualTo("password", message="Las contraseñas deben coincidir"),
        ],
    )

    submit = SubmitField("Resetear Contraseña")


class EditProfileForm(FlaskForm):
    """Formulario para editar perfil de usuario."""

    username = StringField(
        "Nombre de usuario",
        validators=[
            DataRequired(message="El nombre de usuario es obligatorio"),
            Length(min=3, max=80, message="Debe tener entre 3 y 80 caracteres"),
        ],
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El email es obligatorio"),
            Email(message="Email inválido"),
        ],
    )

    first_name = StringField("Nombre", validators=[Optional(), Length(max=50)])

    last_name = StringField("Apellidos", validators=[Optional(), Length(max=50)])

    phone = StringField("Teléfono", validators=[Optional(), Length(max=20)])

    date_of_birth = DateField(
        "Fecha de nacimiento", validators=[Optional()], format="%Y-%m-%d"
    )

    gender = SelectField(
        "Género",
        choices=[
            ("", "Seleccionar..."),
            ("male", "Masculino"),
            ("female", "Femenino"),
            ("other", "Otro"),
        ],
        validators=[Optional()],
    )

    submit = SubmitField("Guardar Cambios")

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        """Validar que el username no esté en uso (excepto el propio)."""
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "Este nombre de usuario ya está en uso. Por favor elige otro."
                )

    def validate_email(self, email):
        """Validar que el email no esté registrado (excepto el propio)."""
        if email.data.lower() != self.original_email.lower():
            user = User.query.filter_by(email=email.data.lower()).first()
            if user:
                raise ValidationError("Este email ya está registrado.")
