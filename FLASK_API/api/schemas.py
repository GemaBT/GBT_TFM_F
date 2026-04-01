#from pydantic import BaseModel
#from typing import Optional
from datetime import datetime

from typing import Optional
from pydantic import BaseModel, EmailStr


# ----------------------
# Users
# ----------------------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role_id: Optional[int] = 2  # Por defecto 'usuario'

#class UserCreate(BaseModel):
#    username: str
#    email: str
#    password: str

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]

class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ----------------------
# Roles
# ----------------------
class RoleCreate(BaseModel):
    name: str
    description: Optional[str]

class RoleUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]

# ----------------------
# Permissions
# ----------------------
class PermissionCreate(BaseModel):
    name: str
    description: Optional[str]

class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
# ----------------------
# User Sessions
# ----------------------
class UserSessionCreate(BaseModel):
    user_id: int
    token: str
    ip_address: str
    user_agent: str
    expires_at: Optional[datetime]
    is_active: Optional[bool] = True

# ----------------------
# Auth Logs
# ----------------------
class AuthLogCreate(BaseModel):
    user_id: Optional[int]
    action: str
    ip_address: str
    user_agent: str
    status: str
    created_at: Optional[datetime] = None