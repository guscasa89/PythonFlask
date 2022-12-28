from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    nro_socio = IntegerField('Numero de socio', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    password2= PasswordField('Repita su Contraseña', validators=[DataRequired(),EqualTo('password', 'Las contraseñas no coinciden')])
    submit = SubmitField('Registro')