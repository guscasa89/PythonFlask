from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class VotarForm(FlaskForm):
    listas = SelectField('Opciones', validators=[DataRequired()])
    submit = SubmitField('Votar!')