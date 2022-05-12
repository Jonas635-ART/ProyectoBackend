from config import validador
from models.preparaciones import Preparacion
from models.recetas import Receta
from marshmallow import fields, validate


class RecetaRequestDTO(validador.SQLAlchemyAutoSchema):
    class Meta:
        model = Receta
         
class RecetaResponseDTO(validador.SQLAlchemyAutoSchema):
    class Meta:
        model = Receta

class BuscarRecetaRequestDTO(validador.Schema):
    nombre = fields.String(required=False)
    estado = fields.Boolean(required=False)
    comensales = fields.Integer(required=False)
    dificultad = fields.String(required=False, validate=validate.OneOf(choices=['FACIL', 'INTERMEDIO', 
    'DIFICIL', 'EXTREMO']))


class PreparacionResponseDTO(validador.SQLAlchemyAutoSchema):
    class Meta:
        model = Preparacion

class RecetaPreparacionesResponseDTO(validador.SQLAlchemyAutoSchema):
    preparaciones = fields.Nested(nested=PreparacionResponseDTO, many=True, only=['descripcion', 'orden'])
    class Meta:
        model = Receta


































