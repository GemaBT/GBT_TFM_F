from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from api.database import Base

# ========================
# Tabla role_permissions
# ========================
class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)

# ========================
# Tabla roles
# ========================
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(255))
    
    # Relación con usuarios
    users = relationship("User", back_populates="role")
    
    # Relación con permisos a través de role_permissions
    permissions = relationship(
        "Permission",
        secondary="role_permissions",
        back_populates="roles"
    )

# ========================
# Tabla permissions
# ========================
class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    description = Column(String(255))

    # Relación con roles a través de role_permissions
    roles = relationship(
        "Role",
        secondary="role_permissions",
        back_populates="permissions"
    )

# ========================
# Tabla users
# ========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    password_hash = Column(String(255))
    role_id = Column(Integer, ForeignKey("roles.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relación con roles
    role = relationship("Role", back_populates="users")

# ========================
# Tabla user_sessions
# ========================
class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    token = Column(String(500))
    ip_address = Column(String(50))
    user_agent = Column(String(255))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

# ========================
# Tabla auth_logs
# ========================
class AuthLog(Base):
    __tablename__ = "auth_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    action = Column(String(50))
    ip_address = Column(String(50))
    user_agent = Column(String(255))
    status = Column(String(50))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))