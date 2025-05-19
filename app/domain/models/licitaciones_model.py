from sqlalchemy import Column, Integer, String
from .base import Base  # ✅ Importamos solo `Base`

class Licitacion(Base):
    __tablename__ = "licitaciones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
