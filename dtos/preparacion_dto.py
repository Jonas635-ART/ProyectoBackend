from config import validador
from models.preparaciones import Preparacion
from marshmallow import fields
from models.recetas import Receta

class PreparacionRequestDTO(validador.SQLAlchemyAutoSchema):
    class Meta:
        model = Preparacion
        include_fk = True


class RecetaResponseDTO(validador.SQLAlchemyAutoSchema):
    class Meta:
        model: Receta       

class PreparacionResponseDTO(validador.SQLAlchemyAutoSchema):


    receta = fields.Nested(nested=RecetaResponseDTO, data_key= 'receta_relacion')

    class Meta:
        model = Preparacion

        load_instance = True
        include_fk = False





        include_relationships = True























































