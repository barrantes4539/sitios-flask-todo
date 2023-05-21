'''
En general, este código se utiliza para manejar la autenticación de usuario en una aplicación web Flask.
'''
import functools #Set de funciones 
from  flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
) 
"""
#Imports de flask
Blueprints: son configurables
flash: mensajes genericos a nuestras plantillas, ej usuario incorrecto. 
g: variable generica
render_template: para renderizar plantillas
request: recibir datos desde formulario'
url_for: crearemos urls
session: mantener una referencia del usuario en el contexto actual
"""
from werkzeug.security import check_password_hash, generate_password_hash 
"""
check_password_hash: verificar si la contraseña que se ingresa es igual a otra
generate_password_hash: encriptar la contraseña
"""
from db import get_db
from mysql.connector.errors import DataError

'''
 Linea 33: Define un objeto Blueprint llamado "auth". Este objeto se utiliza para definir rutas y lógica para la 
 autenticación de usuarios en la aplicación. El parámetro url_prefix establece un prefijo para todas 
 las URL definidas en el objeto Blueprint.
'''
bp = Blueprint('auth', __name__, url_prefix='/auth') 

@bp.route('/register', methods=['GET','POST'])


def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'select id from user where username = %s', (username,)
        )
        if not username:
            error = 'Username es requerido'
        if not password:
            error = 'Password es requerido'
        elif c.fetchone() is not None:
            error = 'Usuario {} se encuentra registrado.'.format(username)

        if error is None:
            try:
                c.execute(
                    'insert into user (username, password) values (%s, %s)',
                    (username, generate_password_hash(password))
                )
                db.commit()

                return redirect(url_for('auth.login'))
            except DataError as e:
                error = e
                db.rollback()

        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'select * from user where username = %s', (username,)
        )
        user = c.fetchone()

        if user is None:
            error = 'Usuario y/o contraseña inválida'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contraseña inválida'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('todo.index'))
        
        flash(error)
    return render_template('auth/login.html')

'''
load_logger_in_user(): Se ejecuta antes de cada solicitud a la aplicación y comprueba si 
un usuario ha iniciado sesión. Si un usuario ha iniciado sesión, 
se almacena en un objeto global llamado g.user.
'''
@bp.before_app_request
def load_logger_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'select * from user where id = %s',(user_id,)
        )
        g.user = c.fetchone()

'''
 login_required() es un decorador que se puede aplicar a cualquier ruta para requerir que un usuario haya 
 iniciado sesión antes de que se le permita acceder a la página. Si un usuario no ha iniciado sesión, se le 
 redirige a la página de inicio de sesión.
'''
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    return wrapped_view

''']
logout() elimina la sesión del usuario y lo redirige a la página de inicio de sesión.
'''
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

