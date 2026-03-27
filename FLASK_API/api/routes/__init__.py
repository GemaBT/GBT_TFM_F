"""from .user_routes import user_routes
from .role_routes import role_routes
from .permission_routes import permission_routes
from .role_permission_routes import role_permission_routes
from .session_routes import session_routes
from .auth_log_routes import auth_log_routes
"""

from .user_routes import router as user_routes
from .role_routes import router as role_routes
from .permission_routes import router as permission_routes
from .role_permission_routes import router as role_permission_routes
from .session_routes import router as session_routes
from .auth_log_routes import router as auth_log_routes