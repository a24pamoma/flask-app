from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Empresa(db.Model):
    __tablename__ = 'empresa'
    id = db.Column(db.Integer, primary_key=True)
    cif = db.Column(db.String(64), unique=True, nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    direccion = db.Column(db.String(200))
    sector = db.Column(db.String(100))
    telefono = db.Column(db.String(50))
    email = db.Column(db.String(120))
    trabajadores = db.relationship('Trabajador', backref='empresa', cascade="all, delete-orphan", passive_deletes=True)

class Trabajador(db.Model):
    __tablename__ = 'trabajador'
    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    apellido = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    puesto = db.Column(db.String(100))
    fecha_contratacion = db.Column(db.Date, default=date.today)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id', ondelete='RESTRICT'), nullable=False)
