
# create table ingredientes (id int primary key ....)
from config import conexion
from sqlalchemy import Column, types

class Ingrediente(conexion.Model):
   
    # https://docs.sqlalchemy.org/en/14/core/metadata.html?highlight=column#sqlalchemy.schema.Column
    # https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.String
    id = Column(type_=types.Integer, primary_key=True, autoincrement=True)
    nombre= Column(type_=types.String(length=45), nullable=False, unique=True)

    __tablename__ = 'ingredientes'