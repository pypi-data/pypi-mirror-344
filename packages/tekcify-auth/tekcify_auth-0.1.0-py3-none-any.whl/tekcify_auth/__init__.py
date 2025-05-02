"""
Tekcify Auth - OAuth and Authentication for Python Applications

A library that provides OAuth integration and authentication tools
for Python applications using Tekcify services.
"""

__version__ = "0.1.0"

from tekcify_auth.core.client import Tekcify
from tekcify_auth.core.errors import TekcifyConnectionError, TekcifyAuthError
from tekcify_auth.decorators.auth import tekcify_auth_required

__all__ = [
    "Tekcify",
    "TekcifyConnectionError",
    "TekcifyAuthError",
    "tekcify_auth_required"
] 