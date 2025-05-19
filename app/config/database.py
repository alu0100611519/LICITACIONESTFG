from app.domain.models.base import Base, engine
import app.domain.models.licitaciones_model 

def init_db():
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas correctamente.")
