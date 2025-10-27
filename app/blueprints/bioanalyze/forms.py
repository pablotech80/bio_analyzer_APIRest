from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, TextAreaField, BooleanField, FileField, FieldList
from wtforms.validators import DataRequired, Optional

class BioAnalyzeForm(FlaskForm):

    # Datos básicos
    name = StringField('Nombre completo', validators=[Optional()])
    first_name = StringField('Nombre', validators=[Optional()])
    username = StringField('Usuario', validators=[Optional()])
    age = IntegerField('Edad', validators=[DataRequired()])
    gender = SelectField('Género', choices=[('male', 'Hombre'), ('female', 'Mujer'), ('other', 'Otro')], validators=[DataRequired()])
    weight = FloatField('Peso (kg)', validators=[DataRequired()])
    height = FloatField('Altura (cm)', validators=[DataRequired()])
    goal = SelectField('Objetivo', choices=[('weight_loss', 'Pérdida de grasa'), ('muscle_gain', 'Ganancia muscular'), ('maintenance', 'Mantenimiento')], validators=[DataRequired()])
    activity_level = SelectField('Nivel de actividad', choices=[('sedentary', 'Sedentario'), ('lightly_active', 'Ligero'), ('moderately_active', 'Moderado'), ('very_active', 'Alto'), ('extra_active', 'Extra')], validators=[DataRequired()])

    # Medidas corporales
    neck = FloatField('Cuello (cm)', validators=[Optional()])
    waist = FloatField('Cintura (cm)', validators=[Optional()])
    hip = FloatField('Cadera (cm)', validators=[Optional()])
    biceps_left = FloatField('Bíceps izquierdo (cm)', validators=[Optional()])
    biceps_right = FloatField('Bíceps derecho (cm)', validators=[Optional()])
    thigh_left = FloatField('Muslo izquierdo (cm)', validators=[Optional()])
    thigh_right = FloatField('Muslo derecho (cm)', validators=[Optional()])
    calf_left = FloatField('Gemelo izquierdo (cm)', validators=[Optional()])
    calf_right = FloatField('Gemelo derecho (cm)', validators=[Optional()])

    # Contexto personal
    day_description = TextAreaField('Describe tu día a día', validators=[Optional()])
    training_time = StringField('Horario y tiempo disponible para entrenar', validators=[Optional()])
    training_preferences = StringField('Preferencias de entrenamiento', validators=[Optional()])
    fitness_experience = StringField('Experiencia previa en fitness/deporte', validators=[Optional()])
    limitations = TextAreaField('Lesiones, limitaciones físicas o enfermedades', validators=[Optional()])
    motivations = TextAreaField('Motivaciones y objetivos personales', validators=[Optional()])
    diet_adherence = SelectField('Adherencia previa a dietas/rutinas', choices=[('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta')], validators=[Optional()])
    food_preferences = TextAreaField('Gustos y aversiones alimentarias', validators=[Optional()])
    supplements = TextAreaField('Suplementos actuales o pasados', validators=[Optional()])
    medication = TextAreaField('¿Tomas algún tipo de medicación actualmente?', validators=[Optional()])
    social_support = SelectField('Apoyo social', choices=[('familiar', 'Familiar'), ('amigos', 'Amigos'), ('entrenador', 'Entrenador'), ('ninguno', 'Ninguno')], validators=[Optional()])
    stress_level = IntegerField('Nivel de estrés (1-10)', validators=[Optional()])
    sleep_quality = StringField('Calidad de sueño', validators=[Optional()])
    role = SelectField('Rol', choices=[('client', 'Cliente'), ('trainer', 'Entrenador'), ('nutritionist', 'Nutricionista')], validators=[Optional()])

    # Fotos de progreso
    front_photo = FileField('Foto frontal (cuerpo entero)', validators=[Optional()])
    side_photo = FileField('Foto lateral (cuerpo entero)', validators=[Optional()])
    back_photo = FileField('Foto de espaldas (cuerpo entero)', validators=[Optional()])
    # Historial y notas
    notes = TextAreaField('Notas adicionales', validators=[Optional()])
