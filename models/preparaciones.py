from config import conexion
from sqlalchemy import Column, types, orm
from sqlalchemy.sql.schema import ForeignKey

class Preparacion(conexion.Model):
    __tablename__ ='preparaciones'

    id = Column(type_=types.Integer, autoincrement= True, primary_key=True)
    descripcion = Column(type_=types.String(length=45))
    orden = Column(type_=types.Integer, nullable= False)

# relacion entre preparaciones y recetas
    receta_id = Column(ForeignKey(column='recetas.id'), type_=types.Integer)
    
    receta = orm.relationship('Receta', backref='preparaciones')
























































