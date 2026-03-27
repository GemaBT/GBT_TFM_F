#from database import SessionLocal
from api.database import SessionLocal
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal() #Abre una conexión a la base de datos
                        # Es como decir: “quiero empezar a trabajar con la DB”
    try:
        yield db        #Entrega esa conexión al endpoint
                        #FastAPI hace magia aquí: pausa la función usa db en el endpoint 
                        #y cuando termina → vuelve aquí

    finally:
        db.close()      # 
