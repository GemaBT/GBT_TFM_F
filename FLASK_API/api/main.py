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

origins = [
    "http://127.0.0.1:5500",  
    "http://localhost:5500"
]

# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# REGISTRO DE RUTAS
# =========================

#app.include_router(user_routes, prefix="/users", tags=["Users"])
app.include_router(user_routes, prefix="/api", tags=["Users"])
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