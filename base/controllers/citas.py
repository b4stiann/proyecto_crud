from flask import Blueprint, render_template, request, redirect, session, flash
from base.models.citas_model import Cita
from base.models.usuario_model import Usuario


bp = Blueprint('citas', __name__)


@bp.get('/')
def dashboard():
    if not session.get('usuario_id'):
        return redirect('/')
    usuario = Usuario.obtener_por_id(session['usuario_id'])
    citas = Cita.obtener_todas()
    favoritos = Cita.obtener_favoritos_de_usuario(session['usuario_id'])
    favoritos_ids = {c['id'] for c in favoritos}
    # Excluir de la lista principal las citas ya marcadas como favoritas (requisito cinturón negro)
    citas_no_favoritas = [c for c in citas if c['id'] not in favoritos_ids]
    return render_template(
        'dashboard.html',
        usuario=usuario,
        citas=citas_no_favoritas,
        favoritos=favoritos,
        favoritos_ids=favoritos_ids,
    )


@bp.post('/agregar')
def agregar_cita():
    if not session.get('usuario_id'):
        return redirect('/')
    if not Cita.validar_cita(request.form):
        return redirect('/citas')
    data = {
        'cita': request.form['cita'].strip(),
        'autor': request.form['autor'].strip(),
        'usuario_id': session['usuario_id'],
    }
    Cita.crear(data)
    return redirect('/citas')


@bp.get('/editar/<int:cita_id>')
def editar_cita(cita_id: int):
    if not session.get('usuario_id'):
        return redirect('/')
    cita = Cita.obtener_por_id(cita_id)
    if not cita or cita['usuario_id'] != session['usuario_id']:
        flash('No tienes permiso para editar esta cita.', 'cita')
        return redirect('/citas')
    return render_template('edita_cita.html', cita=cita)


@bp.post('/editar/<int:cita_id>')
def procesar_edicion(cita_id: int):
    if not session.get('usuario_id'):
        return redirect('/')
    cita = Cita.obtener_por_id(cita_id)
    if not cita or cita['usuario_id'] != session['usuario_id']:
        flash('No tienes permiso para editar esta cita.', 'cita')
        return redirect('/citas')
    if not Cita.validar_cita(request.form):
        return redirect(f'/citas/editar/{cita_id}')
    Cita.actualizar({'id': cita_id, 'cita': request.form['cita'].strip(), 'autor': request.form['autor'].strip()})
    return redirect('/citas')


@bp.get('/borrar/<int:cita_id>')
def borrar_cita(cita_id: int):
    if not session.get('usuario_id'):
        return redirect('/')
    cita = Cita.obtener_por_id(cita_id)
    if not cita or cita['usuario_id'] != session['usuario_id']:
        flash('No tienes permiso para borrar esta cita.', 'cita')
        return redirect('/citas')
    Cita.borrar(cita_id)
    return redirect('/citas')


@bp.get('/agregar_favorito/<int:cita_id>')
def agregar_favorito(cita_id: int):
    if not session.get('usuario_id'):
        return redirect('/')
    Cita.agregar_favorito(session['usuario_id'], cita_id)
    return redirect('/citas')


@bp.get('/remover_favorito/<int:cita_id>')
def remover_favorito(cita_id: int):
    if not session.get('usuario_id'):
        return redirect('/')
    Cita.quitar_favorito(session['usuario_id'], cita_id)
    return redirect('/citas')


@bp.get('/perfil')
def perfil():
    if not session.get('usuario_id'):
        return redirect('/')
    usuario = Usuario.obtener_por_id(session['usuario_id'])
    citas = Cita.obtener_por_usuario(session['usuario_id'])
    total_citas = len(citas)
    return render_template('perfil.html', usuario=usuario, citas=citas, total_citas=total_citas)
