Perfecto, este es el **momento ideal** para migrar a cookies 🍪🔐
Te lo explico **paso a paso y aplicado a tu proyecto (FastAPI + frontend actual)**.

---

# 1) Qué vamos a cambiar

Ahora mismo haces esto en el frontend:

```javascript
localStorage.setItem("token", token)
```

y luego lo envías así:

```javascript
Authorization: Bearer ${token}
```

Vamos a cambiarlo por:

* el **backend guarda el JWT en una cookie**
* el navegador la envía automáticamente
* el frontend ya **no guarda nada**

Esto es mucho más seguro.

---

# 2) Qué cookie usar

La cookie debe llevar:

```python
httponly=True
secure=True
samesite="Lax"
```

Te explico cada una:

* **HttpOnly** → JavaScript no puede leerla
* **Secure** → solo HTTPS
* **SameSite** → protege frente a CSRF

Para desarrollo local:

```python
secure=False
```

porque en localhost no usas HTTPS.

---

# 3) Primer cambio: login en FastAPI

Ahora tienes esto:

```python
return {
    "access_token": create_access_token(token_data),
    "refresh_token": create_refresh_token(token_data),
    "token_type": "bearer"
}
```

Vamos a cambiarlo.

---

## ✅ Sustituye la función `login_user`

Pon esto:

```python
from fastapi import Response

@router.post("/token/")
def login_user(
    user: UserLogin,
    response: Response,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token_data = {
        "user_id": db_user.id,
        "username": db_user.username,
        "role_id": db_user.role_id,
    }

    access_token = create_access_token(token_data)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,      # True en producción
        samesite="Lax",
        max_age=1800
    )

    return {"message": "Login correcto"}
```

---

# 4) Segundo cambio: leer cookie en vez de header

Tu `get_current_user` seguramente usa:

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

Esto hay que cambiarlo.

---

## ✅ Modifica `dependencies.py`

Busca la función `get_current_user`.

Cámbiala por esto:

```python
from fastapi import Request

def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail="No autenticado"
        )

    payload = verify_token(token)

    user = db.query(User).filter(
        User.id == payload["user_id"]
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuario no válido"
        )

    return user
```

---

# 5) Tercer cambio: frontend login

Aquí es donde más cambia.

---

## ❌ Elimina esto

```javascript
const token = data.access_token || data.access;
if (token) localStorage.setItem("token", token);
```

YA NO SE USA.

---

## ✅ Añade esto al fetch

```javascript
credentials: "include"
```

---

## ✅ Login nuevo

```javascript
const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ username, password })
});
```

---

# 6) Cuarto cambio: resto de peticiones

Todas las peticiones protegidas deben llevar:

```javascript
credentials: "include"
```

---

## Antes

```javascript
headers: { "Authorization": `Bearer ${token}` }
```

---

## Ahora

```javascript
const res = await fetch(url, {
    credentials: "include"
});
```

---

# 7) Ejemplo listar usuarios

---

## ❌ Antes

```javascript
const token = localStorage.getItem("token");

const res = await fetch(url, {
    headers: {
        "Authorization": `Bearer ${token}`
    }
});
```

---

## ✅ Ahora

```javascript
const res = await fetch(url, {
    credentials: "include"
});
```

Muchísimo más limpio.

---

# 8) Muy importante → CORS

Si no configuras esto, no funcionará.

---

## En FastAPI

Busca:

```python
app.add_middleware(
    CORSMiddleware,
```

Y déjalo así:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔴 OJO

`allow_credentials=True` es obligatorio con cookies.

---

# 9) Logout (muy recomendable)

Añade endpoint:

```python
@router.post("/logout/")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logout correcto"}
```

---

# 10) Qué ganas en seguridad

Con esto mejoras:

---

## ✅ XSS

Antes podían robar token con:

```javascript
localStorage.getItem("token")
```

Ahora no.

---

## ✅ OWASP 2025

Esto mejora:

* **A01 Broken Access Control**
* **A02 Security Misconfiguration**
* **A07 Authentication Failures**

---

# 11) Recomendación TFM

Haz primero:

* login
* listar usuarios

Cuando eso funcione, migramos resto de endpoints.

Es la forma más segura.

---

Si quieres, te ayudo con el **código exacto de tu `dependencies.py` actual** para adaptarlo sin romper nada.


------------------------------------------------------------
cabeceras cors
Sí, aquí conviene que lo implementes **aunque todavía no estés usando cookies**, y tiene todo el sentido en tu TFM. Te explico primero el *por qué* (para que lo puedas justificar bien) y luego te doy los pasos para **FastAPI y Django**.

---

## 🧠 ¿Por qué implementar CORS ahora?

Aunque ahora estés usando JWT en headers (Authorization: Bearer), **CORS sigue siendo relevante** porque:

* Tu frontend (HTML + JS) hace peticiones desde otro origen (`localhost:...`)
* El navegador **sí aplica política CORS**, aunque no uses cookies
* Sin CORS:

  * O no funciona el frontend
  * O dejas la API abierta (`*`) → mala práctica de seguridad

👉 Además, OWASP A02 (Security Misconfiguration) incluye:

* APIs expuestas sin restricciones de origen
* Configuraciones permisivas innecesarias (`allow_origins="*"`)

📌 Por tanto, aunque no uses cookies aún:

* ✔️ **Debes restringir CORS**
* ✔️ Ya estás mitigando A02 correctamente
* ✔️ Y cuando migres a cookies, ya lo tendrás bien configurado

---

## 🧾 TEXTO PARA TU TFM (puedes copiar)

> En relación con la vulnerabilidad A02: Security Misconfiguration, se ha procedido a configurar adecuadamente la política de CORS (Cross-Origin Resource Sharing) en ambas APIs.
>
> Aunque en esta fase del experimento la autenticación se basa en tokens JWT enviados mediante cabeceras HTTP, y no en cookies, la configuración de CORS sigue siendo necesaria debido a la interacción con un frontend ejecutado en un origen distinto.
>
> Inicialmente, una configuración permisiva (allow_origins="*") puede facilitar el desarrollo, pero supone un riesgo de seguridad al permitir peticiones desde cualquier dominio. Por ello, se ha restringido el acceso únicamente a orígenes controlados, como el entorno local de desarrollo.
>
> Esta medida permite prevenir accesos no autorizados desde aplicaciones externas, reduciendo la superficie de ataque y alineándose con las recomendaciones del OWASP Top 10:2025 en cuanto a la correcta configuración de los servicios expuestos.
>
> Además, esta configuración sienta las bases para futuras mejoras de seguridad, como la migración a autenticación basada en cookies seguras, donde CORS adquiere un papel aún más crítico.

---

## ⚙️ IMPLEMENTACIÓN

---

# 🚀 FastAPI

### 1. Instalar middleware (si no lo tienes)

```bash
pip install fastapi[all]
```

---

### 2. En tu `main.py` (MUY IMPORTANTE)

Añade esto:

```python
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://127.0.0.1:5500",  # tu frontend
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # ❌ NO usar "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### 🔐 Claves importantes

* ❌ `allow_origins=["*"]` → inseguro
* ✔️ Lista cerrada de orígenes
* ✔️ `allow_credentials=True` → necesario cuando uses cookies después

---

# 🐍 Django REST Framework

---

### 1. Instalar librería

```bash
pip install django-cors-headers
```

---

### 2. Añadir en `settings.py`

```python
INSTALLED_APPS = [
    ...
    "corsheaders",
]
```

---

### 3. Middleware (ORDEN IMPORTANTE)

```python
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    ...
]
```

---

### 4. Configurar orígenes permitidos

```python
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]
```

---

### 5. (Preparado para futuro cookies)

```python
CORS_ALLOW_CREDENTIALS = True
```

---

## 🧪 PRUEBAS QUE DEBES HACER (esto te da puntos en el TFM)

### ✅ 1. Prueba correcta

* Desde tu frontend → funciona

---

### ❌ 2. Prueba ataque

* Cambia origen (por ejemplo desde otra app o puerto)
* Resultado esperado:

  * Bloqueo por CORS (error en navegador)

---

### ❌ 3. Configuración insegura (para justificar)

Temporalmente:

```python
allow_origins=["*"]
```

✔️ Resultado:

* Todo funciona → pero inseguro

📌 Esto lo explicas como:

> configuración funcional pero no segura

---

## 🎯 CONCLUSIÓN (lo que estás haciendo bien)

Con esto estás cubriendo:

* ✔️ A02 Security Misconfiguration
* ✔️ Preparando A07 Authentication (cookies después)
* ✔️ Evitando exposición innecesaria

---

Si quieres, en el siguiente paso te preparo **exactamente cómo documentar las pruebas (con capturas tipo Postman + navegador)** para que lo dejes perfecto de cara al TFM.
----------------------------------
Perfecto, esto ya es nivel “A09 bien hecho en TFM”. Te lo explico **paso a paso en Django y FastAPI**, porque aquí hay una diferencia importante de arquitectura.

---

# 🧩 1. IMPLEMENTACIÓN EN DJANGO (más sencillo)

## ✔️ Paso 1: Crear el modelo

En `models.py`:

```python id="d1j8kq"
from django.db import models
from django.contrib.auth.models import User

class SecurityLog(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=100)
    endpoint = models.CharField(max_length=200)
    status_code = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True)
```

---

## ✔️ Paso 2: Migraciones

```bash id="m1g2ra"
python manage.py makemigrations
python manage.py migrate
```

---

## ✔️ Paso 3: Función reutilizable de logging

Crea `utils/logging.py`:

```python id="lg8f3a"
from .models import SecurityLog

def log_event(user, action, endpoint, status_code, ip=None):
    SecurityLog.objects.create(
        user=user,
        action=action,
        endpoint=endpoint,
        status_code=status_code,
        ip_address=ip
    )
```

---

## ✔️ Paso 4: Uso en endpoints

### Login fallido:

```python id="lg1"
log_event(None, "login_failed", "/api/token/", 401)
```

### Login correcto:

```python id="lg2"
log_event(user, "login_success", "/api/token/", 200)
```

### Cambio de contraseña:

```python id="lg3"
log_event(user, "password_change", "/api/users/password/", 200)
```

---

## ✔️ Paso 5: Obtener IP (opcional)

```python id="ip1"
request.META.get("REMOTE_ADDR")
```

---

# ⚡ 2. IMPLEMENTACIÓN EN FASTAPI (más manual)

FastAPI NO tiene ORM por defecto, así que tienes 2 opciones:

* ✔️ SQLAlchemy (recomendado)
* ✔️ tabla directa con SQL

Te explico con SQLAlchemy (lo correcto en TFM).

---

## ✔️ Paso 1: Modelo

```python id="fa1"
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from database import Base

class SecurityLog(Base):
    __tablename__ = "security_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    action = Column(String(100))
    endpoint = Column(String(200))
    status_code = Column(Integer)
    ip_address = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
```

---

## ✔️ Paso 2: Crear tabla

```bash id="fa2"
alembic upgrade head
```

(o create_all si no usas migraciones)

---

## ✔️ Paso 3: función log_event

```python id="fa3"
from database import SessionLocal
from models import SecurityLog

def log_event(user_id, action, endpoint, status_code, ip=None):
    db = SessionLocal()
    log = SecurityLog(
        user_id=user_id,
        action=action,
        endpoint=endpoint,
        status_code=status_code,
        ip_address=ip
    )
    db.add(log)
    db.commit()
    db.close()
```

---

## ✔️ Paso 4: uso en endpoints

### Login fallo:

```python id="fa4"
log_event(None, "login_failed", "/api/token", 401)
```

### Login OK:

```python id="fa5"
log_event(user.id, "login_success", "/api/token", 200)
```

### Password change:

```python id="fa6"
log_event(user.id, "password_change", "/api/users/password", 200)
```

---

# 🧪 3. PRUEBAS QUE DEBES HACER

### ✔️ Login incorrecto

→ se guarda `login_failed`

### ✔️ Login correcto

→ se guarda `login_success`

### ✔️ Acceso sin token

→ `unauthorized_access`

### ✔️ Cambio password

→ `password_change`

### ✔️ Eliminación usuario

→ `delete_user`

---

# 🧠 4. QUÉ DEMUESTRAS EN EL TFM

Con esto estás demostrando:

* ✔️ Auditoría de seguridad (OWASP A09)
* ✔️ Trazabilidad de usuarios
* ✔️ Detección de ataques
* ✔️ Separación logs técnicos vs seguridad
* ✔️ Diseño profesional tipo producción

---

# 🚀 SI QUIERES SUBIR NOTA (RECOMENDADO)

Puedes añadir:

* IP del atacante
* User-Agent
* Timestamp preciso
* Endpoint exacto

---

Si quieres, te puedo hacer el siguiente paso nivel “proyecto real”:

👉 middleware automático de logging (para no poner log_event en cada endpoint)

Eso ya es nivel empresa +10 en TFM 🔥
