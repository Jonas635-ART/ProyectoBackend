from flask import Flask
from flask_jwt import JWT, jwt_required,current_identity
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
from dtos.registro_dto import UsuarioResponseDTO
from config import validador, conexion
from os import environ
from dotenv import load_dotenv
from flask_cors import CORS
from seguridad import autenticador, identificador
from datetime import datetime, timedelta


load_dotenv()


app = Flask(__name__)
# Creamos la instancia de flask_restful.Api y le indicamos que toda la configuracion que haremos se agrege a nuestra instancia de Flask
CORS(app=app)

app.config['SECRET_KEY'] = 'secreto'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['JWT_AUTH_URL_RULE'] = '/login-jwt'
app.config['JWT_AUTH_USERNAME_KEY'] = 'correo'
app.config['JWT_AUTH_PASSWORD_KEY'] = 'pass'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1, minutes=5)
app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'

jsonwebtoken = JWT(app=app, authentication_handler=autenticador, identity_handler=identificador)

api = Api(app=app)
validador.init_app(app)
conexion.init_app(app)

conexion.create_all(app=app)


@app.route('/status', methods=['GET'])
def status():
    return {
        'status': True,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

@app.route('/')
def inicio():
    return 'Bienvenido a mi API de recetas'

@app.route('/yo')
@jwt_required()
def perfil_usuario():
    print(current_identity)
    usuario = UsuarioResponseDTO().dump(current_identity)
    return {
        'message': 'El usuario es'
    }

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





































































