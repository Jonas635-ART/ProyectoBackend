from flask_jwt import *
from flask import Flask, request
# from flask_jwt import JWT, jwt_required, current_identity
import json
from flask_restful import Api
from controllers.ingredientes import ( IngredientesController, 
                                       PruebaController, 
                                       IngredienteController )
from controllers.recetas import ( RecetasController, 
                                  BuscarRecetaController, 
                                  RecetaController)
from controllers.preparaciones import PreparacionController
from controllers.ingredientes_recetas import IngredientesRecetasController
from controllers.usuarios import LoginController, RegistroController
from config import validador, conexion
from os import environ
from dotenv import load_dotenv
from models.usuarios import Usuario
from dtos.registro_dto import UsuarioResponseDTO
from flask_cors import CORS
from seguridad import autenticador, identificador
from datetime import timedelta
from cryptography.fernet import Fernet
from datetime import datetime


load_dotenv()


app = Flask(__name__)
# Creamos la instancia de flask_restful.Api y le indicamos que toda la configuracion que haremos se agrege a nuestra instancia de Flask
CORS(app=app)

# Si se establece True entonces SQLALCHEMY rastreara las modificaciones de los objectos (modelos) y emitira señales cuando cambie algun modelo, su valor por defecto es None
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# para jalar la configuracion de mi flask y extraer su conexion a la base de datos
app.config['SECRET_KEY'] = 'secreto'
app.config['SECRET_KEY'] = environ.get('JWT_SECRET_KEY')
# para cambiar el endpoint de mi JWT
app.config['JWT_AUTH_URL_RULE'] = '/login-jwt'
# para cambiar la llave para solicitar el username
app.config['JWT_AUTH_USERNAME_KEY'] = 'correo'
# para cambiar la llave para solicitar la password
app.config['JWT_AUTH_PASSWORD_KEY'] = 'pass'
# para cambiar el tiempo de expiracion de mi JWT
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1, minutes=5)
# Para indicar cual sera el prefijo de la token en los headers de authorization
app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'
jsonwebtoken = JWT(app=app, authentication_handler=autenticador,
                   identity_handler=identificador)
api = Api(app=app)
validador.init_app(app)
conexion.init_app(app)


@app.route('/status', methods=['GET'])
def status():
    return {
        'status': True,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

@app.route('/')
def inicio():
    return 'Bienvenido a mi API de recetas'

#Login
@app.route('/status')
def estado():
    return {
        'status': True,
        'hora_del_servidor': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }, 200
    
@app.route('/yo')
@jwt_required()
def perfil_usuario():
    print(current_identity)
    # serializar el usuario (current identity)
    usuario = UsuarioResponseDTO().dump(current_identity)
    return {
        'message': 'El usuario es',
        'content': usuario
    }
@app.route('/validar-token', methods=['POST'])
def validate_token():

    body = request.get_json()
    token = body.get('token')
    fernet = Fernet(environ.get('FERNET_SECRET_KEY'))
    try: 
      
        data = fernet.decrypt(bytes(token, 'utf-8')).decode('utf-8')
        print(data)
        diccionario = json.loads(data)
        fecha_caducidad = datetime.strptime(diccionario.get('fecha_caducidad'), '%Y-%m-%d %H:%M:%S.%f')
        hora_actual = datetime.now()
        if hora_actual < fecha_caducidad:
            print(conexion.session.query(Usuario).with_entities(Usuario.correo).filter_by(id= 
            diccionario.get('id_usuario')))
            usuarioEncontrado = conexion.session.query(Usuario).with_entities(Usuario.correo).filter_by(id= 
            diccionario.get('id_usuario')).first()
            if usuarioEncontrado:
                return {
                    'message': 'Correcto',
                    'content': {
                        'correo': usuarioEncontrado.correo
                    }  }
            else:
                return {
                            'message': 'Usuario no existe'
                        }, 400
        else:
            print('Token caduco')
        return {
            'message': 'si es el usuario'
        }, 200
    except Exception as e:
        return {
            'message': 'Token Incorrecto'
        }, 400

# Ahora definimos las rutas que van a ser utilizadas con un determinado controlador
api.add_resource(IngredientesController, '/ingredientes', '/ingrediente')
api.add_resource(PruebaController, '/pruebas')
api.add_resource(IngredienteController, '/ingrediente/<int:id>')
api.add_resource(RecetasController, '/recetas', '/receta')
api.add_resource(BuscarRecetaController, '/buscar_receta')
api.add_resource(PreparacionController, '/preparacion')
api.add_resource(RecetaController, '/receta/<int:id>')
api.add_resource(IngredientesRecetasController, '/ingrediente_receta')
api.add_resource(RegistroController, '/registro')
api.add_resource(LoginController, '/login')


# comprobara que la instancia de la clase Flask se este ejecutando en el archivo principal del proyecto, esto se usa para no crear multiples instancias y generar un posible error de Flask 
if (__name__ == '__main__'):
    app.run(debug=True)





































































