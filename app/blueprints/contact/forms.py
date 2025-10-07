# app/blueprints/contact/forms.py
"""
Formularios para sistema de contacto
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class ContactForm(FlaskForm):
    """Formulario de contacto con el entrenador"""
    
    subject = StringField(
        'Asunto',
        validators=[
            DataRequired(message='El asunto es obligatorio'),
            Length(min=5, max=200, message='El asunto debe tener entre 5 y 200 caracteres')
        ]
    )
    
    message = TextAreaField(
        'Mensaje',
        validators=[
            DataRequired(message='El mensaje es obligatorio'),
            Length(min=10, max=2000, message='El mensaje debe tener entre 10 y 2000 caracteres')
        ]
    )
    
    analysis_id = SelectField(
        'Análisis relacionado',
        coerce=int,
        choices=[],  # Se llenará dinámicamente
        validators=[]
    )
    
    submit = SubmitField('Enviar Mensaje')
