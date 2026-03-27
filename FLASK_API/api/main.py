"""from fastapi import FastAPI
from api.routes import user_routes, role_routes, permission_routes, role_permission_routes, session_routes, auth_log_routes

app = FastAPI()

app.include_router(user_routes.router, prefix="/api")
app.include_router(role_routes.router, prefix="/api")
app.include_router(permission_routes.router, prefix="/api")
app.include_router(role_permission_routes.router, prefix="/api")
app.include_router(session_routes.router, prefix="/api")
app.include_router(auth_log_routes.router, prefix="/api")
"""
"""from fastapi import FastAPI
#from routers import users
from api.router import user_routes

app = FastAPI()

#app.include_router(user_routes.router)
app.include_router(user_routes.router, prefix="/api")

"""
"""
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://api_user:api_password@localhost:3307/api_security")
conn = engine.connect()
result = conn.execute("SELECT * FROM users").fetchall()
print(result)
conn.close()
"""

"""from fastapi import FastAPI
from api.routes import user_routes, role_routes, permission_routes, session_routes, auth_log_routes


app = FastAPI(title="API Seguridad")

# Routers

app.include_router(user_routes.router, prefix="/api")
app.include_router(role_routes.router, prefix="/api")
app.include_router(permission_routes.router, prefix="/api")
app.include_router(session_routes.router, prefix="/api")
app.include_router(auth_log_routes.router, prefix="/api")

# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa todos los routers desde api/routes

from api.routes.user_routes import user_routes.route
from api.routes.role_routes import role_routes
from api.routes.permission_routes import permission_routes
from api.routes.role_permission_routes import role_permission_routes
from api.routes.session_routes import session_routes
from api.routes.auth_log_routes import auth_log_routes

from api.routes import user_routes, role_routes, permission_routes, role_permission_routes, session_routes, auth_log_routes

# Inicializa la app
app = FastAPI(
    title="TFM GBT API",
    description="API para gestión de usuarios, roles, permisos y sesiones",
    version="1.0.0"
)

# Configuración de CORS si la necesitas
origins = [
    "*",  # permite cualquier dominio (en producción restringirlo)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluye los routers con sus prefijos
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(role_routes.router, prefix="/roles", tags=["Roles"])
app.include_router(permission_routes.router, prefix="/permissions", tags=["Permissions"])
app.include_router(role_permission_routes.router, prefix="/role-permissions", tags=["Role-Permissions"])
app.include_router(session_routes.router, prefix="/sessions", tags=["Sessions"])
app.include_router(auth_log_routes.router, prefix="/auth-logs", tags=["Auth-Logs"])

# Ruta de prueba
@app.get("/")
def root():
    return {"message": "API TFM GBT funcionando correctamente"}

"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar routers desde routes (gracias al __init__.py)
from api.routes import (
    user_routes,
    role_routes,
    permission_routes,
    role_permission_routes,
    session_routes,
    auth_log_routes
)

app = FastAPI(
    title="Security API",
    version="1.0.0"
)

# CORS (opcional pero recomendado)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción limita esto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# REGISTRO DE RUTAS
# =========================

app.include_router(user_routes, prefix="/users", tags=["Users"])
app.include_router(role_routes, prefix="/roles", tags=["Roles"])
app.include_router(permission_routes, prefix="/permissions", tags=["Permissions"])
app.include_router(role_permission_routes, prefix="/role-permissions", tags=["Role Permissions"])
app.include_router(session_routes, prefix="/sessions", tags=["Sessions"])
app.include_router(auth_log_routes, prefix="/logs", tags=["Auth Logs"])

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"message": "API funcionando correctamente "}