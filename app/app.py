from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, Empresa, Trabajador
from forms import EmpresaForm, TrabajadorForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    @app.before_request
    def _enable_sqlite_fk():
        """Activa claves foráneas en SQLite para cada petición."""
        if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
            db.session.execute(text("PRAGMA foreign_keys = ON"))

    @app.route('/')
    def menu():
        empresas = Empresa.query.all()
        trabajadores = Trabajador.query.all()
        return render_template("index.html", empresas=empresas, trabajadores=trabajadores)


    # ------------------- EMPRESAS -------------------
    @app.route('/empresas')
    def empresas_list():
        empresas = Empresa.query.all()
        return render_template('empresas_list.html', empresas=empresas)

    @app.route('/empresa/<int:id>')
    def empresa_detail(id):
        e = Empresa.query.get_or_404(id)
        return render_template('empresa_detail.html', empresa=e)

    @app.route('/empresa/create', methods=['GET','POST'])
    def empresa_create():
        form = EmpresaForm()
        if form.validate_on_submit():
            e = Empresa(
                cif=form.cif.data,
                nombre=form.nombre.data,
                direccion=form.direccion.data,
                sector=form.sector.data,
                telefono=form.telefono.data,
                email=form.email.data
            )
            db.session.add(e)
            try:
                db.session.commit()
                flash("Empresa creada", "success")
                return redirect(url_for('empresas_list'))
            except IntegrityError:
                db.session.rollback()
                flash("CIF duplicado", "danger")
        return render_template('empresa_form.html', form=form, action="Crear")

    @app.route('/empresa/<int:id>/edit', methods=['GET','POST'])
    def empresa_edit(id):
        e = Empresa.query.get_or_404(id)
        form = EmpresaForm(obj=e)
        if form.validate_on_submit():
            e.cif = form.cif.data
            e.nombre = form.nombre.data
            e.direccion = form.direccion.data
            e.sector = form.sector.data
            e.telefono = form.telefono.data
            e.email = form.email.data
            try:
                db.session.commit()
                flash("Empresa modificada", "success")
                return redirect(url_for('empresas_list', id=id))
            except IntegrityError:
                db.session.rollback()
                flash("CIF duplicado", "danger")
        return render_template('empresa_form.html', form=form, action="Editar")

    @app.route('/empresa/<int:id>/delete', methods=['POST'])
    def empresa_delete(id):
        e = Empresa.query.get_or_404(id)
        if e.trabajadores:
            flash("No se puede eliminar, tiene trabajadores asociados", "danger")
            return redirect(url_for('empresa_detail', id=id))
        db.session.delete(e)
        db.session.commit()
        flash("Empresa eliminada", "success")
        return redirect(url_for('empresas_list'))

    # ------------------- TRABAJADORES -------------------
    @app.route('/trabajadores')
    def trabajadores_list():
        trabajadores = Trabajador.query.all()
        return render_template('trabajadores_list.html', trabajadores=trabajadores)

    @app.route('/trabajador/<int:id>')
    def trabajador_detail(id):
        t = Trabajador.query.get_or_404(id)
        return render_template('trabajador_detail.html', t=t)

    @app.route('/trabajador/create', methods=['GET','POST'])
    def trabajador_create():
        form = TrabajadorForm()
        form.empresa_id.choices = [(e.id, e.nombre) for e in Empresa.query.all()]
        if form.validate_on_submit():
            t = Trabajador(
                dni=form.dni.data,
                nombre=form.nombre.data,
                apellido=form.apellido.data,
                email=form.email.data,
                puesto=form.puesto.data,
                fecha_contratacion=form.fecha_contratacion.data,
                empresa_id=form.empresa_id.data
            )
            db.session.add(t)
            try:
                db.session.commit()
                flash("Trabajador creado", "success")
                return redirect(url_for('trabajadores_list'))
            except IntegrityError:
                db.session.rollback()
                flash("DNI duplicado", "danger")
        return render_template('trabajador_form.html', form=form, action="Crear")

    @app.route('/trabajador/<int:id>/edit', methods=['GET','POST'])
    def trabajador_edit(id):
        t = Trabajador.query.get_or_404(id)
        form = TrabajadorForm(obj=t)
        form.empresa_id.choices = [(e.id, e.nombre) for e in Empresa.query.all()]
        if form.validate_on_submit():
            t.dni = form.dni.data
            t.nombre = form.nombre.data
            t.apellido = form.apellido.data
            t.email = form.email.data
            t.puesto = form.puesto.data
            t.fecha_contratacion = form.fecha_contratacion.data
            t.empresa_id = form.empresa_id.data
            db.session.commit()
            flash("Trabajador modificado", "success")
            return redirect(url_for('trabajadores_list', id=id))
        return render_template('trabajador_form.html', form=form, action="Editar")

    @app.route('/trabajador/<int:id>/delete', methods=['POST'])
    def trabajador_delete(id):
        t = Trabajador.query.get_or_404(id)
        db.session.delete(t)
        db.session.commit()
        flash("Trabajador eliminado", "success")
        return redirect(url_for('trabajadores_list'))

    with app.app_context():
        if not os.path.exists('/sqlite3-db/app.db'):
            db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
