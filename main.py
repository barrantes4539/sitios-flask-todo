'''
 Esta clase crea una aplicación web Flask que se conecta a una base de datos 
 y define dos módulos adicionales que proporcionan funcionalidades específicas a la aplicación.
'''
import os

from flask import Flask


app = Flask(__name__)

# app.config.from_mapping(
#     SECRET_KEY = 'mikey', #Define las sesiones en nuestra aplicacion (cookie)
#     DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),
#     DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
#     DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
#     DATABASE = os.environ.get('FLASK_DATABASE'),
# )
app.config.from_mapping(
    SECRET_KEY='mikey',  # Define las sesiones en nuestra aplicacion (cookie)
    DATABASE_HOST='tiusr2pl.cuc-carrera-ti.ac.cr',
    DATABASE_PORT=3306,
    DATABASE_USER='kbarrantes',
    DATABASE_PASSWORD='sitios1234',
    DATABASE='tiusr2pl_flask',
)

#Importa la clase de db
import db

#Instancia la funcion de init proveniente de db y le pasa la app de create app como parametro
#Conecta la aplicación con la base de datos.
db.init_app(app)

import auth
import todo

'''
Se importan dos módulos adicionales (auth y todo) y se registran sus blueprints en la aplicación, 
lo que significa que se asocian a las rutas URL que definen y se hacen accesibles a través de la aplicación.
'''
app.register_blueprint(auth.bp)
app.register_blueprint(todo.bp)

if __name__ == "__main__":
    app.run(debug=True)