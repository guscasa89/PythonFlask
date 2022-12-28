from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo


class AdministrarForm(FlaskForm):
    nro_lista = IntegerField('Numero de Lista', validators=[DataRequired()])
    presidente = StringField('Presidente', validators=[DataRequired()])
    vicepresidente = StringField('Vicepresidente', validators=[DataRequired()])
    submit = SubmitField('Ingresar Lista')