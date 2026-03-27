"""from pydantic import BaseModel

# USERS
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# ROLES
class RoleCreate(BaseModel):
    name: str
    description: str

# PERMISSIONS
class PermissionCreate(BaseModel):
    name: str
    description: str

# ROLE-PERMISSION
class RolePermissionCreate(BaseModel):
    role_id: int
    permission_id: int

# USER SESSIONS
class UserSessionCreate(BaseModel):
    user_id: int
    token: str
    ip_address: str = None
    user_agent: str = None
    expires_at: str = None

# AUTH LOGS
class AuthLogCreate(BaseModel):
    user_id: int
    action: str
    ip_address: str = None
    user_agent: str = None
    status: str
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ----------------------
# Users
# ----------------------
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]

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