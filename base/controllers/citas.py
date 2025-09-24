from base.models.citas_model import Cita
from base.models.usuario_model import Usuario
from flask import *

bp = Blueprint('/citas', methods = ['GET', 'POST'])
#Ruta para agregar una nueva cita, solo los usuarios autenticados pueden acceder
#Valida la cita y muestra si es necesario.
def agregar_cita():
    if 'usuario_id' not in session:
        return redirect('/')
    if not Cita.validar_cita(request.form):
        return redirect('/citas')
    data = {
        'cita' : request.form['cita'],
        'usuario_id' : session['usuario_id']
    }
    Cita.guardar_cita(data)
    return redirect('/citas')

@bp.route('/editar/<int:cita_id>')
def editar_cita(cita_id):
    #ruta para mostrar el formulario de edicion de una cita. Como validacion adicional, verifica que el usuario autenticado sea el unico que pueda editar la cita.
    if 'usuario_id' not in session:
        return redirect('/')
    cita = Cita.obtener_por_id({'id': cita_id})
    if not cita or cita.usuario_id != session['usuario_id']:
        flash("No tienes permiso para editar esta cita.", 'error')
        return redirect('/citas')
    return render_template('editar_cita.html')

@bp.route('/editar/<int:cita_id>', methods=['POST'])
def procesar_edicion(cita_id):
    #Procesa la edicion de una cita, validando que el usuario autenticado sea el unico que pueda editar la cita.
    #Solamente los usuarios autenticados pueden acceder.