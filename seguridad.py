from config import conexion
from models.usuarios import Usuario
from bcrypt import checkpw

def autenticador(username, password):
    """Funcion encargada de validar si las credenciales son correctas o no, si no son no pasara 
    pero si si lo son retornara una JWT"""
    # primero valido si los parametros son correctos
    if username and password:
        # buscare el usuario en la bd
        usuarioEncontrado = conexion.session.query(
            Usuario).filter_by(correo=username).first()
        if usuarioEncontrado:
            print('se encontro el usuario')
            # ahora valido si la password es la correcta
            validacion = checkpw(bytes(password, 'utf-8'),
                                 bytes(usuarioEncontrado.password, 'utf-8'))
            if validacion is True:
                print('si es la contraseña')
                # si todas las validaciones son correctas entonces deberemos de retornar una instancia con un atributo id
                return usuarioEncontrado
            else:
                return None
        else:
            return None
    else:
        return None
def identificador(payload):
    """Sirve para validar al usuario previamente autenticado"""
    print(payload)
    usuarioEncontrado: Usuario | None = conexion.session.query(
        Usuario).filter_by(id=payload['identity']).first()
    if usuarioEncontrado:
        # esta informacion me servira para cuando quiera acceder al usuario actual de la peticion
        return usuarioEncontrado
    else:
        return None