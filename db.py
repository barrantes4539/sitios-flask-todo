import mysql.connector
import click #herramienta para poder ejecutar comandos en cmd para conexion a bd
from flask import current_app, g #current_app: mantiene la aplicacion que estamos ejecutando y g: se le pueden asignar variables para despues accederlas desde otra parte de la aplicacion
from flask.cli import with_appcontext # with_appcontext: contexto de la configuracion de la aplicacion, se pueden acceder a las variables de configuracion de la aplicacion como el host de la base de datos, su usuario y password
from schema import instructions #contendra todos los scripts necesarios para crear la base de datos

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c  # Returns the connection string and cursor

    # if 'db' not in g:
    #     g.db = mysql.connector.connect(
    #         host=current_app.config['DATABASE_HOST'],
    #         user=current_app.config['DATABASE_USER'],
    #         password=current_app.config['DATABASE_PASSWORD'],
    #         database=current_app.config['DATABASE']
    #     )
    #     g.c = g.db.cursor(dictionary=True)
    # return g.db, g.c #Devuelve el string de conexion y el cursor

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db, c = get_db()
    for i in instructions:
        c.execute(i)
    db.commit()

@click.command('init-db') #este comando se podra utilizar en la terminal para ejecutar la base de datos
@with_appcontext #indica que utiliza el contexto de la aplicacion para que pueda acceder a las variables de DATABASE_HOST, DATABASE_USER, ETC
def init_db_command():
    init_db()
    click.echo('Base de datos inicializada')

def init_app(app):
    app.teardown_appcontext(close_db) #Cierra la conexion a la base de datos cada vez que se termine de realizar una peticion a la base de datos
    app.cli.add_command(init_db_command) #Suscribe init_db_command a nuestra aplicacion


