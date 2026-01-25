from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Optional, Length, Email

class EmpresaForm(FlaskForm):
    cif = StringField('CIF', validators=[DataRequired(), Length(max=64)])
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=120)])
    direccion = StringField('Dirección', validators=[Optional(), Length(max=200)])
    sector = StringField('Sector', validators=[Optional(), Length(max=100)])
    telefono = StringField('Teléfono', validators=[Optional(), Length(max=50)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    submit = SubmitField('Guardar')

class TrabajadorForm(FlaskForm):
    dni = StringField('DNI', validators=[DataRequired(), Length(max=20)])
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=120)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    puesto = StringField('Puesto', validators=[Optional(), Length(max=100)])
    fecha_contratacion = DateField('Fecha de contratación', validators=[Optional()])
    empresa_id = SelectField('Empresa', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')
