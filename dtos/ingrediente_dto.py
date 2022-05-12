from config import validador
from models.ingredientes import Ingrediente
from marshmallow_sqlalchemy import auto_field
from marshmallow import validate
class IngredienteRequestDTO(validador.SQLAlchemyAutoSchema):
    nombre = auto_field(validate= validate.And(validate.Length(min=1), validate.Regexp("[A-Z]|[a-z]+")))
  
    class Meta:
      model = Ingrediente


class IngredienteResponseDTO(validador.SQLAlchemyAutoSchema):

    class Meta:
      model = Ingrediente




























