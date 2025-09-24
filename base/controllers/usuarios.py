from flask import Blueprint, request, redirect, session, flash
from flask import render_template
from werkzeug.security import generate_password_hash, check_password_hash
from base.models.usuario_model import Usuario


bp = Blueprint('usuarios', __name__)


@bp.post('/procesar_registro')
def procesar_registro():
    if not Usuario.validar_registro(request.form):
        return redirect('/')
    data = {
        'nombre': request.form['nombre'].strip(),
        'apellido': request.form['apellido'].strip(),
        'email': request.form['email'].strip().lower(),
        'password': generate_password_hash(request.form['password'])
    }
    usuario_id = Usuario.crear(data)
    session['usuario_id'] = usuario_id
    return redirect('/citas')


@bp.post('/procesar_login')
def procesar_login():
    email = (request.form.get('email') or '').strip().lower()
    password = request.form.get('password') or ''
    usuario = Usuario.obtener_por_email(email)
    if not usuario or not check_password_hash(usuario['password'], password):
        flash('Credenciales inválidas.', 'login')
        return redirect('/')
    session['usuario_id'] = usuario['id']
    return redirect('/citas')


@bp.get('/logout')
def logout():
    session.clear()
    return redirect('/')

