import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("MYSQL_HOST")
DB_PORT = os.getenv("MYSQL_PORT")
DB_NAME = os.getenv("MYSQL_DATABASE")

#DB_HOST = "localhost" si estoy en mi máquina fuera de docker.
#DATABASE_URL = "mysql+pymysql://api_user:api_password@localhost:3307/api_security"
#Caso 1: FastAPI en tu PC

#Caso 2: FastAPI dentro de Docker
#DATABASE_URL = "mysql+pymysql://api_user:api_password@mysql:3306/api_security"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
"""
Se usa para conectar con la base de datos en:
SQLAlchemy (ORM)
FastAPI
Scripts Python

mysql+pymysql://
mysql → tipo de base de datos
pymysql → driver que usa Python para conectarse
"""

"""
{DB_USER}:{DB_PASSWORD}
Usuario de la base de datos
Contraseña
Ejemplo: api_user:api_password
"""

"""
{DB_HOST}:{DB_PORT}
Dónde está la base de datos
Ejemplo: localhost:3307
    o en Docker: mysql:3306
"""

"""
/{DB_NAME}
Nombre de la base de datos
Ejemplo: /api_security
"""

# Esto crea el motor de conexión a la base de datos.
# el objeto que sabe:
# cómo conectarse a la DB
# qué tipo de DB es (MySQL en tu caso)
# cómo gestionar conexiones

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  #Buenas prácticas: Antes de usar una conexión, comprueba que sigue viva
)

# Esto crea una fábrica de sesiones de base de datos: abrir conexiones a la bd.
#Una session es: una conexión activa con la base de datos para: 
# hacer consultas (SELECT)
# insertar datos (INSERT)
# actualizar (UPDATE)
# borrar (DELETE)

#sessionmaker: Es una función de SQLAlchemy que crea un generador de sesiones.
SessionLocal = sessionmaker(
    autocommit=False,  #los cambios no se guaradn automáticamente. db.commit()
    autoflush=False,   #Evita que SQLAlchemy envíe cambios automáticamente antes de una consulta.
    bind=engine        #usa esta conexión a la base de datos. (ese engine viene de tu DATABASE_URL)
)

Base = declarative_base() #Es la base de la que van a heredar todos tus modelos de base de datos.
                          #Esto define la estructura base para crear tablas en Python
                          #Cuando trabajas con SQLAlchemy, no escribes solo SQL, sino que defines clases Python que representan tablas
                          #Y todas esas clases necesitan una base común → Base.
#Base.metadata.create_all(bind=engine) #Esto crea todas las tablas automáticamente en la DB

"""Esto crea:
el motor de conexión
el gestor de sesiones
la base para los modelos
"""