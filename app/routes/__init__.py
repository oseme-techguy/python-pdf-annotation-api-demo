"""
    Routes
"""

from app.routes.index import index
from app.routes import users
from app.routes import documents
from app.routes import annotations
from app.routes import named_entities

__all__ = ('index', 'users', 'documents', 'annotations', 'named_entities')
