from flask_restful import Resource, request
from models.recetas import Receta
from dtos.receta_dto import (RecetaRequestDTO, 
                                RecetaResponseDTO, 
                                BuscarRecetaRequestDTO,
                                RecetaPreparacionesResponseDTO)
from dtos.paginacion_dto import PaginacionRequestDTO
from config import conexion
from math import ceil
class RecetasController(Resource):
    def post(self):
        body = request.get_json()
        try:
            data = RecetaRequestDTO().load(body)
            nuevaReceta = Receta(
                nombre = data.get('nombre'),
                estado = data.get('estado'),
                comensales = data.get('comensales'),
                duracion = data.get('duracion'),
                dificultad = data.get('dificultad')
            )
         
            conexion.session.add(nuevaReceta)
            conexion.session.commit()
            
            respuesta = RecetaResponseDTO().dump(nuevaReceta)
            return {
                'message':'Receta exitosamente creada',
                'content': respuesta
            }, 201

        except Exception as e:
            conexion.session.rollback()
            return {
                'message':'Error al crear la receta',
                'content': e.args
            }

    def get(self):
      # TODO: agrega paginacion
      query_params = request.args
      paginacion = PaginacionRequestDTO().load(query_params)
      PerPage= paginacion.get('PerPage')
      page = paginacion.get('page')

      if(PerPage < 1 or page < 1):
          return {
              'message': 'Los parametros no aceptan valores negativos'
          }, 400

      skip = PerPage * (page - 1)

      recetas = conexion.session.query(Receta).limit(PerPage).offset(skip).all()

      total = conexion.session.query(Receta).count()
      
      itemsxpage = PerPage if total >= PerPage else total
      totalpages = ceil(total / itemsxpage) if itemsxpage > 0 else None
      PrevPage = page - 1 if page > 1 and page <= totalpages else None
      NextPage = page + 1 if totalpages > 1 and page < totalpages else None
      


      respuesta = RecetaResponseDTO(many=True).dump(recetas)

      return {
        'message':'las recetas son:',
        'paginacion': {
            'total': total,
            'itemsxpage': itemsxpage,
            'totalpages': totalpages,
            'PrevPage': PrevPage,
            'NextPage': NextPage
        },
        'content': respuesta
    }
   
class BuscarRecetaController(Resource):
    def get(self):
        query_params = request.args
        try:
            parametros = BuscarRecetaRequestDTO().load(query_params)
            print(parametros)
            recetas2= conexion.session.query(Receta).filter(Receta.nombre.like('%a%')).all()
            print(recetas2)
            nombre = parametros.get('nombre','')
            if parametros.get('nombre') is not None:
                del parametros['nombre']
            recetas = conexion.session.query(Receta).filter(Receta.nombre.like('%{}%'.format(nombre))).filter_by(**parametros).all()
            resultado = RecetaResponseDTO(many=True).dump(recetas)
            print(recetas)

            return {
            'message': '',
            'content': resultado
            }
        except Exception as e:
            return {
                'message': 'Error en la busqueda',
                'content': e.args
            }, 400

class RecetaController(Resource):
    def get(self, id):
        receta: Receta | None = conexion.session.query(Receta).filter(Receta.id == id).first()
        if receta is None:
            return {
         'message': 'Receta no encontrada'
       }, 404
  
        else:
            print(receta.preparaciones)
            respuesta = RecetaPreparacionesResponseDTO().dump(receta)
            return {
                   'message': 'Receta encontrada',
                   'content': respuesta
               }, 200









































































