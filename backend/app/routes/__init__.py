# Routes package init
from .auth_routes import auth_bp
from .credential_routes import credential_bp
from .user_routes import user_bp

__all__ = ['auth_bp', 'credential_bp', 'user_bp']
