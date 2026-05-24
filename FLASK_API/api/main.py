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
    "https://127.0.0.1:5501",
    "https://localhost:5501",
    "http://127.0.0.1:5500",
    "http://localhost:5500"
]

# CORS 
"""app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""

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
"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://127.0.0.1:5501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
"""@app.middleware("http")   # añadimos manualmente cabeceras de seguridad.
async def add_security_headers(request, call_next):
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"

    return response
"""
@app.middleware("http") #https
async def add_security_headers(request, call_next):

    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"

    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "img-src 'self' data: https://fastapi.tiangolo.com;"
    )

    return response
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