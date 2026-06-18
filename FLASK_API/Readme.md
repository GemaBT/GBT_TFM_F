# (virtualenv) Preparación del entorno de trabajo.

Creación de un entorno virtual es un “Python aislado” para proyecto FastAPI. => No mezclar dependencias entre proyectos, evitar conflictos de versiones, tener un entorno reproducible...

**Crear entorno virtual**. Windows:

```bash
python -m venv venv
```

Esto crea una carpeta:

```
FASTAPI/
 ├── venv/
```

**Activar el entorno virtual**


```bash
venv\Scripts\activate
```
Dentro del entorno virtual

```bash
(venv) user@pc:security_api$
```
---

**Instalar FastAPI y DRF dentro del entorno**. Siempre con el entorno activado

```bash
pip install fastapi
pip install uvicorn
pip install sqlalchemy
pip install pymysql
pip install python-jose[cryptography]
pip install passlib[bcrypt]
pip install python-multipart
pip install pydantic-settings
pip install fastapi-cors
```
```bash
pip install fastapi uvicorn sqlalchemy pymysql python-jose[cryptography] passlib[bcrypt] python-multipart pydantic-settings fastapi-cors
```
---

**Guardar dependencias**. Reproducir el proyecto.

```bash
pip freeze > requirements.txt
```

En **FastAPI** no existe un comando equivalente a:

```bash
django-admin startproject security_api .
```

FastAPI no genera automáticamente toda la estructura del proyecto como Django. Se crean las carpetas y archivos manualmente.

```bash
mkdir api
cd api
```

Crea un archivo `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hola FastAPI"}
```

Ejecuta: para arrancar una aplicación básica.

```bash
uvicorn main:app --reload
```

### Estructura recomendada

```
FASTAPI/
│
├── api/
│   ├── main.py
│   ├── routers/
│   │   └── users.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── core/
│
├── requirements.txt
├── .env
└── README.md
```

### Equivalencia Django → FastAPI

| Django                                     | FastAPI                                |
| ------------------------------------------ | -------------------------------------- |
| `django-admin startproject security_api .` | Crear carpeta del proyecto y `main.py` |
| `python manage.py runserver`               | `uvicorn app.main:app --reload`        |
| `urls.py`                                  | Routers (`APIRouter`)                  |
| Views                                      | Endpoints (`@app.get`, `@app.post`)    |
| Models ORM                                 | SQLAlchemy / SQLModel                  |
| DRF Serializers                            | Pydantic Schemas                       |
| DRF ViewSets                               | APIRouter + dependencias               |


La estructura del proyecto, no la genera FastAPI automáticamente. 
FastAPI es bastante minimalista: da el framework para definir rutas, validación de datos, dependencias y documentación automática, pero la organización de carpetas normalmente se diseñas manualmente.

FastAPI te proporciona:

* `FastAPI()` para crear la aplicación.
* Decoradores de rutas (`@app.get`, `@app.post`, etc.).
* `APIRouter` para separar endpoints.
* Inyección de dependencias (`Depends`).
* Validación mediante Pydantic.
* Documentación automática Swagger/OpenAPI.
* Manejo de peticiones y respuestas HTTP.

Estructura:

```text
project/
│
├── __pycache__/
├── models/
├── routes/
├── util/
│
├── __init__.py
├── database.py
├── dependencies.py
├── main.py
├── models.py
├── schemas.py
└── security.py
```

`main.py`: Punto de entrada de la aplicación.

```python
from fastapi import FastAPI

app = FastAPI()
```

`database.py`: Configuración de la base de datos.

`models.py`: Modelos ORM (SQLAlchemy).

```python
class User(Base):
    __tablename__ = "users"
```
`schemas.py`: Esquemas Pydantic para validar entrada y salida.

```python
class UserCreate(BaseModel):
    username: str
```

`dependencies.py`: Dependencias reutilizables.

```python
def get_db():
    ...
```

`security.py`: Autenticación y JWT.

```python
def create_access_token():
    ...
```

`routes/`:  Controladores o endpoints agrupados por recurso.

```text
routes/
├── users.py
├── auth.py
└── products.py
```

`models/`: aquí se separan los modelos.

```text
models/
├── user.py
├── role.py
└── permission.py
```

`util/`: Funciones auxiliares.

```text
util/
├── validators.py
├── helpers.py
└── constants.py
```

**Comparación rápida con Django**

| Django         | FastAPI                              |
| -------------- | ------------------------------------ |
| settings.py    | Configuración manual                    |
| urls.py        | routes/                              |
| models.py      | models.py                            |
| serializers.py | schemas.py                           |
| views.py       | routes/*.py                          |
| authentication | security.py                          |
| manage.py      | No existe                            |
| ORM incluido   | instalar SQLAlchemy u otro ORM |


# Código Completo comentado:

## main.py (código comentado)
`main.py` es el punto de entrada de tu API. 

```python
# ============================================================
# IMPORTACIONES
# ============================================================

# Clase principal de FastAPI para crear la aplicación.
from fastapi import FastAPI

# Middleware que permite configurar CORS
# (Cross-Origin Resource Sharing).
from fastapi.middleware.cors import CORSMiddleware

# Importación de los routers definidos en la carpeta routes.
# Gracias al archivo __init__.py podemos importarlos desde api.routes.
from api.routes import (
    user_routes,
    role_routes,
    permission_routes,
    role_permission_routes,
    session_routes,
    auth_log_routes
)

# ============================================================
# CREACIÓN DE LA APLICACIÓN
# ============================================================

# Instancia principal de FastAPI.
# title y version aparecerán en Swagger (/docs).
app = FastAPI(
    title="Security API",
    version="1.0.0"
)

# ============================================================
# CONFIGURACIÓN CORS
# ============================================================

# Lista de orígenes autorizados para consumir la API.
# Se utiliza durante el desarrollo local.
origins = [
    "https://127.0.0.1:5501",
    "https://localhost:5501",
    "http://127.0.0.1:5500",
    "http://localhost:5500"
]

# Middleware CORS.
# Permite que aplicaciones frontend autorizadas
# realicen peticiones a la API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://127.0.0.1:5501",
        #"https://localhost:5501",
        "http://127.0.0.1:5501",
        #"http://localhost:5501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# CABECERAS DE SEGURIDAD HTTP. Middleware de seguridad
# ============================================================

# Middleware que añade cabeceras de seguridad
# a todas las respuestas enviadas por la API.
@app.middleware("http")
async def add_security_headers(request, call_next):

    # Continúa el flujo normal de la petición.
    response = await call_next(request)

    # Evita que el navegador interprete tipos MIME incorrectos.
    response.headers["X-Content-Type-Options"] = "nosniff"

    # Impide que la API sea cargada dentro de iframes.
    response.headers["X-Frame-Options"] = "DENY"

    # Política de Seguridad de Contenido (CSP).
    # Restringe los recursos que pueden cargarse.
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "img-src 'self' data: https://fastapi.tiangolo.com;"
    )

    return response

# ============================================================
# REGISTRO DE RUTAS
# ============================================================

# Cada router agrupa endpoints relacionados con una entidad.
# FastAPI combinará automáticamente todas las rutas
# dentro de la aplicación principal.

# Usuarios
app.include_router(user_routes, prefix="/api", tags=["Users"])

# Roles
app.include_router(role_routes, prefix="/roles", tags=["Roles"])

# Permisos
app.include_router(permission_routes, prefix="/permissions", tags=["Permissions"])

# Relación Rol-Permiso
app.include_router(
    role_permission_routes,
    prefix="/role-permissions",
    tags=["Role Permissions"]
)

# Sesiones activas
app.include_router(session_routes, prefix="/sessions", tags=["Sessions"])

# Logs de autenticación
app.include_router(auth_log_routes, prefix="/logs", tags=["Auth Logs"])

# ============================================================
# ENDPOINT RAÍZ
# ============================================================

# Endpoint de comprobación rápida (health check).
# Permite verificar que la API está operativa.
@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}
```

## database.py 
============================================================
DATABASE CONFIGURATION MODULE
============================================================
Este módulo gestiona toda la configuración de acceso a la base de datos del proyecto utilizando SQLAlchemy.
- Carga variables de entorno desde el archivo .env. (Lee la configuración de conexión desde variables de entorno) 
- Construye la cadena de conexión a MySQL (Crear el motor de conexión (engine))
- Inicializa el motor de base de datos (engine) 
- Define la fábrica de sesiones (SessionLocal) (Crear sesiones de trabajo (SessionLocal))
- Define la clase Base para los modelos ORM (Define la clase base (Base) para todos los modelos)

TECNOLOGÍAS: FastAPI, SQLAlchemy, PyMySQL, python-dotenv.

Es el corazón de la capa de persistencia. Si main.py arranca la API, database.py es quien permite hablar con MySQL.

```python
# ============================================================
# IMPORTACIONES
# ============================================================

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# ============================================================
# CARGA DE VARIABLES DE ENTORNO
# ============================================================

# Carga el archivo .env para poder usar variables como MYSQL_USER, para evitar almacenar credenciales directamente en el código.
load_dotenv()

# ============================================================
# VARIABLES DE CONFIGURACIÓN DE BASE DE DATOS
# ============================================================

# Obtiene los parámetros de conexión desde las variables de entorno configuradas en .env.
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("MYSQL_HOST")
DB_PORT = os.getenv("MYSQL_PORT")
DB_NAME = os.getenv("MYSQL_DATABASE")

# ============================================================
# CADENA DE CONEXIÓN (DATABASE URL). Construcción de la URL de conexión
# ============================================================
# Cadena de conexión utilizada por SQLAlchemy para conectarse a la base de datos MySQL mediante PyMySQL.

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

"""
Formato de la URL:

mysql+pymysql://usuario:contraseña@host:puerto/nombre_bd

- mysql+pymysql → tipo de base de datos y driver
- usuario:contraseña → credenciales de acceso
- host:puerto → ubicación de la base de datos
- nombre_bd → base de datos a utilizar
"""

# ============================================================
# MOTOR DE CONEXIÓN (ENGINE). Crear el motor (Engine)
# ============================================================
# El engine es el administrador de conexiones. No ejecuta consultas directamente. Motor principal de conexión a la base de datos. Gestiona el pool de conexiones y la comunicación entre SQLAlchemy y MySQL.
# Se encarga de: abrir conexiones, reutilizar conexiones, cerrar conexiones, gestionar el pool
# Sirve como puente entre Python y MySQL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # Verifica conexiones antes de usarlas
)
# Esto crea el motor de conexión a la base de datos.
# el objeto que sabe: cómo conectarse a la DB,  qué tipo de DB es (MySQL en tu caso) y cómo gestionar conexiones

# ============================================================
# FÁBRICA DE SESIONES (SESSION LOCAL)
# ============================================================
# La Session representa una conversación activa con la base de datos. Fábrica de sesiones.
# Cada petición de FastAPI normalmente utilizará una sesión independiente para trabajar con la base de datos.
# autoflush=False: Evita que SQLAlchemy envíe cambios automáticamente antes de cada consulta.
# autocommit=False: Control de cuando guardar. Da más control sobre cuándo sincronizar los datos.
# bind=engine: Indica qué motor utilizar para crear las sesiones.

# Esto crea una fábrica de sesiones de base de datos: abrir conexiones a la bd.
# Una session es: una conexión activa con la base de datos para: 
# hacer consultas (SELECT)
# insertar datos (INSERT)
# actualizar (UPDATE)
# borrar (DELETE)

#sessionmaker: Es una función de SQLAlchemy que crea un generador de sesiones.

SessionLocal = sessionmaker(
    autocommit=False,  #los cambios no se guardan automáticamente. db.commit()
    autoflush=False,   #Evita que SQLAlchemy envíe cambios automáticamente antes de una consulta.
    bind=engine        #usa esta conexión a la base de datos. (ese engine viene de tu DATABASE_URL)
)

# ============================================================
# BASE PARA MODELOS ORM
# ============================================================
# Esta es probablemente la línea más importante después del engine. Clase base de la que heredarán todos los modelos ORM.
# Permite a SQLAlchemy mapear clases Python con tablas SQL. Todos tus modelos heredarán de ella.

Base = declarative_base() #Es la base de la que van a heredar todos tus modelos de base de datos.
                          #Esto define la estructura base para crear tablas en Python
                          #Cuando trabajas con SQLAlchemy, no escribes solo SQL, sino que defines clases Python que representan tablas
                          #Y todas esas clases necesitan una base común → Base.

# ============================================================
# NOTA OPCIONAL: CREACIÓN AUTOMÁTICA DE TABLAS
# ============================================================

# Base.metadata.create_all(bind=engine) #Esto crea todas las tablas automáticamente en la DB. Usamos fichero init.sql para la creación de tablas

#Si se descomenta la línea de arriba:SQLAlchemy creará automáticamente las tablas en la base de datos.
```

## dependencies.py. Código comentado

Este módulo (dependencies.py) centraliza las dependencias globales de la aplicación en FastAPI, principalmente la gestión de la conexión a la base de datos y la autenticación del usuario. 

get_db() crea y gestiona una sesión de base de datos por cada petición, asegurando su correcta apertura y cierre mediante el uso de yield y finally, lo que evita fugas de conexiones. 

get_current_user() implementa la lógica de autenticación basada en JWT, permitiendo obtener el usuario autenticado tanto desde cookies (para clientes web) como desde el header Authorization (para herramientas como Postman). Este diseño permite desacoplar la lógica de seguridad y acceso a datos del resto de la aplicación, facilitando su reutilización en los diferentes endpoints y mejorando la mantenibilidad del sistema.

Este módulo define las dependencias globales del proyecto. Responsabilidades:
- Gestión de conexión a base de datos (get_db)
- Autenticación del usuario actual (get_current_user)
- Validación de JWT (cookies y headers)
- Inyección de dependencias en FastAPI

Este archivo es clave en la arquitectura porque conecta: FastAPI + Base de datos + Autenticación + Seguridad

```python
# ============================================================
# IMPORTACIONES
# ============================================================

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from api.database import SessionLocal
from api.models import User
from api.security import SECRET_KEY, ALGORITHM, verify_token

# ============================================================
# CONFIGURACIÓN OAUTH2 (token por header Bearer)
# ============================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

# OAuth2PasswordBearer,permite obtener el token desde el header:Authorization: Bearer <token>

# ============================================================
# DEPENDENCIA: CONEXIÓN A BASE DE DATOS
# ============================================================

def get_db():
    db = SessionLocal() # Abre una conexión a la base de datos
                        # Es como decir: “quiero empezar a trabajar con la DB”
    try:
        yield db        #Entrega esa conexión al endpoint
                            #FastAPI : pausa la función usa db en el endpoint 
                            #          y cuando termina → vuelve a este punto
    finally:
        db.close()      # Cierra conexión base de datos

# ============================================================
# DEPENDENCIA: USUARIO AUTENTICADO
# ============================================================

# Función que obtiene el usuario autenticado desde JWT.
#    Soporta dos métodos:
#      1. Cookie (frontend web)
#      2. Authorization Header (Postman / APIs externas)

# Flujo:Extrae token -> Valida JWT -> Busca usuario en base de datos -> Retorna usuario autenticado

def get_current_user(request: Request,db: Session = Depends(get_db)):
    # ========================================================
    # 1. OBTENER TOKEN
    # ========================================================

    token = request.cookies.get("access_token")

    # Si no hay cookie, intentar desde header
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    # Si no hay token en ningún sitio. Error 401
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Token no proporcionado"
        )

    # ========================================================
    # 2. VALIDAR TOKEN JWT
    # ========================================================

    # Intenta decodificar el tocket JWT recibido. Verica
        # Que el token no esté alterado
        # firmado correctamente con SECRET_KEY. Definida en security.py
        # usa el algoritmo esperado. Definida en security.py
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        # si no existe el user_id dentro del token, significa que el token no continene la información mínima válida para identificar al usuario.
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )
    
    # Se ejecuta si el token está mal formado, ha sido manipulado, ha expirado o no se puede validar con la clave secreta.
    # Rechaza la autenticación devolviendo error 401
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    # ========================================================
    # 3. BUSCAR USUARIO EN BASE DE DATOS
    # ========================================================

    # Una vez validao el JWT, se obtiene el usuario asociado al identificador (user_id) almacenado en el token
    # Se realiza la consulta sobre la tabla User buscando el registro cuyo id coincida con el user_id extraído.
    user = db.query(User).filter(User.id == user_id).first()

    # Si no existe ningún usuario con ese identificador, se devuelve error 404
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    # Si el usuario existe se devuelve el objeto User.
    # A partir de este punto el endpoint puede acceder a sus datos, roles y permisos.
    return user
```
## Security.py (código comentado)
El módulo security.py centraliza las funciones relacionadas con la autenticación y protección de credenciales de la aplicación. Su responsabilidad principal es gestionar el cifrado seguro de contraseñas mediante Argon2, generar y validar tokens JWT para el control de acceso, y definir los parámetros criptográficos utilizados durante el proceso de autenticación. Además, implementa la creación diferenciada de tokens de acceso y refresco, incorporando información de seguridad como fecha de emisión (iat), fecha de expiración (exp), identificador único (jti) y tipo de token. Este diseño permite aplicar mecanismos de autenticación robustos y alineados con las recomendaciones de seguridad actuales para aplicaciones web y APIs REST.

```python
# ============================================================
# IMPORTACIONES
# ============================================================

# Componentes de FastAPI utilizados en procesos de autenticación.
# Algunas importaciones pueden reservarse para futuras ampliaciones.
from fastapi import FastAPI, Request, HTTPException, Depends

# Librería utilizada para el hash seguro de contraseñas.
from passlib.context import CryptContext

# Librería para generar y validar tokens JWT.
from jose import jwt

# Utilidades para trabajar con fechas y expiraciones.
from datetime import datetime, timedelta, timezone

# Generación de identificadores únicos para tokens.
import uuid

# ============================================================
# CONFIGURACIÓN JWT
# ============================================================

# Clave secreta utilizada para firmar y validar los JWT.
# En producción debería almacenarse en variables de entorno.
SECRET_KEY = "supersecret"  # JWT utiliza: SECRET_KEY para firmar los tokens.
#SECRET_KET = os.getenv("SECRECT_KEY") # evitas poner material criptográfico en el repositorio cumpliendo las recomendaciones de seguridad.

# Algoritmo de firma utilizado por JWT.
ALGORITHM = "HS256" # JWT utiliza:ALGORITHM para indicar el algoritmo criptográfico.

# ============================================================
# CONFIGURACIÓN DEL HASH DE CONTRASEÑAS
# ============================================================
# Argon2 es actualmente uno de los algoritmos más seguros para almacenar contraseñas.

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

# ============================================================
# GENERAR HASH DE CONTRASEÑA
# ============================================================
# Convierte una contraseña en texto plano en un hash seguro utilizando Argon2
# password (str): contraseña original
# Retorna (str): contraseña cifrada
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ============================================================
# VERIFICAR CONTRASEÑA
# ============================================================
# Comprueba si una contraseña en texto plano coincide con su versión almacenada en la base de datos.
    #   plain (str): contraseña introducida.
    #   hashed (str): hash almacenado.
        # Retorna->bool: True si coinciden.
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# ============================================================
# CREAR ACCESS TOKEN
# ============================================================
# Genera un JWT de acceso. Duración:30 minutos
# Claims añadidos:
    #    exp         -> fecha de expiración
    #    iat         -> fecha de emisión
    #    jti         -> identificador único
    #    token_type  -> tipo de token  
def create_access_token(data: dict):
    
    # Copia de los datos recibidos.
    to_encode = data.copy()

    # Fecha y hora actual UTC.
    now = datetime.now(timezone.utc)

    # Fecha de expiración.
    expire = now + timedelta(minutes=30)

    # Claims estándar y personalizados.
    to_encode.update({
        "exp": int(expire.timestamp()),
        "iat": int(now.timestamp()),
        "jti": str(uuid.uuid4()),
        "token_type": "access"
    })

    # Firma y devuelve el token.
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

# ============================================================
# CREAR REFRESH TOKEN
# ============================================================
# Genera un JWT de refresco. Duración:7 días
#    Utilidad: Permite obtener nuevos access tokens sin necesidad de volver a autenticarse.

def create_refresh_token(data: dict):
    # Fecha actual.
    now = datetime.now(timezone.utc)

    # Expiración a largo plazo.
    expire = now + timedelta(days=7)

    # Copia de los datos originales.
    to_encode = data.copy()

    # Claims JWT.
    to_encode.update({
        "exp": int(expire.timestamp()),
        "iat": int(now.timestamp()),
        "jti": str(uuid.uuid4()),
        "token_type": "refresh"
    })

    # Firma el token.
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

# ============================================================
# VALIDAR TOKEN JWT
# ============================================================
# Decodifica y valida un token JWT.
        # token (str): JWT recibido desde cookie o cabecera Authorization.
        # Retorna -> dict: payload contenido en el token.
#    Excepciones: JWTError si el token es inválido, está manipulado o ha expirado.
def verify_token(token: str):
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload
```

Este módulo centraliza todas las funcionalidades relacionadas
con la autenticación y seguridad de la API.

Responsabilidades:
- Cifrado de contraseñas mediante Argon2
- Verificación de contraseñas
- Generación de Access Tokens (JWT)
- Generación de Refresh Tokens (JWT)
- Validación de tokens JWT
- Configuración de algoritmos y claves criptográficas

Tecnologías utilizadas:
- Passlib
- Argon2
- Python-JOSE
- JWT (JSON Web Token)

# models.py
El módulo models.py define el modelo de datos de la aplicación mediante SQLAlchemy ORM, estableciendo la correspondencia entre las clases Python y las tablas de la base de datos relacional. En este módulo se representan las entidades principales del sistema de seguridad, incluyendo usuarios, roles, permisos, sesiones activas y registros de auditoría de autenticación. Además, se implementan las relaciones entre entidades, como la asociación muchos a muchos entre roles y permisos mediante una tabla intermedia. Esta capa de abstracción permite manipular la información de la base de datos utilizando objetos Python, facilitando el mantenimiento del código, la integridad de los datos y la aplicación de reglas de negocio dentro de la arquitectura de la API.

```python
# ============================================================
# IMPORTACIONES
# ============================================================
# Tipos de columnas utilizados por SQLAlchemy.
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime
)

# Permite definir relaciones entre tablas.
from sqlalchemy.orm import relationship

# Utilizado para registrar fechas en UTC.
from datetime import datetime, timezone

# Clase base definida en database.py.
from api.database import Base

# ============================================================
# TABLA INTERMEDIA ROLE_PERMISSIONS
# ============================================================
# Tabla puente para implementar la relación muchos a muchos entre roles y permisos.
# Un rol puede tener varios permisos.
# Un permiso puede pertenecer a varios roles.
class RolePermission(Base):
    __tablename__ = "role_permissions"

    # Clave primaria compuesta.
    role_id = Column(
        Integer,
        ForeignKey("roles.id"),
        primary_key=True
    )

    permission_id = Column(
        Integer,
        ForeignKey("permissions.id"),
        primary_key=True
    )

# ============================================================
# TABLA ROLES
# ============================================================
# Representa los roles disponibles en el sistema. Administrador/Usuario
class Role(Base):
    __tablename__ = "roles"

    # Identificador único del rol.
    id = Column(Integer, primary_key=True)

    # Nombre único del rol.
    name = Column(String(50), unique=True)

    # Descripción opcional.
    description = Column(String(255))

    # --------------------------------------------------------
    # RELACIÓN 1:N CON USERS
    # --------------------------------------------------------
    # Un rol puede estar asociado a múltiples usuarios.
    users = relationship(
        "User",
        back_populates="role"
    )

    # --------------------------------------------------------
    # RELACIÓN N:M CON PERMISSIONS
    # --------------------------------------------------------
    # Un rol puede tener múltiples permisos.
    permissions = relationship(
        "Permission",
        secondary="role_permissions",
        back_populates="roles"
    )

# ============================================================
# TABLA PERMISSIONS
# ============================================================
# Representa los permisos disponibles en el sistema.create_user/delete_user/view_logs

class Permission(Base):

    __tablename__ = "permissions"

    # Identificador único.
    id = Column(Integer, primary_key=True)

    # Nombre único del permiso.
    name = Column(String(100), unique=True)

    # Descripción funcional.
    description = Column(String(255))

    # --------------------------------------------------------
    # RELACIÓN N:M CON ROLES
    # --------------------------------------------------------
    # Un permiso puede pertenecer a múltiples roles.
    roles = relationship(
        "Role",
        secondary="role_permissions",
        back_populates="permissions"
    )

# ============================================================
# TABLA USERS
# ============================================================
# Representa los usuarios registrados en el sistema.
class User(Base):
    __tablename__ = "users"

    # Identificador único del usuario.
    id = Column(Integer, primary_key=True)

    # Nombre de usuario único.
    username = Column(
        String(50),
        unique=True
    )

    # Correo electrónico único.
    email = Column(
        String(100),
        unique=True
    )

    # Contraseña cifrada mediante Argon2.
    password_hash = Column(String(255))

    # Rol asignado al usuario.
    role_id = Column(
        Integer,
        ForeignKey("roles.id")
    )

    # Estado lógico del usuario.
    is_active = Column(
        Boolean,
        default=True
    )

    # Fecha de creación del registro.
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    # --------------------------------------------------------
    # RELACIÓN N:1 CON ROLES
    # --------------------------------------------------------
    # Cada usuario pertenece a un único rol.
    role = relationship(
        "Role",
        back_populates="users"
    )

# ============================================================
# TABLA USER_SESSIONS
# ============================================================
# Almacena información sobre las sesiones activas. Permite:Auditoría/Seguimiento de conexiones/Revocación de sesiones
class UserSession(Base):
    __tablename__ = "user_sessions"

    # Identificador de sesión.
    id = Column(Integer, primary_key=True)

    # Usuario propietario de la sesión.
    user_id = Column(Integer)

    # Token JWT asociado.
    token = Column(String(500))

    # Dirección IP del cliente.
    ip_address = Column(String(50))

    # Información del navegador o cliente.
    user_agent = Column(String(255))

    # Fecha de inicio de sesión.
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    # Fecha de expiración de sesión.
    expires_at = Column(
        DateTime,
        nullable=True
    )

    # Estado de la sesión.
    is_active = Column(
        Boolean,
        default=True
    )

# ============================================================
# TABLA AUTH_LOGS
# ============================================================
# Tabla de auditoría de autenticación. Registra eventos relacionados con: Login\Logout\Tokens inválidos\Accesos denegados\Errores de autenticación
class AuthLog(Base):
    __tablename__ = "auth_logs"

    # Identificador único del evento.
    id = Column(Integer, primary_key=True)

    # Usuario relacionado con el evento.
    user_id = Column(
        Integer,
        nullable=True
    )

    # Acción realizada.
    action = Column(String(50))

    # Dirección IP origen.
    ip_address = Column(String(50))

    # Navegador o cliente utilizado.
    user_agent = Column(String(255))

    # Resultado de la acción.
    status = Column(String(50))

    # Fecha y hora del evento.
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

```
Este módulo define todas las entidades de la aplicación
utilizando SQLAlchemy ORM.

Cada clase representa una tabla de la base de datos.

Tablas definidas:
- roles
- permissions
- role_permissions
- users
- user_sessions
- auth_logs

Relaciones:
- Un usuario pertenece a un rol.
- Un rol puede tener muchos usuarios.
- Un rol puede tener muchos permisos.
- Un permiso puede pertenecer a muchos roles.

# shemas.py (código comentado)
El módulo schemas.py define los esquemas de validación y serialización de datos utilizando Pydantic, actuando como una capa intermedia entre las peticiones HTTP y los modelos de base de datos. Estos esquemas permiten validar automáticamente los datos recibidos por la API, garantizando que cumplen los requisitos establecidos antes de ser procesados por la lógica de negocio. Además, facilitan la serialización de objetos Python a formato JSON para las respuestas enviadas al cliente. La separación entre modelos ORM y esquemas Pydantic contribuye a una arquitectura más segura, mantenible y desacoplada, evitando exponer directamente la estructura interna de la base de datos a los consumidores de la API.

```python

# ============================================================
# IMPORTACIONES
# ============================================================

# Tipo datetime utilizado en sesiones y logs.
from datetime import datetime

# Optional permite indicar campos opcionales.
from typing import Optional

# BaseModel es la clase base de todos los schemas.
# EmailStr añade validación automática de correos electrónicos.
from pydantic import BaseModel, EmailStr

# ============================================================
# USERS
# ============================================================
# Datos necesarios para crear un usuario.
class UserCreate(BaseModel):
    # Nombre de usuario único.
    username: str

    # Correo electrónico validado automáticamente.
    email: EmailStr

    # Contraseña en texto plano.
    # Posteriormente será cifrada con Argon2.
    password: str

    # Rol asignado al usuario.
    role_id: int

# Datos permitidos para actualizar un usuario.
# Todos los campos son opcionales para permitir actualizaciones parciales.
class UserUpdate(BaseModel):
    username: Optional[str]

    email: Optional[str]

# Datos requeridos para cambiar una contraseña. old_password, new_password
class PasswordUpdate(BaseModel):
    # Contraseña actual.
    old_password: str

    # Nueva contraseña.
    new_password: str

# Credenciales utilizadas durante el login.
class UserLogin(BaseModel):
    # Usuario utilizado para autenticación.
    username: str

    # Contraseña proporcionada por el usuario.
    password: str

# Datos públicos devueltos al cliente. No incluye información sensible (hashes de contraseñas).
class UserOut(BaseModel):
    id: int
    username: str
    email: str

    # Permite convertir automáticamente objetos ORM de SQLAlchemy a objetos Pydantic.
    class Config:
        from_attributes = True

# ============================================================
# ROLES
# ============================================================
# Datos necesarios para crear un rol.
class RoleCreate(BaseModel):
    name: str
    description: Optional[str]

# Datos permitidos para actualizar un rol.
class RoleUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]

# ============================================================
# PERMISSIONS
# ============================================================
# Datos necesarios para crear un permiso.
class PermissionCreate(BaseModel):
    name: str
    description: Optional[str]

# Datos permitidos para actualizar un permiso.
class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# ============================================================
# USER SESSIONS
# ============================================================
# Información asociada a una sesión de usuario.
class UserSessionCreate(BaseModel):
    # Usuario propietario de la sesión.
    user_id: int

    # JWT asociado a la sesión.
    token: str

    # Dirección IP origen.
    ip_address: str

    # Navegador o cliente utilizado.
    user_agent: str

    # Fecha de expiración de la sesión.
    expires_at: Optional[datetime]

    # Estado de la sesión.
    is_active: Optional[bool] = True

# ============================================================
# AUTH LOGS
# ============================================================
# Datos registrados en la auditoría de autenticación.
class AuthLogCreate(BaseModel):
    # Usuario relacionado con el evento.
    user_id: Optional[int]

    # Acción realizada.
    action: str

    # Dirección IP origen.
    ip_address: str

    # Cliente o navegador utilizado.
    user_agent: str

    # Resultado de la operación.
    status: str

    # Fecha del evento.
    created_at: Optional[datetime] = None
```
Este módulo define los esquemas de validación de datos
utilizados por FastAPI mediante Pydantic.

Funciones principales:
- Validar datos de entrada (request)
- Validar datos de salida (response)
- Documentar automáticamente la API en Swagger
- Evitar exponer directamente los modelos ORM

Los schemas NO representan tablas de base de datos.
Representan estructuras de intercambio de datos.

# `__init__.py` comentado

El archivo `__init__.py` se utiliza para definir el paquete de Python y centralizar las importaciones más relevantes del módulo, facilitando su reutilización en el resto de la aplicación. En este caso, se exponen los esquemas relacionados con la entidad de usuario, permitiendo importarlos directamente desde el paquete principal sin necesidad de acceder al módulo `schemas.py` de forma explícita. Esta práctica mejora la organización del código, simplifica las importaciones y contribuye a una estructura más limpia y mantenible dentro del proyecto FastAPI.

PACKAGE INITIALIZER: Este archivo convierte el directorio en un paquete Python e indica qué componentes se exponen públicamente cuando se importa el módulo.

En este caso, centraliza la importación de los schemas de usuario para facilitar su uso desde otros módulos de la API."""

```python
# ============================================================
# IMPORTACIONES EXPLICITAS DEL PAQUETE
# ============================================================

# Se importan y exponen los schemas relacionados con usuarios
# para poder acceder a ellos directamente desde el paquete api.
from .schemas import (
    UserCreate,
    UserUpdate,
    PasswordUpdate
)
```
# roures/
El directorio `routes` contiene la capa de controladores de la API, donde se definen todos los endpoints accesibles por el cliente. Cada archivo dentro de este directorio agrupa las rutas relacionadas con una entidad o funcionalidad específica del sistema, como usuarios, roles, permisos, sesiones y registros de auditoría. Esta organización sigue un enfoque modular que separa las responsabilidades por dominio, facilitando el mantenimiento, la escalabilidad y la legibilidad del código. Además, el uso de routers de FastAPI permite encapsular la lógica de cada módulo de forma independiente, integrándolos posteriormente en la aplicación principal mediante `include_router`, lo que contribuye a una arquitectura limpia y desacoplada basada en principios de desarrollo REST.

# roures/__init__.py comentado
El archivo __init__.py del directorio routes actúa como un punto de agregación de los distintos routers que componen la API. Su función principal es centralizar la exportación de los módulos de rutas, permitiendo que sean importados de forma simplificada desde otros archivos del proyecto, especialmente desde main.py. Esta estructura mejora la organización del código al agrupar los controladores por funcionalidad y facilita la escalabilidad del sistema, ya que cada conjunto de endpoints se encuentra encapsulado en su propio módulo, manteniendo una arquitectura modular, clara y mantenible basada en FastAPI.

ROUTES PACKAGE INITIALIZER: Este archivo convierte la carpeta `routes` en un paquete Python y centraliza la exportación de todos los routers de la API.

Su objetivo es simplificar las importaciones en `main.py`, permitiendo registrar todas las rutas desde un único punto.

```python 
# ============================================================
# EXPORTACIÓN DE ROUTERS
# ============================================================

# Router de usuarios (gestión de usuarios)
from .user_routes import router as user_routes

# Router de roles (gestión de roles del sistema)
from .role_routes import router as role_routes

# Router de permisos (gestión de permisos)
from .permission_routes import router as permission_routes

# Router de relación rol-permisos (RBAC)
from .role_permission_routes import router as role_permission_routes

# Router de sesiones de usuario (control de sesiones activas)
from .session_routes import router as session_routes

# Router de logs de autenticación (auditoría del sistema)
from .auth_log_routes import router as auth_log_routes
```
# role\auth_log_routes.py comentado

El módulo auth_log_routes.py implementa los endpoints encargados de gestionar los registros de auditoría de autenticación del sistema. Estos registros permiten almacenar y consultar eventos relacionados con la seguridad, como inicios de sesión, cierres de sesión, accesos denegados o incidencias durante el proceso de autenticación. La existencia de esta funcionalidad facilita la trazabilidad de las acciones realizadas por los usuarios y constituye un mecanismo fundamental para tareas de auditoría, monitorización y análisis de incidentes de seguridad. Los endpoints desarrollados permiten consultar, crear y eliminar registros de auditoría mediante operaciones REST sobre la entidad AuthLog.

AUTH LOG ROUTES: Este módulo define los endpoints relacionados con los registros de auditoría de autenticación.

Funcionalidades:
- Consultar logs de autenticación
- Crear nuevos registros de auditoría
- Eliminar registros existentes

Los logs permiten realizar tareas de:
- Auditoría
- Monitorización
- Trazabilidad
- Investigación de incidentes

```python
# ============================================================
# IMPORTACIONES
# ============================================================

# Componentes básicos de FastAPI.
from fastapi import APIRouter, Depends, HTTPException

# Tipo Session utilizado por SQLAlchemy.
from sqlalchemy.orm import Session

# Fábrica de sesiones definida en database.py.
from api.database import SessionLocal

# Modelo ORM de la tabla auth_logs.
from api.models import AuthLog

# Schema utilizado para validar la creación de logs.
from api.schemas import AuthLogCreate

# Permite acceder a información de la petición HTTP.
# Actualmente no se utiliza en este archivo.
from fastapi import Request

# ============================================================
# CREACIÓN DEL ROUTER
# ============================================================

# Router independiente que posteriormente será registrado
# en main.py mediante include_router().
router = APIRouter()

# ============================================================
# DEPENDENCIA DE BASE DE DATOS
# ============================================================
# Crea una sesión de base de datos para cada petición.
#   Flujo:
#    1. Abre una conexión.
#    2. La entrega al endpoint.
#    3. La cierra automáticamente al finalizar.
def get_db():
    
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# ============================================================
# OBTENER TODOS LOS LOGS
# ============================================================
# Devuelve todos los registros almacenados en la tabla auth_logs.
# Método HTTP: GET. Endpoint: /logs
@router.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    return db.query(AuthLog).all()

# ============================================================
# CREAR NUEVO LOG
# ============================================================
# Crea un nuevo registro de auditoría. Método HTTP: POST. Endpoint: /logs
@router.post("/logs")
def create_log(
    log: AuthLogCreate,
    db: Session = Depends(get_db)
):
    
    # Convierte el schema recibido en una instancia ORM.
    new_log = AuthLog(**log.dict())

    # Añade el registro a la sesión actual.
    db.add(new_log)

    # Guarda los cambios en la base de datos.
    db.commit()

    # Recarga el objeto desde la base de datos para
    # obtener valores generados automáticamente.
    db.refresh(new_log)

    # Devuelve el registro creado.
    return new_log

# ============================================================
# ELIMINAR LOG
# ============================================================
# Elimina un registro de auditoría. Método HTTP: DELETE. Endpoint:/logs/{log_id}
@router.delete("/logs/{log_id}")
def delete_log(
    log_id: int,
    db: Session = Depends(get_db)
):
    # Busca el log por identificador.
    log = (
        db.query(AuthLog)
        .filter(AuthLog.id == log_id)
        .first()
    )

    # Si no existe se devuelve error 404.
    if not log:
        raise HTTPException(
            status_code=404,
            detail="Log no encontrado"
        )

    # Elimina el registro.
    db.delete(log)

    # Confirma cambios.
    db.commit()

    # Respuesta de confirmación.
    return {
        "message": "Log eliminado"
    }
```

# role\role_permission_routes.py comentado
El módulo role_permission_routes.py implementa los endpoints encargados de gestionar la relación entre roles y permisos dentro del sistema de control de acceso basado en roles (RBAC). Su función principal es permitir la asignación y revocación de permisos asociados a cada rol, facilitando la administración centralizada de privilegios. Mediante estos endpoints, los administradores pueden modificar dinámicamente las capacidades de los distintos perfiles de usuario sin necesidad de realizar cambios directos en la base de datos. Esta aproximación mejora la flexibilidad, escalabilidad y mantenibilidad del sistema de autorización, permitiendo adaptar fácilmente los permisos a las necesidades operativas de la aplicación.

ROLE-PERMISSION ROUTES: Este módulo gestiona la asignación y eliminación de permisos asociados a los roles del sistema.
Forma parte de la implementación del modelo RBAC (Role-Based Access Control).

Funcionalidades: Asignar permisos a un rol/Eliminar permisos de un rol.

Relación gestionada: Role <---> Permission

```python
# ============================================================
# IMPORTACIONES
# ============================================================
# Componentes básicos de FastAPI.
from fastapi import APIRouter, Depends, HTTPException

# Tipo Session utilizado por SQLAlchemy.
from sqlalchemy.orm import Session

# Fábrica de sesiones definida en database.py.
from api.database import SessionLocal

# Modelos ORM utilizados.
from api.models import Role, Permission

# Permite acceder a información de la petición HTTP.
# Actualmente no se utiliza en este módulo.
from fastapi import Request

# ============================================================
# CREACIÓN DEL ROUTER
# ============================================================

# Router independiente que será registrado posteriormente
# desde main.py mediante include_router().
router = APIRouter()

# ============================================================
# DEPENDENCIA DE BASE DE DATOS
# ============================================================
# Genera una sesión de base de datos por petición.
# Flujo:
#    1. Abre conexión.
#    2. La entrega al endpoint.
#    3. La cierra automáticamente al finalizar.
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# ============================================================
# ASIGNAR PERMISO A UN ROL
# ============================================================
# Asigna un permiso existente a un rol existente. Método HTTP: POST. Endpoint: /roles/{role_id}/permisos/{permiso_id}
@router.post("/roles/{role_id}/permisos/{permiso_id}")
def add_permission(
    role_id: int,
    permiso_id: int,
    db: Session = Depends(get_db)
):
    # Buscar rol por identificador.
    role = db.get(Role, role_id)

    # Buscar permiso por identificador.
    permiso = db.get(Permission, permiso_id)

    # Verificar existencia de ambas entidades.
    if not role or not permiso:
        raise HTTPException(
            status_code=404,
            detail="Rol o permiso no encontrado"
        )

    # Verificar que el permiso aún no esté asignado.
    if permiso not in role.permissions:

        # Añadir relación en la tabla intermedia.
        role.permissions.append(permiso)

        # Guardar cambios.
        db.commit()

        return {
            "message": "Permiso añadido"
        }

    # Si ya existe la relación.
    return {
        "message": "El permiso ya estaba asignado"
    }

# ============================================================
# ELIMINAR PERMISO DE UN ROL
# ============================================================
# Elimina la relación entre un rol y un permiso. Método HTTP: DELETE. Endpoint:/roles/{role_id}/permisos/{permiso_id}
@router.delete("/roles/{role_id}/permisos/{permiso_id}")
def remove_permission(
    role_id: int,
    permiso_id: int,
    db: Session = Depends(get_db)
):
    # Buscar rol por identificador.
    role = db.get(Role, role_id)

    # Buscar permiso por identificador.
    permiso = db.get(Permission, permiso_id)

    # Verificar existencia de ambas entidades.
    if not role or not permiso:
        raise HTTPException(
            status_code=404,
            detail="Rol o permiso no encontrado"
        )

    # Comprobar que el permiso está asignado.
    if permiso in role.permissions:

        # Eliminar relación en la tabla intermedia.
        role.permissions.remove(permiso)

        # Guardar cambios.
        db.commit()

        return {
            "message": "Permiso eliminado"
        }

    # Si no existe relación previa.
    return {
        "message": "El permiso no estaba asignado"
    }
```

# role\role_routes.py comentado
El módulo role_routes.py implementa las operaciones CRUD (Create, Read, Update, Delete) sobre la entidad de roles dentro del sistema de control de acceso. A través de estos endpoints es posible crear nuevos roles, consultar roles existentes, modificar su información y eliminarlos cuando ya no son necesarios. Los roles constituyen un elemento fundamental del modelo RBAC (Role-Based Access Control), ya que permiten agrupar permisos y asignarlos posteriormente a los usuarios. Esta separación entre usuarios, roles y permisos facilita la administración de privilegios, mejora la escalabilidad del sistema y simplifica la gestión de autorizaciones en entornos con múltiples perfiles de acceso.

ROLE ROUTES: Este módulo implementa los endpoints encargados de la gestión de roles dentro del sistema.

Operaciones disponibles:
- Listar roles
- Crear roles
- Consultar un rol
- Actualizar un rol
- Eliminar un rol

Los roles forman parte del modelo RBAC (Role-Based Access Control).

```python
# ============================================================
# IMPORTACIONES
# ============================================================

# Componentes básicos de FastAPI.
from fastapi import APIRouter, Depends, HTTPException

# Tipo Session utilizado por SQLAlchemy.
from sqlalchemy.orm import Session

# Fábrica de sesiones de base de datos.
from api.database import SessionLocal

# Modelos ORM relacionados con roles y permisos.
from api.models import Role, RolePermission, Permission

# Schemas utilizados para validar datos de entrada.
from api.schemas import RoleCreate, RoleUpdate

# Permite acceder a información de la petición HTTP.
# Actualmente no se utiliza en este archivo.
from fastapi import Request

# ============================================================
# CREACIÓN DEL ROUTER
# ============================================================

# Router independiente que será registrado desde main.py.
router = APIRouter()

# ============================================================
# DEPENDENCIA DE BASE DE DATOS
# ============================================================
# Genera una sesión de base de datos para cada petición.
# Flujo:
#    1. Abre conexión.
#    2. La entrega al endpoint.
#    3. La cierra automáticamente al finalizar.
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# ============================================================
# LISTAR TODOS LOS ROLES
# ============================================================
# Recupera todos los roles registrados en la base de datos. Método HTTP: GET. Endpoint:/roles
@router.get("/roles")
def get_roles(
    db: Session = Depends(get_db)
):
    # Obtener todos los registros de la tabla roles.
    roles = db.query(Role).all()

    return roles

# ============================================================
# CREAR NUEVO ROL
# ============================================================
# Crea un nuevo rol. Método HTTP: POST. Endpoint:/roles
@router.post("/roles")
def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db)
):
    # Crear instancia del modelo ORM.
    new_role = Role(
        name=role.name,
        description=role.description
    )

    # Añadir el objeto a la sesión.
    db.add(new_role)

    # Guardar cambios en la base de datos.
    db.commit()

    # Recargar el objeto desde la base de datos.
    db.refresh(new_role)

    # Devolver el rol creado.
    return new_role

# ============================================================
# OBTENER ROL POR ID
# ============================================================
# Recupera un rol concreto mediante su identificador. Método HTTP: GET. Endpoint:/roles/{role_id}
@router.get("/roles/{role_id}")
def get_role(
    role_id: int,
    db: Session = Depends(get_db)
):
    # Buscar rol por ID.
    role = (
        db.query(Role)
        .filter(Role.id == role_id)
        .first()
    )

    # Si no existe devolver error 404.
    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role no encontrado"
        )

    return role

# ============================================================
# ACTUALIZAR ROL
# ============================================================
# Actualiza los datos de un rol existente. Método HTTP: PUT. Endpoint:/roles/{role_id}
@router.put("/roles/{role_id}")
def update_role(
    role_id: int,
    role_data: RoleUpdate,
    db: Session = Depends(get_db)
):
    # Buscar rol en la base de datos.
    role = (
        db.query(Role)
        .filter(Role.id == role_id)
        .first()
    )

    # Verificar existencia.
    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role no encontrado"
        )

    # Actualizar nombre.
    role.name = role_data.name

    # Actualizar descripción.
    role.description = role_data.description

    # Guardar cambios.
    db.commit()

    # Recargar objeto actualizado.
    db.refresh(role)

    return role

# ============================================================
# ELIMINAR ROL
# ============================================================
# Elimina un rol existente. Método HTTP: DELETE. Endpoint:/roles/{role_id}
@router.delete("/roles/{role_id}")
def delete_role(
    role_id: int,
    db: Session = Depends(get_db)
):
    # Buscar rol por identificador.
    role = (
        db.query(Role)
        .filter(Role.id == role_id)
        .first()
    )

    # Verificar existencia.
    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role no encontrado"
        )

    # Eliminar registro.
    db.delete(role)

    # Confirmar cambios.
    db.commit()

    # Respuesta de confirmación.
    return {
        "message": "Role eliminado"
    }
```
# role\session_routes.py comentado
El módulo session_routes.py implementa los endpoints encargados de gestionar las sesiones de usuario almacenadas en el sistema. Estas sesiones permiten registrar información asociada a la autenticación de los usuarios, incluyendo el token utilizado, la dirección IP de origen, el agente de usuario (User-Agent) y el estado de la sesión. La gestión de sesiones proporciona una capa adicional de control y auditoría sobre los accesos a la aplicación, permitiendo consultar las sesiones activas, registrar nuevas conexiones y eliminar sesiones cuando sea necesario. Esta funcionalidad resulta especialmente útil para tareas de monitorización, control de accesos y detección de actividades sospechosas.

SESSION ROUTES: Este módulo implementa los endpoints encargados de gestionar las sesiones de usuario registradas en el sistema.

Funcionalidades:
- Consultar sesiones.
- Crear sesiones.
- Eliminar sesiones.

La información almacenada puede utilizarse para:
- Auditoría.
- Monitorización.
- Gestión de accesos.
- Control de sesiones activas.

```python
# ============================================================
# IMPORTACIONES
# ============================================================

# Componentes básicos de FastAPI.
from fastapi import APIRouter, Depends, HTTPException

# Tipo Session utilizado por SQLAlchemy.
from sqlalchemy.orm import Session

# Fábrica de sesiones de base de datos.
from api.database import SessionLocal

# Modelo ORM correspondiente a la tabla user_sessions.
from api.models import UserSession

# Schema utilizado para validar la creación de sesiones.
from api.schemas import UserSessionCreate

# Permite acceder a información de la petición HTTP.
# Actualmente no se utiliza en este módulo.
from fastapi import Request

# ============================================================
# CREACIÓN DEL ROUTER
# ============================================================

# Router independiente que posteriormente será registrado
# desde main.py mediante include_router().
router = APIRouter()

# ============================================================
# DEPENDENCIA DE BASE DE DATOS
# ============================================================
# Genera una sesión de base de datos para cada petición.
# Flujo:
#    1. Abre conexión.
#    2. La entrega al endpoint.
#    3. La cierra automáticamente al finalizar.
def get_db():
    # Crear sesión.
    db = SessionLocal()

    try:
        # Entregar sesión al endpoint.
        yield db

    finally:
        # Cerrar conexión.
        db.close()

# ============================================================
# OBTENER TODAS LAS SESIONES
# ============================================================
# Recupera todas las sesiones registradas. Método HTTP: GET. Endpoint:/sessions
@router.get("/sessions")
def get_sessions(
    db: Session = Depends(get_db)
):
    # Consulta completa de la tabla user_sessions.
    return db.query(UserSession).all()

# ============================================================
# CREAR NUEVA SESIÓN
# ============================================================
# Registra una nueva sesión de usuario. Método HTTP: POST. Endpoint:/sessions
@router.post("/sessions")
def create_session(
    session: UserSessionCreate,
    db: Session = Depends(get_db)
):
    # Crear objeto ORM utilizando los datos
    # validados por el schema.
    new_session = UserSession(
        **session.dict()
    )

    # Añadir objeto a la sesión actual.
    db.add(new_session)

    # Guardar cambios en la base de datos.
    db.commit()

    # Recargar el objeto desde la base de datos
    # para obtener valores generados automáticamente.
    db.refresh(new_session)

    # Devolver sesión creada.
    return new_session

# ============================================================
# ELIMINAR SESIÓN
# ============================================================
# Elimina una sesión existente. Método HTTP: DELETE. Endpoint:/sessions/{session_id}
@router.delete("/sessions/{session_id}")
def delete_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    # Buscar sesión por identificador.
    s = (
        db.query(UserSession)
        .filter(UserSession.id == session_id)
        .first()
    )

    # Comprobar existencia.
    if not s:
        raise HTTPException(
            status_code=404,
            detail="Session no encontrada"
        )

    # Eliminar registro.
    db.delete(s)

    # Confirmar cambios.
    db.commit()

    # Respuesta de confirmación.
    return {
        "message": "Session eliminada"
    }
```

# role\user_routes.py comentado
El módulo `user_routes.py` constituye el núcleo funcional de la API, ya que implementa los endpoints relacionados con la gestión de usuarios y los procesos de autenticación. Este componente permite realizar operaciones CRUD sobre los usuarios, gestionar el inicio y cierre de sesión, modificar credenciales y aplicar mecanismos de autorización basados en roles (RBAC). Además, incorpora controles de seguridad como el almacenamiento seguro de contraseñas mediante Argon2, la emisión de tokens JWT para la autenticación, la validación de permisos de acceso y el registro de eventos de auditoría asociados a operaciones sensibles. La combinación de estas funcionalidades proporciona una capa integral de gestión de identidades y control de acceso dentro del sistema.

El módulo user_routes.py implementa el núcleo del sistema de gestión de identidades y autenticación de la API. Este componente centraliza todas las operaciones relacionadas con los usuarios, incluyendo registro, autenticación mediante JSON Web Tokens (JWT), consulta de perfiles, actualización de datos, cambio de contraseñas, eliminación de cuentas y cierre de sesión. Además, incorpora mecanismos avanzados de seguridad como el hashing de contraseñas con Argon2, el control de acceso basado en roles (RBAC), la protección frente a vulnerabilidades como IDOR/BOLA y el registro de eventos de auditoría para todas las acciones críticas. Esta combinación de funcionalidades garantiza un sistema robusto de autenticación y autorización, alineado con buenas prácticas de seguridad en aplicaciones web modernas.

* Gestión de usuarios (CRUD)
* Login y logout
* Generación de JWT
* Control RBAC
* Auditoría (`log_event`)
* Cambio de contraseña
* Protección frente a IDOR/BOLA
* Gestión de cookies seguras
* Validación de acceso

user_routes.py
│
├── Importaciones
├── Configuración router
├── Dependencia get_db()
├── GET /usuarios
├── POST /registro
├── POST /token
├── GET /usuarios/{id}
├── PUT /usuarios/{id}/password
├── PUT /usuarios/{id}
├── DELETE /usuarios/{id}
└── POST /logout

USER ROUTES: Este módulo implementa la gestión completa de usuarios y autenticación del sistema.

Incluye funcionalidades de:
- Registro de usuarios
- Login con JWT
- Logout
- CRUD de usuarios
- Cambio de contraseña
- Control de acceso basado en roles (RBAC)
- Auditoría de eventos (log_event)

Además aplica medidas de seguridad como:
- Hash de contraseñas con Argon2
- Tokens JWT (access + refresh)
- Cookies seguras en HTTPS
- Protección contra acceso no autorizado (IDOR / BOLA)

```python
# ============================================================
# IMPORTACIONES
# ============================================================

# Router principal de FastAPI para definir endpoints
from fastapi import APIRouter, Depends, HTTPException

# Sesiones de SQLAlchemy para acceso a la base de datos
from sqlalchemy.orm import Session

# Conexión a la base de datos
from api.database import SessionLocal

# Modelo de usuario
from api.models import User

# Esquemas Pydantic (validación de entrada/salida)
from api.schemas import (
    UserCreate,
    UserUpdate,
    PasswordUpdate,
    UserLogin,
    UserOut
)

# Funciones de seguridad (hash, JWT)
from api.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)

# Dependencia para obtener usuario autenticado
from api.dependencies import get_current_user

# Permite acceder a request HTTP (IP, headers)
from fastapi import Request

# Función de auditoría (logs de seguridad)
from api.utils.logging import log_event

# Permite modificar cookies en la respuesta HTTP
from fastapi import Response

# Manejo de errores de integridad en BD
from sqlalchemy.exc import IntegrityError

# ============================================================
# CREACIÓN DEL ROUTER
# ============================================================

router = APIRouter()

# ============================================================
# DEPENDENCIA DE BASE DE DATOS
# ============================================================
# Crea y gestiona la sesión de base de datos.
# Flujo:
#    1. Abre conexión
#    2. La entrega al endpoint
#    3. La cierra automáticamente al finalizar
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# ============================================================
# LISTAR USUARIOS
# ============================================================
# Devuelve lista de usuarios.
# - Admin (role_id = 1): ve todos los usuarios
# - Usuario normal: solo ve su propio perfil
@router.get("/usuarios/", response_model=list[UserOut])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Si es admin → devuelve todos los usuarios
    if current_user.role_id == 1:
        return db.query(User).all()

    # Usuario normal → solo su propio usuario
    return [current_user]

# ============================================================
# REGISTRO DE USUARIO
# ============================================================
# Crea un nuevo usuario en el sistema.
    # - Hashea la contraseña con Argon2
    # - Registra eventos de auditoría
    # - Controla duplicados (email/username)
@router.post("/registro/", response_model=UserOut)
def create_user(
    user: UserCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    # Obtener IP del cliente
    ip = request.client.host

    # Obtener User-Agent del navegador
    user_agent = request.headers.get("user-agent")

    # Crear objeto usuario con contraseña hasheada
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
        role_id=user.role_id,
        is_active=True
    )

    try:
        # Guardar en base de datos
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        # Revertir cambios si hay error de duplicado
        db.rollback()

        # Registrar intento fallido
        log_event(db, None, "duplicate_user", "400", ip, user_agent)

        raise HTTPException(
            status_code=400,
            detail="El usuario o email ya existe"
        )

    # Registrar creación exitosa
    log_event(db, new_user.id, "user_created", "201", ip, user_agent)

    return new_user

# ============================================================
# LOGIN (GENERACIÓN DE TOKENS JWT)
# ============================================================
# Autenticación de usuario.
#   - Verifica credenciales
#   - Genera access + refresh token
#   - Registra eventos de seguridad
@router.post("/token/")
def login_user(
    user: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    # IP del cliente
    ip = request.client.host

    # User-Agent del cliente
    user_agent = request.headers.get("user-agent")

    # Buscar usuario en BD
    db_user = db.query(User).filter(User.username == user.username).first()

    # Usuario no encontrado
    if not db_user:
        log_event(db, None, "login_failed", "401", ip, user_agent)
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    # Verificar contraseña
    if not verify_password(user.password, db_user.password_hash):
        log_event(db, None, "login_failed", "401", ip, user_agent)
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # Login correcto
    log_event(db, db_user.id, "login_success", "200", ip, user_agent)

    # Datos incluidos en el token JWT
    token_data = {
        "user_id": db_user.id,
        "username": db_user.username,
        "role_id": db_user.role_id,
    }

    # Generación de tokens
    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
        "token_type": "bearer"
    }

# ============================================================
# OBTENER USUARIO POR ID
# ============================================================
# Devuelve un usuario específico.
#     Acceso permitido:
#     - Admin
#     - Propietario del usuario
@router.get("/usuarios/{user_id}/", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Buscar usuario
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Control de acceso (BOLA protection)
    if current_user.role_id == 1 or current_user.id == user_id:
        return user

    raise HTTPException(status_code=403, detail="No autorizado")

# ============================================================
# CAMBIO DE CONTRASEÑA
# ============================================================
# Permite cambiar la contraseña de un usuario.
#     Incluye:
#   - Verificación de contraseña actual
#   - Hash de nueva contraseña
#   - Auditoría de evento
@router.put("/usuarios/{user_id}/password/")
def change_password(
    user_id: int,
    password_data: PasswordUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ip = request.client.host
    user_agent = request.headers.get("user-agent")

    # Control de acceso
    if current_user.role_id != 1 and current_user.id != user_id:
        log_event(db, current_user.id, "forbidden_access", "403", ip, user_agent)
        raise HTTPException(status_code=403, detail="No autorizado")

    # Buscar usuario
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar contraseña actual
    if not verify_password(password_data.old_password, user.password_hash):
        log_event(db, current_user.id, "password_change_failed", "400", ip, user_agent)
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")

    # Guardar nueva contraseña hasheada
    user.password_hash = hash_password(password_data.new_password)
    db.commit()

    # Log éxito
    log_event(db, current_user.id, "password_change", "200", ip, user_agent)

    return {"msg": "Contraseña actualizada correctamente"}

# ============================================================
# ACTUALIZAR USUARIO
# ============================================================
# Actualiza username y email de un usuario.
#    Solo permitido para:
#   - Admin
#   - Propietario del usuario
@router.put("/usuarios/{user_id}/", response_model=UserOut)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Control de acceso
    if current_user.role_id != 1 and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No autorizado")

    # Buscar usuario
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualizar datos
    user.username = user_data.username
    user.email = user_data.email

    db.commit()
    db.refresh(user)

    return user

# ============================================================
# ELIMINAR USUARIO
# ============================================================
#  Elimina un usuario del sistema. Incluye control de acceso y auditoría.
@router.delete("/usuarios/{user_id}/")
def delete_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ip = request.client.host
    user_agent = request.headers.get("user-agent")

    # Control de acceso
    if current_user.role_id != 1 and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No autorizado")

    # Buscar usuario
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Log eliminación
    log_event(db, current_user.id, "delete_user", "200", ip, user_agent)

    # Eliminar usuario
    db.delete(user)
    db.commit()

    return {"message": "Usuario eliminado"}

# ============================================================
# LOGOUT
# ============================================================
# Cierra sesión del usuario eliminando cookies.
@router.post("/logout/")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return {"message": "Logout correcto"}