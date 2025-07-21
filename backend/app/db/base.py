# This file is used to ensure all SQLAlchemy models are imported before initializing the DB.
# This is crucial for tools like Alembic that need to know about all models.

from app.db.base_class import Base
from app.models.user import User  # noqa